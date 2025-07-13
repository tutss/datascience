
from typing import Tuple

import numpy as np

from torch.utils.data import Dataset


class MaskedCIFAR10(Dataset):
    def __init__(self, dataset: Dataset, mode="train") -> None:
        super(MaskedCIFAR10, self).__init__()
        self.data = dataset
        self.mode = mode
        self.mask_size = (15, 15)
        self.img_size = 32

    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index):
        img, _ = self.data[index]
        img = np.array(img)
        masked_img, mask = self.apply_mask(img)

        # print(f"Masked_img: {masked_img.shape}")
        # print(f"Image: {img.shape}")
        # print(f"Mask: {mask.shape}")

        return masked_img, img, mask
        
    def apply_mask(self, img) -> Tuple[np.array, np.array]:
        y1, x1 = np.random.randint(0, self.img_size - self.mask_size[0], 2)
        y2, x2 = y1 + self.mask_size[0], x1 + self.mask_size[0]
        
        # print(f"Image: {img.shape}")
        # print(f"Mask: y1={y1}, x1={x1}, y2={y2}, x2={x2}")
        masked_part = img[y1:y2, x1:x2, :]
        # print(f"Masked part shape = {masked_part.shape}")
        masked_img = img.copy()
        
        masked_img[y1:y2, x1:x2, :] = 255

        return masked_img, masked_part