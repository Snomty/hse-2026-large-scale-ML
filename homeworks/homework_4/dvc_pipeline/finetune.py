import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
import datetime
from torchvision import transforms, models
from PIL import Image
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score
from tqdm import tqdm
import json
import os
import shutil

print("="*50)
print("DVC piplene.\tStep 2: Дообучение модели на Train_2")
print("="*50)

#######################################################################################################

class ImageDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.data = pd.read_csv(csv_file)
        self.root_dir = Path(root_dir)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.root_dir / self.data.iloc[idx]['file_name']
        image = Image.open(img_path).convert('RGB')
        label = self.data.iloc[idx]['label']

        if self.transform:
            image = self.transform(image)

        return image, label

#######################################################################################################

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

parent_dir = "/content/ai-vs-human-generated-dataset-hw/ai-vs-human-generated-dataset-hw"

train_dataset = ImageDataset(
    csv_file = parent_dir + '/Train_2/train.csv',
    root_dir = parent_dir + '/Train_2',
    transform=train_transform
)

batch_size = 32

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
print(f'Train dataset size: {len(train_dataset)}')

#######################################################################################################

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

#######################################################################################################

model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)

pretrained_path = 'models/model_v1_pretrained.pth'

if not os.path.exists(pretrained_path):
    if os.path.exists('models/model_v1.pth'):
        print("Копируем model_v1.pth -> model_v1_pretrained.pth")
        shutil.copy('models/model_v1.pth', pretrained_path)
    else:
        print(f"Модель не найдена: {pretrained_path}")
        print("Сначала запустите download_model.py")
        exit(1)

checkpoint = torch.load(pretrained_path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
print(f"Загружена предобученная модель: {pretrained_path}")

model = model.to(device)

#######################################################################################################

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)  # в 10 раз меньше
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)

finetune_params = {
    'learning_rate': 0.0001,
    'num_epochs': 5,
    'batch_size': batch_size,
    'optimizer': 'Adam',
    'scheduler': 'StepLR',
    'step_size': 3,
    'gamma': 0.5,
    'pretrained_model': 'model_v1.pth'
}

finetune_log_dir = f"logs/finetune_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
finetune_writer = SummaryWriter(log_dir=finetune_log_dir)

for key, value in finetune_params.items():
    finetune_writer.add_text('Fine-tuning Parameters', f'{key}: {value}', 0)

print(f"TensorBoard лог: {finetune_log_dir}")

#######################################################################################################

def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    all_preds = []
    all_labels = []

    for images, labels in tqdm(dataloader, desc='Fine-tuning'):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_acc = accuracy_score(all_labels, all_preds)
    epoch_f1 = f1_score(all_labels, all_preds, average='weighted')

    return epoch_loss, epoch_acc, epoch_f1

#######################################################################################################

num_epochs = 5
train_losses = []
train_accs = []
train_f1s = []

print("Начало дообучения")

for epoch in range(num_epochs):
    print(f'\nEpoch {epoch+1}/{num_epochs}')
    print('-' * 40)

    train_loss, train_acc, train_f1 = train_epoch(model, train_loader, criterion, optimizer, device)
    scheduler.step()

    train_losses.append(train_loss)
    train_accs.append(train_acc)
    train_f1s.append(train_f1)

    finetune_writer.add_scalar('Loss/train', train_loss, epoch)
    finetune_writer.add_scalar('Accuracy/train', train_acc, epoch)
    finetune_writer.add_scalar('F1/train', train_f1, epoch)
    finetune_writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)

    print(f'Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f}, F1: {train_f1:.4f}')

finetune_writer.close()

#######################################################################################################

finetune_metrics = {
    'train_losses': train_losses,
    'train_accs': train_accs,
    'train_f1s': train_f1s,
    'final_loss': train_losses[-1],
    'final_accuracy': train_accs[-1],
    'final_f1': train_f1s[-1]
}

os.makedirs('models', exist_ok=True)
torch.save({
    'model_state_dict': model.state_dict(),
    'finetune_metrics': finetune_metrics,
    'finetune_params': finetune_params
}, 'models/model_v2.pth')

print("Сохранена дообученная модель: models/model_v2.pth")
