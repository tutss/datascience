import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.functional import relu
from torch.utils.data import DataLoader


from constants import EPOCHS, MODEL_PATH, DEVICE


class VariationalAutoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(VariationalAutoencoder, self).__init__()
        self.encoder = VariationalEncoder(latent_dims)
        self.decoder = Decoder(latent_dims)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)


class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims, channels=3):
        super(VariationalEncoder, self).__init__()
        self.convs = nn.Sequential(
            nn.Conv2d(channels, 32, kernel_size=3),
            nn.BatchNorm2d(32), 
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 32, kernel_size=3),
            nn.BatchNorm2d(32), 
            nn.LeakyReLU(0.2, inplace=True)
        )

        self.mean = nn.Linear(1024, latent_dims)
        self.var = nn.Linear(1024, latent_dims)

        self.N = torch.distributions.Normal(0, 1)
        self.N.loc = self.N.loc.cuda() # hack to get sampling on the GPU
        self.N.scale = self.N.scale.cuda()
        self.kl = 0

    def forward(self, x):
        x = torch.permute(x, (0, 3, 1, 2))
        print(f"Encoder Input shape = {x.shape}")
        x = self.convs(x)
        x = torch.flatten(x)
        print(f"X shape after flattening = {x.shape}")

        mean = self.mean(x)
        var = torch.exp(self.var(x))

        z = mean + var*self.N.sample(mean.shape)
        self.kl = (var**2 + mean**2 - torch.log(var) - 1/2).sum()

        return z


class Decoder(nn.Module):
    def __init__(self, latent_dims, channels=3):
        super(Decoder, self).__init__()
        self.linear1 = nn.Linear(latent_dims, 512)
        self.linear2 = nn.Linear(512, 1024)

        self.convs = nn.Sequential(
            nn.ConvTranspose2d(channels, 64, kernel_size=4),
            nn.BatchNorm2d(64), 
            nn.LeakyReLU(0.2, inplace=True),
            nn.ConvTranspose2d(64, 64, kernel_size=4),
            nn.BatchNorm2d(64), 
            nn.LeakyReLU(0.2, inplace=True),
            nn.ConvTranspose2d(64, channels, kernel_size=1)
        )

    def forward(self, x):
        print(f"Decoder Input shape = {x.shape}")
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.convs(x.reshape(-1, 64, 1, 1))
        return torch.sigmoid(x).reshape(-1, 3, 32, 32)
    

def train(model: VariationalAutoencoder,
          optimizer: torch.optim.Optimizer,
          train_loader: DataLoader,
          val_loader: DataLoader,
          epochs=EPOCHS,
          evaluate=False,
          device=DEVICE) -> None:
    """Trains model using criterion and optimizer. Data is loaded from trainloader

    Args:
        model (VariationalAutoencoder): Autoencoder model
        optimizer (torch.optim.Optimizer): optimizer
        trainloader (DataLoader): dataloader to train the model
        epochs (int, optional): number of epochs to train the model. Defaults to 20.
        evaluate (bool, optional): whether to evaluate the model. Defaults to False.
        device (str, optional): device to train the model. Defaults to 'cuda'.
    
    Returns:
        None. Saves model weights to MODEL_PATH.
    """
    train_avg_losses, val_avg_losses = list(), list()
    print("Starting training stage...")
    for e in range(1, epochs+1):
        model.train()

        # train step
        print(f"Epoch {e}...")
        train_avg_loss = 0
        for i, data in enumerate(train_loader, 0):
            inputs, imgs, _ = data
            inputs = inputs.to(device, dtype=torch.float32)
            imgs = imgs.to(device, dtype=torch.float32)
            optimizer.zero_grad()

            outputs = model(inputs)
            loss = F.mse_loss(outputs, imgs) + model.encoder.kl
            train_avg_loss += loss.detach().item()

            loss.backward()
            optimizer.step()

            if i % 2 == 0:
                print(f'[Epoch={e+1}, Iteration={i+1}] train loss: {loss.item():.3f}')
        
        train_avg_loss /= i
        
        # eval step
        if evaluate:
            print("Starting evaluation stage...")
            model.eval()
            eval_avg_loss = 0
            with torch.no_grad():
                for i, data in enumerate(val_loader, 0):
                    inputs, labels = data
                    inputs = inputs.to(device, dtype=torch.float32)
                    labels = labels.to(device, dtype=torch.float32)

                    outputs = model(inputs)
                    loss = F.mse_loss(outputs, imgs) + model.encoder.kl
                    eval_avg_loss += loss.detach().item()

                    if i % 2 == 0:
                        print(f'[Epoch={e+1}, Iteration={i+1}] test loss: {loss.item():.3f}')

            eval_avg_loss /= i

        train_avg_losses.append(train_avg_loss)
        val_avg_losses.append(eval_avg_loss)

    torch.save(model.state_dict(), MODEL_PATH)
    print(f'[Epoch={e+1}] model saved')

    return train_avg_losses, val_avg_losses