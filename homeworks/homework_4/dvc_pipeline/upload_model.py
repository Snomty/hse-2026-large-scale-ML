import os
import shutil

print("="*50)
print("DVC piplene.\tStep 4: Загрузка новой версии модели в S3")
print("="*50)


if os.path.exists('models/model_v2.pth'):
    size = os.path.getsize('models/model_v2.pth') / (1024*1024)
    print("[ЭМУЛЯЦИЯ для колаба] Модель готова к загрузке в S3")
    print(f"Файл: models/model_v2.pth ({size:.2f} MB)")
else:
    print("model_v2.pth не найдена!")
    