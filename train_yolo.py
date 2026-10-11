import os
import torch
from ultralytics import YOLO

def train_yolo_classifier():
    base_dir = "/Users/tanmaykalra/jaundice_detection"
    dataset_dir = os.path.join(base_dir, "dataset")
    project_dir = os.path.join(base_dir, "runs")
    
    # Check device: Apple Silicon MPS, CUDA, or CPU
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        
    print(f"Using compute device: {device}")
    
    # Load YOLO classification pretrained backbone
    # yolov8n-cls is lightweight, fast, and highly accurate for 2-class medical image classification
    print("Loading YOLOv8-cls model...")
    model = YOLO("yolov8n-cls.pt")
    
    print("Beginning YOLO training on neonatal images...")
    results = model.train(
        data=dataset_dir,
        epochs=15,
        imgsz=224,
        batch=16,
        project=project_dir,
        name="jaundice_yolo_cls",
        device=device,
        exist_ok=True,
        workers=2,
        verbose=True
    )
    
    # Save the trained weights to a standard path for the Streamlit app
    best_weights = os.path.join(project_dir, "jaundice_yolo_cls", "weights", "best.pt")
    target_weights = os.path.join(base_dir, "models", "yolov8_jaundice_best.pt")
    os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
    
    if os.path.exists(best_weights):
        import shutil
        shutil.copy(best_weights, target_weights)
        print(f"Copied best model weights to {target_weights}")
    else:
        print(f"Notice: weights at {best_weights}")

    # Validate model on validation/test set
    metrics = model.val()
    print("Validation top1 accuracy:", getattr(metrics, 'top1', 'N/A'))

if __name__ == "__main__":
    train_yolo_classifier()
