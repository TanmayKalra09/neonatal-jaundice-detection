import os
import shutil
import zipfile
import random

def prepare_yolo_dataset():
    base_dir = "/Users/tanmaykalra/jaundice_detection"
    raw_njn = os.path.join(base_dir, "raw_data", "NJN")
    jaundice_zip = os.path.join(raw_njn, "jaundice.zip")
    normal_zip = os.path.join(raw_njn, "normal.zip")
    
    dataset_dir = os.path.join(base_dir, "dataset")
    train_jaundice = os.path.join(dataset_dir, "train", "jaundice")
    train_normal = os.path.join(dataset_dir, "train", "normal")
    val_jaundice = os.path.join(dataset_dir, "val", "jaundice")
    val_normal = os.path.join(dataset_dir, "val", "normal")
    test_jaundice = os.path.join(dataset_dir, "test", "jaundice")
    test_normal = os.path.join(dataset_dir, "test", "normal")
    
    for d in [train_jaundice, train_normal, val_jaundice, val_normal, test_jaundice, test_normal]:
        os.makedirs(d, exist_ok=True)
        
    temp_extract = os.path.join(base_dir, "temp_images")
    os.makedirs(temp_extract, exist_ok=True)
    
    print("Extracting jaundice.zip...")
    with zipfile.ZipFile(jaundice_zip, 'r') as zf:
        zf.extractall(temp_extract)
        
    print("Extracting normal.zip...")
    with zipfile.ZipFile(normal_zip, 'r') as zf:
        zf.extractall(temp_extract)
        
    jaundice_src = os.path.join(temp_extract, "jaundice")
    normal_src = os.path.join(temp_extract, "normal")
    
    jaundice_imgs = [os.path.join(jaundice_src, f) for f in os.listdir(jaundice_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    normal_imgs = [os.path.join(normal_src, f) for f in os.listdir(normal_src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(jaundice_imgs)} jaundice images, {len(normal_imgs)} normal images.")
    
    random.seed(42)
    random.shuffle(jaundice_imgs)
    random.shuffle(normal_imgs)
    
    # 80% train, 10% val, 10% test
    def split_and_copy(imgs, train_dest, val_dest, test_dest):
        n = len(imgs)
        n_train = int(n * 0.8)
        n_val = int(n * 0.1)
        
        train_files = imgs[:n_train]
        val_files = imgs[n_train:n_train+n_val]
        test_files = imgs[n_train+n_val:]
        
        for f in train_files:
            shutil.copy(f, train_dest)
        for f in val_files:
            shutil.copy(f, val_dest)
        for f in test_files:
            shutil.copy(f, test_dest)
            
        print(f"Copied {len(train_files)} to train, {len(val_files)} to val, {len(test_files)} to test.")
        
    print("Distributing jaundice images...")
    split_and_copy(jaundice_imgs, train_jaundice, val_jaundice, test_jaundice)
    
    print("Distributing normal images...")
    split_and_copy(normal_imgs, train_normal, val_normal, test_normal)
    
    # Clean up temp
    shutil.rmtree(temp_extract, ignore_errors=True)
    print("Dataset setup completed successfully!")

if __name__ == "__main__":
    prepare_yolo_dataset()
