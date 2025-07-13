import matplotlib.pyplot as plt
from torch import randint
import numpy as np


def plot_image(dataset) -> None:
    fig, axs = plt.subplots(3, 3, figsize=(5, 5))

    for i in range(3):
        sample_idx = randint(len(dataset), size=(1,)).item()
        masked_img, img, mask = dataset[sample_idx]

        axs[i, 0].imshow(img)
        axs[i, 0].axis("off")
        axs[i, 0].set_title("Original Image")

        axs[i, 1].imshow(masked_img, cmap="gray")
        axs[i, 1].axis("off")
        axs[i, 1].set_title("Masked image")

        axs[i, 2].imshow(mask)
        axs[i, 2].axis("off")
        axs[i, 2].set_title("Mask")