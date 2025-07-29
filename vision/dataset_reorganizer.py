import os
import shutil
import random
from pathlib import Path

def reorganize_dataset(dataset_path, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        raise ValueError(f"Dataset path {dataset_path} does not exist")
    
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError("Split ratios must sum to 1.0")
    
    person_folders = [f for f in dataset_path.iterdir() if f.is_dir() and not f.name.startswith('.')]
    
    if not person_folders:
        raise ValueError("No person folders found in dataset directory")
    
    random.seed(seed)
    random.shuffle(person_folders)
    
    n_total = len(person_folders)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    n_test = n_total - n_train - n_val
    
    splits = {
        'train': person_folders[:n_train],
        'val': person_folders[n_train:n_train + n_val],
        'test': person_folders[n_train + n_val:]
    }
    
    print(f"Dataset split: {n_train} train, {n_val} val, {n_test} test ({n_total} total)")
    
    for split_name, folders in splits.items():
        split_dir = dataset_path / split_name
        split_dir.mkdir(exist_ok=True)
        
        for person_folder in folders:
            dest_path = split_dir / person_folder.name
            shutil.move(str(person_folder), str(dest_path))
            print(f"Moved {person_folder.name} to {split_name}/")
    
    print(f"\nReorganization complete. New structure:")
    for split in ['train', 'val', 'test']:
        split_path = dataset_path / split
        if split_path.exists():
            count = len([f for f in split_path.iterdir() if f.is_dir()])
            print(f"  {split}/: {count} person folders")

if __name__ == "__main__":
    dataset_folder = '/Users/arturmagalhaes/Downloads/lfw/lfw_funneled'
    reorganize_dataset(dataset_folder, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
