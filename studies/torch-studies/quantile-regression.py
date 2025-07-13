import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


np.random.seed(1)


class QuantileLoss(nn.Module):
    def __init__(self, tau):
        super(QuantileLoss, self).__init__()
        self.tau = tau

    def forward(self, y_pred, y_true):
        return torch.mean(
            torch.maximum(
                self.tau * (y_true - y_pred), 
                (1 - self.tau) * (y_true - y_pred)
            )
        )


class QuantileRegression(nn.Module):

    def __init__(self, input_dim):
        super(QuantileRegression, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.model(x)


def main():
    n = 10000
    X = np.sort(np.random.uniform(-4, 4, n))
    y = 3 / (3 + 2 * np.abs(X)**3) + np.exp(-X**2) + np.cos(X) * np.sin(X) + np.random.normal(0, 0.3, n)

    X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
    y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    dataset = TensorDataset(X_tensor, y_tensor)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    epochs = 100
    input_dim = 1
    tau = .25  # quantile value

    model = QuantileRegression(input_dim=input_dim)
    qloss = QuantileLoss(tau=tau)
    optimizer = optim.AdamW(model.parameters(), lr=0.001)
    train_losses = list()
    val_losses = list()

    for e in range(epochs):
        print(f'======= Epoch = {e+1}/{epochs} =======')
        model.train()
        train_loss = 0.0
        for batch in train_loader:
            inputs, targets = batch
            inputs, targets = inputs.float(), targets.float()
            optimizer.zero_grad()
            
            y_pred = model(inputs).squeeze()
            loss = qloss(y_pred, targets)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        train_loss /= len(train_loader)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                inputs, targets = batch
                inputs, targets = inputs.float(), targets.float()
                y_pred = model(inputs).squeeze()
                loss = qloss(y_pred, targets)
                val_loss += loss.item()

        val_loss /= len(val_loader)

        train_losses.append(train_loss)
        val_losses.append(val_loss)

    plt.plot([i for i in range(epochs)], train_losses)
    plt.plot([i for i in range(epochs)], val_losses)
    plt.show()

main()