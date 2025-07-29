import torch
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter


class FaceEmbeddingTrainer:

    def __init__(self, model, train_loader, val_loader, loss, device='cpu', log_dir='runs/face_embedding'):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.loss = loss
        self.writer = SummaryWriter(log_dir)
        self.global_step = 0
        self.device = device

    def train_epoch(self,
            optimizer,
            epoch: int
        ):
        self.model.train()
        epoch_loss = 0.0

        print(f'Size of train loader dataset = {len(self.train_loader.dataset)}')

        print('Started training epoch...')
        for batch_idx, (anchor, positive, negative) in enumerate(self.train_loader):
            print(f'Loading batch {batch_idx}')
            
            anchor, positive, negative = anchor.to(self.device), positive.to(self.device), negative.to(self.device)

            optimizer.zero_grad()

            anchor_emb = self.model(anchor)
            positive_emb = self.model(positive)
            negative_emb = self.model(negative)

            _loss = self.loss(anchor_emb, positive_emb, negative_emb)

            _loss.backward()
            optimizer.step()

            epoch_loss += _loss.item()

            if batch_idx % 100 == 0:
                self.writer.add_scalar('Loss/Train_Batch', _loss.item(), self.global_step)
                self.writer.add_scalar('Learning_Rate', optimizer.param_groups[0]['lr'], self.global_step)
            
            self.global_step += 1
        
        print('Finished training epoch...')
        avg_loss = epoch_loss / len(self.train_loader)
        self.writer.add_scalar('Loss/Train_Epoch', avg_loss, epoch)
        return avg_loss
    
    def validate(self, epoch):
        self.model.eval()
        val_loss = 0.0
        correct_triplets = 0
        total_triplets = 0

        print(f'Size of val loader dataset = {len(self.val_loader.dataset)}')

        print('Starting validation step...')
        with torch.no_grad():
            for batch_idx, (anchor, positive, negative) in enumerate(self.val_loader):
                print(f'Loading batch {batch_idx}')
                
                anchor, positive, negative = anchor.to(self.device), positive.to(self.device), negative.to(self.device)

                anchor_emb = self.model(anchor)
                positive_emb = self.model(positive)
                negative_emb = self.model(negative)
                
                _loss = self.loss(anchor_emb, positive_emb, negative_emb)
                val_loss += _loss.item()

                pos_dist = F.pairwise_distance(anchor_emb, positive_emb, p=2)
                neg_dist = F.pairwise_distance(anchor_emb, negative_emb, p=2)
                
                correct_triplets += (pos_dist < neg_dist).sum().item()
                total_triplets += anchor.size(0)
        
        print('Finished validation step...')
        avg_val_loss = val_loss / len(self.val_loader)
        self.writer.add_scalar('Loss/Validation', avg_val_loss, epoch)

        accuracy = correct_triplets / total_triplets
        self.writer.add_scalar('Accuracy/Validation', accuracy, epoch)
    
        return avg_val_loss, accuracy