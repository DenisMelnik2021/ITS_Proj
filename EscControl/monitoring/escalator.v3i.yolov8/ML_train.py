from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('yolov8s.pt')

    results = model.train(
        data='./data.yaml',
        epochs=50,
        device='cuda',  # Использовать GPU
        batch=16,
        workers=4,
    )

    results = model.val()

    metrics = results
    print(metrics.box.map)  # mAP50-95
    print(metrics.box.map50)  # mAP50

    model.export(format='onnx')