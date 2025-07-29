import torch.nn as nn
import torch.nn.functional as F


class FaceEmbeddingCNN(nn.Module):

    def __init__(self, embedding_dim=512):
        super(FaceEmbeddingCNN, self).__init__()

        self.embedding_dim = embedding_dim

        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(.3)

        self.fc1 = nn.Linear(256 * 14 * 14, 1024)
        self.fc2 = nn.Linear(1024, self.embedding_dim)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # conv1 (3→32, k=3, p=1) + pool(2,2): (batch, 32, 112, 112)
        x = self.pool(F.relu(self.conv2(x)))  # conv2 (32→64, k=3, p=1) + pool(2,2): (batch, 64, 56, 56) 
        x = self.pool(F.relu(self.conv3(x)))  # conv3 (64→128, k=3, p=1) + pool(2,2): (batch, 128, 28, 28)
        x = self.pool(F.relu(self.conv4(x)))  # conv4 (128→256, k=3, p=1) + pool(2,2): (batch, 256, 14, 14)

        x = x.view(-1, 256 * 14 * 14)  # (224 ÷ 2⁴ = 224 ÷ 16 = 14)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)

        embeddings = self.fc2(x)

        return F.normalize(embeddings, p=2, dim=1)