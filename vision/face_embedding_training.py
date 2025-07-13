import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import random
import os
from typing import Tuple, List
import matplotlib.pyplot as plt

class FaceEmbeddingCNN(nn.Module):
    
    def __init__(self, embedding_dim=512):
        super(FaceEmbeddingCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.3)
        
        self.fc1 = nn.Linear(256 * 14 * 14, 1024)
        self.fc2 = nn.Linear(1024, embedding_dim)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        
        x = x.view(-1, 256 * 14 * 14)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        embeddings = self.fc2(x)
        
        # L2 normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings

class TripletLoss(nn.Module):
    """
    Triplet Loss for face embedding training.
    Ensures anchor-positive distance < anchor-negative distance by margin.
    """
    def __init__(self, margin=0.5):
        super(TripletLoss, self).__init__()
        self.margin = margin
    
    def forward(self, anchor, positive, negative):
        # Calculate distances
        pos_distance = F.pairwise_distance(anchor, positive, p=2)
        neg_distance = F.pairwise_distance(anchor, negative, p=2)
        
        # Triplet loss: max(0, pos_dist - neg_dist + margin)
        loss = F.relu(pos_distance - neg_distance + self.margin)
        return loss.mean()

class FaceDataset(Dataset):
    """
    Dataset for triplet training.
    Each person should have multiple face images in separate folders.
    
    Directory structure:
    dataset/
    ├── person_001/
    │   ├── img1.jpg
    │   ├── img2.jpg
    │   └── img3.jpg
    ├── person_002/
    │   ├── img1.jpg
    │   └── img2.jpg
    └── ...
    """
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.person_to_images = {}
        self.all_persons = []
        
        # Build person -> images mapping
        for person_dir in os.listdir(data_dir):
            person_path = os.path.join(data_dir, person_dir)
            if os.path.isdir(person_path):
                images = [f for f in os.listdir(person_path) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if len(images) >= 2:  # Need at least 2 images per person
                    self.person_to_images[person_dir] = [
                        os.path.join(person_path, img) for img in images
                    ]
                    self.all_persons.append(person_dir)
        
        print(f"Loaded {len(self.all_persons)} persons with multiple images")
    
    def __len__(self):
        return len(self.all_persons) * 10  # Generate 10 triplets per person per epoch
    
    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # Select anchor person
        anchor_person = self.all_persons[idx % len(self.all_persons)]
        
        # Get two different images of the same person (anchor and positive)
        person_images = self.person_to_images[anchor_person]
        anchor_img_path, positive_img_path = random.sample(person_images, 2)
        
        # Get negative image from different person
        negative_person = random.choice([p for p in self.all_persons if p != anchor_person])
        negative_img_path = random.choice(self.person_to_images[negative_person])
        
        # Load and transform images
        anchor = self.load_image(anchor_img_path)
        positive = self.load_image(positive_img_path)
        negative = self.load_image(negative_img_path)
        
        return anchor, positive, negative
    
    def load_image(self, img_path: str) -> torch.Tensor:
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image

def create_data_transforms():
    """Create data augmentation transforms for training"""
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.RandomGrayscale(p=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])  # ImageNet stats
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def validate_model(model, val_loader, device):
    """
    Validate model by computing average triplet loss and accuracy.
    Accuracy = percentage of triplets where pos_dist < neg_dist
    """
    model.eval()
    total_loss = 0.0
    correct_triplets = 0
    total_triplets = 0
    
    triplet_loss_fn = TripletLoss(margin=0.5)
    
    with torch.no_grad():
        for batch_idx, (anchor, positive, negative) in enumerate(val_loader):
            anchor, positive, negative = anchor.to(device), positive.to(device), negative.to(device)
            
            # Get embeddings
            anchor_emb = model(anchor)
            positive_emb = model(positive)
            negative_emb = model(negative)
            
            # Calculate loss
            loss = triplet_loss_fn(anchor_emb, positive_emb, negative_emb)
            total_loss += loss.item()
            
            # Calculate accuracy (pos distance < neg distance)
            pos_dist = F.pairwise_distance(anchor_emb, positive_emb, p=2)
            neg_dist = F.pairwise_distance(anchor_emb, negative_emb, p=2)
            correct_triplets += (pos_dist < neg_dist).sum().item()
            total_triplets += anchor.size(0)
    
    avg_loss = total_loss / len(val_loader)
    accuracy = correct_triplets / total_triplets
    
    return avg_loss, accuracy

def train_face_embedding_model(
    train_data_dir: str,
    val_data_dir: str,
    num_epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    margin: float = 0.5,
    save_path: str = "face_embedding_model.pth"
):
    """Main training function"""
    
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")
    
    # Create transforms
    train_transform, val_transform = create_data_transforms()
    
    # Create datasets
    print("Loading datasets...")
    train_dataset = FaceDataset(train_data_dir, transform=train_transform)
    val_dataset = FaceDataset(val_data_dir, transform=val_transform)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, 
                             shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, 
                           shuffle=False, num_workers=4)
    
    # Initialize model, loss, and optimizer
    model = FaceEmbeddingCNN(embedding_dim=512).to(device)
    triplet_loss = TripletLoss(margin=margin)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.1)
    
    # Training history
    train_losses = []
    val_losses = []
    val_accuracies = []
    
    print(f"\nStarting training for {num_epochs} epochs...")
    print(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        epoch_loss = 0.0
        
        for batch_idx, (anchor, positive, negative) in enumerate(train_loader):
            anchor, positive, negative = anchor.to(device), positive.to(device), negative.to(device)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            anchor_emb = model(anchor)
            positive_emb = model(positive)
            negative_emb = model(negative)
            
            # Calculate loss
            loss = triplet_loss(anchor_emb, positive_emb, negative_emb)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            
            # Print progress
            if batch_idx % 50 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}/{len(train_loader)}, '
                      f'Loss: {loss.item():.4f}')
        
        # Validation phase
        val_loss, val_accuracy = validate_model(model, val_loader, device)
        
        # Update learning rate
        scheduler.step()
        
        # Record metrics
        avg_train_loss = epoch_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        
        print(f'Epoch {epoch+1}/{num_epochs} Summary:')
        print(f'  Train Loss: {avg_train_loss:.4f}')
        print(f'  Val Loss: {val_loss:.4f}')
        print(f'  Val Accuracy: {val_accuracy:.4f}')
        print(f'  Learning Rate: {scheduler.get_last_lr()[0]:.6f}')
        print('-' * 50)
        
        # Save best model
        if epoch == 0 or val_loss < min(val_losses[:-1]):
            torch.save(model.state_dict(), save_path)
            print(f"✅ New best model saved to {save_path}")
    
    print("Training completed!")
    
    # Plot training curves
    plot_training_curves(train_losses, val_losses, val_accuracies)
    
    return model, train_losses, val_losses, val_accuracies

def plot_training_curves(train_losses, val_losses, val_accuracies):
    """Plot training and validation metrics"""
    epochs = range(1, len(train_losses) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss curves
    ax1.plot(epochs, train_losses, 'b-', label='Training Loss')
    ax1.plot(epochs, val_losses, 'r-', label='Validation Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Accuracy curve
    ax2.plot(epochs, val_accuracies, 'g-', label='Validation Accuracy')
    ax2.set_title('Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_curves.png', dpi=300, bbox_inches='tight')
    plt.show()

# Example usage and configuration
if __name__ == "__main__":
    # Configuration
    config = {
        'train_data_dir': 'dataset/train',  # Path to training data
        'val_data_dir': 'dataset/val',      # Path to validation data
        'num_epochs': 50,
        'batch_size': 32,
        'learning_rate': 0.001,
        'margin': 0.5,
        'save_path': 'face_embedding_model.pth'
    }
    
    # Note: You need to prepare your dataset first
    print("=== Face Embedding Training Configuration ===")
    print("Dataset structure should be:")
    print("dataset/")
    print("├── train/")
    print("│   ├── person_001/")
    print("│   │   ├── img1.jpg")
    print("│   │   ├── img2.jpg")
    print("│   │   └── ...")
    print("│   ├── person_002/")
    print("│   └── ...")
    print("└── val/")
    print("    ├── person_101/")
    print("    └── ...")
    print()
    
    # Uncomment to start training (when you have the dataset ready)
    # model, train_losses, val_losses, val_accuracies = train_face_embedding_model(**config)
    
    print("Training script ready! Prepare your dataset and uncomment the training call.")
    
    # Load and test trained model
    def test_trained_model():
        """Example of how to load and test the trained model"""
        model = FaceEmbeddingCNN(embedding_dim=512)
        model.load_state_dict(torch.load('face_embedding_model.pth'))
        model.eval()
        
        # Test with random images
        with torch.no_grad():
            test_img1 = torch.randn(1, 3, 224, 224)
            test_img2 = torch.randn(1, 3, 224, 224)
            
            emb1 = model(test_img1)
            emb2 = model(test_img2)
            
            similarity = F.cosine_similarity(emb1, emb2)
            print(f"Embedding similarity: {similarity.item():.3f}")
    
    # test_trained_model()  # Uncomment after training