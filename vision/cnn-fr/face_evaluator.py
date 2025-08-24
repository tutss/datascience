import random

import torch
from torch import nn
from torch import Tensor
import torch.nn.functional as F
from torch.utils.data import Subset, DataLoader
from collections import defaultdict

from face_dataset import SimpleFaceDataset


class FaceRecognitionEvaluator:

    def __init__(self, model: nn.Module, device='cpu'):
        self.model = model
        self.device = device
        self.model.eval()

    def extract_embeddings_with_labels(self, data_loader: DataLoader):
        """
        Extract embeddings and labels from a DataLoader.
        """
        embeddings = []
        labels = []

        print(f"Extracting embeddings from {len(data_loader.dataset)} images...")

        with torch.no_grad():
            for batch_idx, (batch_images, batch_labels) in enumerate(data_loader):
                batch_images = batch_images.to(self.device)

                batch_embeddings = self.model(batch_images)

                embeddings.append(batch_embeddings.cpu())
                labels.extend(batch_labels)  # batch_labels is a list of strings

                if (batch_idx + 1) % 10 == 0:
                    print(f"  Processed {batch_idx + 1}/{len(data_loader)} batches")

        embeddings = torch.cat(embeddings, dim=0)
        print(f"Extracted {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}")

        return embeddings, labels

    def compute_similarity_matrix(self, 
                                  query_embeddings: Tensor, 
                                  gallery_embeddings: Tensor, 
                                  metric='cosine'
                                  ):
        if metric == 'cosine':
            query_norm = F.normalize(query_embeddings, p=2, dim=1)
            gallery_norm = F.normalize(gallery_embeddings, p=2, dim=1)

            # Cosine similarity: higher = more similar
            similarities = torch.mm(query_norm, gallery_norm.T)

        elif metric == 'euclidean':
            # Negative squared distances (higher = more similar)
            query_norm = (query_embeddings ** 2).sum(dim=1, keepdim=True)
            gallery_norm = (gallery_embeddings ** 2).sum(dim=1, keepdim=False)
            squared_distances = query_norm + gallery_norm - 2 * torch.mm(query_embeddings, gallery_embeddings.T)

            # Convert negate so higher = more similar
            similarities = -squared_distances

        else:
            raise ValueError(f"Unknown metric: {metric}")

        return similarities

    def evaluate_recognition(self, 
                             gallery_loader: DataLoader, 
                             query_loader: DataLoader, 
                             k_values=[1, 5], 
                             metric='cosine'
                            ):
        gallery_embeddings, gallery_labels = self.extract_embeddings_with_labels(gallery_loader)
        query_embeddings, query_labels = self.extract_embeddings_with_labels(query_loader)

        print(f"\nGallery: {len(gallery_embeddings)} embeddings from {len(set(gallery_labels))} people")
        print(f"Query: {len(query_embeddings)} embeddings from {len(set(query_labels))} people")

        print(f"\nComputing {metric} similarities...")
        similarities = self.compute_similarity_matrix(query_embeddings, gallery_embeddings, metric)

        _, sorted_indices = torch.sort(similarities, dim=1, descending=True)

        results = {}
        total_queries = len(query_labels)

        print(f"\nEvaluating top-k accuracies...")
        for k in k_values:
            correct = 0

            for i, query_label in enumerate(query_labels):
                top_k_indices = sorted_indices[i, :k]

                predicted_labels = [gallery_labels[idx] for idx in top_k_indices]

                if query_label in predicted_labels:
                    correct += 1

            accuracy = correct / total_queries
            results[f'top_{k}_accuracy'] = accuracy

        return results
    
def split_dataset_for_evaluation(dataset: SimpleFaceDataset, gallery_images_per_person=2, random_seed=42):
    random.seed(random_seed)

    person_to_indices = defaultdict(list)
    for idx, (_, person_label) in enumerate(dataset.image_paths):
        person_to_indices[person_label].append(idx)

    gallery_indices = []
    query_indices = []

    print(f"Splitting dataset for evaluation:")
    print(f"Gallery images per person: {gallery_images_per_person}")

    for person, indices in person_to_indices.items():
        shuffled_indices = indices.copy()
        random.shuffle(shuffled_indices)

        if len(indices) < gallery_images_per_person + 1:
            print(f"Warning: {person} has only {len(indices)} images, skipping...")
            continue

        gallery_indices.extend(shuffled_indices[:gallery_images_per_person])
        query_indices.extend(shuffled_indices[gallery_images_per_person:])

    print(f"Gallery set: {len(gallery_indices)} images")
    print(f"Query set: {len(query_indices)} images")
    print(f"People in evaluation: {len(person_to_indices)} total")

    gallery_dataset = Subset(dataset, gallery_indices)
    query_dataset = Subset(dataset, query_indices)

    return gallery_dataset, query_dataset

def get_dataset_statistics(dataset_subset: SimpleFaceDataset):
    person_counts = defaultdict(int)

    for idx in dataset_subset.indices:
        _, person_label = dataset_subset.dataset.image_paths[idx]
        person_counts[person_label] += 1

    stats = {
        'total_images': len(dataset_subset),
        'total_people': len(person_counts),
        'images_per_person': dict(person_counts),
        'avg_images_per_person': sum(person_counts.values()) / len(person_counts)
    }

    return stats
