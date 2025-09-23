from ultralytics import YOLO
import os, json, time, requests
token = "28b15690b91e7f02bd97859661c88ed7703b3493"
def send_to_api(data, files):
    global token
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/yolo/incidents/report/',
            data=data,
            files = files,   # Автоматически сериализует в JSON
            headers={#'Content-Type': 'application/json',
            'Authorization': f'Token {token}'},
            timeout = 10
            )
        print(f'{response}--------------------')
        return response.json()
    except Exception as e:
        print(f"API Error: {e}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None


path_to_model = 'escalator.v3i.yolov8/runs/detect/train/weights/best.pt'
path_to_imgs = 'escalator.v3i.yolov8/train/images'
model = YOLO(path_to_model)
c = 0

for img in os.listdir(path_to_imgs):
    results = model.predict(f'{path_to_imgs}/{img}',
                            save=True,
                            project='EscControl/monitoring/',
                            show=False,
                            conf=0.3,
                            name="incident_screenshots",  # Важно: пустая строка
                            exist_ok=True)

    # Подробный анализ результатов
    for i, r in enumerate(results):
        # Информация о bounding boxes
        boxes = r.boxes
        print(f"Обнаружено объектов: {len(boxes)}")

        if len(boxes) > 0:
            for j, box in enumerate(boxes):
                class_id = int(box.cls[0])
                confidence_ml = float(box.conf[0])
                coordinates = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                class_name = r.names[class_id]

                if class_id == 1:
                    continue
                c+=1
                new_filename = f"incident_{c}.jpg"
                output_path = f'EscControl/monitoring/incident_screenshots/{new_filename}'
                r.save(filename=output_path)
                            
                for_api = {
                    "status" : "new",
                    "notes" : "fall",
                    "escalator" : 2,
                    "ts" : "2025-09-23T07:10:00Z",
                    "confidence" : float(f"{confidence_ml:.3f}"),
                    "incident_type" : 1
                    #"screenshot" : output_path
                    }
                with open(output_path, 'rb') as img_file:
                    files = {
                        'screenshot': (os.path.basename(output_path), img_file, 'application/octet-stream')
                        }
                    response = send_to_api(for_api, files)
                    print(response)

                break
            
            #time.sleep(10)