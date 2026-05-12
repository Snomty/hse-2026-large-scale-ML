import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
import datetime
import json
import os

print("="*50)
print("DVC pipeline.\tStep 3: Тестирование на Test_2")
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

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

parent_dir = "/content/ai-vs-human-generated-dataset-hw/ai-vs-human-generated-dataset-hw"

test_dataset = ImageDataset(
    csv_file=parent_dir + '/Test_2/test.csv',
    root_dir=parent_dir + '/Test_2',
    transform=test_transform
)

test_dataset.data['file_name'] = test_dataset.data['file_name'].str.replace('train_data', 'test_data')

batch_size = 32
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

print(f'Test_2 dataset size: {len(test_dataset)}')

#######################################################################################################

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

#######################################################################################################

model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)

model_path = '../models/model_v2.pth'

if not os.path.exists(model_path):
    if os.path.exists('models/model_v2.pth'):
        model_path = 'models/model_v2.pth'
    else:
        print(f"Модель не найдена: {model_path}")
        print("Сначала запустите finetune.py")
        exit(1)

checkpoint = torch.load(model_path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
print(f"Загружена дообученная модель: {model_path}")

model = model.to(device)

#######################################################################################################

def validate(model, dataloader, device):
    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    criterion = nn.CrossEntropyLoss()

    with torch.no_grad():
        for images, labels in tqdm(dataloader, desc='Testing on Test_2'):
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_acc = accuracy_score(all_labels, all_preds)
    epoch_f1 = f1_score(all_labels, all_preds, average='weighted')
    epoch_precision = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
    epoch_recall = recall_score(all_labels, all_preds, average='weighted', zero_division=0)

    return epoch_loss, epoch_acc, epoch_f1, epoch_precision, epoch_recall

#######################################################################################################

print("Начало тестирования на Test_2")

test_loss, test_acc, test_f1, test_precision, test_recall = validate(model, test_loader, device)

# Логируем в TensorBoard
test_log_dir = f"logs/test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
test_writer = SummaryWriter(log_dir=test_log_dir)

test_writer.add_scalar('Test/Loss', test_loss, 0)
test_writer.add_scalar('Test/Accuracy', test_acc, 0)
test_writer.add_scalar('Test/F1', test_f1, 0)
test_writer.add_scalar('Test/Precision', test_precision, 0)
test_writer.add_scalar('Test/Recall', test_recall, 0)

test_writer.close()
print(f"Метрики залогированы в TensorBoard: {test_log_dir}")
