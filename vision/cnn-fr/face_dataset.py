import os
import random
from PIL import Image

import torch
from torch.utils.data import Dataset

from torchvision import transforms


class FaceDataset(Dataset):
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.person_to_images = {}
        self.all_persons = []

        for person_dir in os.listdir(data_dir):
            person_path = os.path.join(data_dir, person_dir)
            if os.path.isdir(person_path):
                images = [img for img in os.listdir(person_path)
                          if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if len(images) >= 2: # needs anchor, positive and negative
                    self.person_to_images[person_dir] = [
                        os.path.join(person_path, img) for img in images
                    ]
                    self.all_persons.append(person_dir)
        
        print(f'Loaded {len(self.all_persons)} total people (with >= 2 photos)')
    
    def __len__(self):
        return len(self.all_persons)
    
    def __getitem__(self, idx):
        anchor_person = self.all_persons[idx % len(self.all_persons)]

        images = self.person_to_images[anchor_person]
        anchor_img_path, positive_img_path = random.sample(images, 2)

        negative_person = random.choice(
            [p for p in self.all_persons if p != anchor_person]
        )
        negative_img_path = random.choice(self.person_to_images[negative_person])

        anchor = self.load_image(anchor_img_path)
        positive = self.load_image(positive_img_path)
        negative = self.load_image(negative_img_path)

        return anchor, positive, negative
    
    def get_person_images(self, person_name: str):
        return self.person_to_images[person_name]
    
    def get_person_name(self, idx):
        return self.all_persons[idx % len(self.all_persons)]
    
    def load_image(self, img_path: str) -> torch.Tensor:
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        else:
            transform = transforms.ToTensor()
            image = transform(image)
        return image
    

class SimpleFaceDataset(Dataset):

    def __init__(self, data_dir: str, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.image_paths = []  # List of (image_path, person_label)

        for person_dir in os.listdir(data_dir):
            person_path = os.path.join(data_dir, person_dir)
            if os.path.isdir(person_path):
                images = [img for img in os.listdir(person_path)
                        if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

                for img in images:
                    img_path = os.path.join(person_path, img)
                    self.image_paths.append((img_path, person_dir))

        print(f'Loaded {len(self.image_paths)} images from {len(set(label for _, label in self.image_paths))} people')

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path, person_label = self.image_paths[idx]
        image = self.load_image(img_path)
        return image, person_label

    def load_image(self, img_path: str) -> torch.Tensor:
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        else:
            transform = transforms.ToTensor()
            image = transform(image)
        return image