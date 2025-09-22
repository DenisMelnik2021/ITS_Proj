from ultralytics import YOLO

path_to_model = 'escalator.v3i.yolov8/runs/detect/train/weights/best.pt'
path_to_img = 'escalator.v3i.yolov8/train/images/4_webp.rf.40f38faa43427cb3314b71efc16b34bd.jpg'

model = YOLO(path_to_model)

results = model.predict(path_to_img,
                        save=True,
                        project='results',
                        name='',
                        show=True,
                        conf=0.3)

# Подробный анализ результатов
for i, r in enumerate(results):
    print(f"\n=== Результат для изображения {i + 1} ===")
    print(f"Путь к изображению: {r.path}")
    print(f"Размер изображения: {r.orig_shape}")
    print(f"Классы модели: {r.names}")

    # Информация о bounding boxes
    boxes = r.boxes
    print(f"Обнаружено объектов: {len(boxes)}")

    if len(boxes) > 0:
        for j, box in enumerate(boxes):
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            coordinates = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            class_name = r.names[class_id]

            print(f"\nОбъект {j + 1}:")
            print(f"  Класс: {class_name} (ID: {class_id})")
            print(f"  Уверенность: {confidence:.3f * 100}%")
            print(
                f"  Координаты: x1={coordinates[0]:.1f}, y1={coordinates[1]:.1f}, x2={coordinates[2]:.1f}, y2={coordinates[3]:.1f}")
    else:
        print("Объекты не обнаружены!")

    print(f"Результаты сохранены в: {r.save_dir}")