import os
import shutil

print("="*50)
print("DVC piplene.\tStep 1: Загрузка модели из S3 (MinIO)")
print("="*50)

os.makedirs('models', exist_ok=True)


if os.path.exists('models/model_v1.pth'):
    shutil.copy('models/model_v1.pth', 'models/model_v1_pretrained.pth')
    print("[ЭМУЛЯЦИЯ для колаба] Модель скопирована: models/model_v1_pretrained.pth")
else:
    print("Модель не найдена. Сначала загрузите model_v1.pth в папку models/")
    