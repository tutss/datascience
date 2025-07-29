# Part-based Face Recognition with Vision Transformers

## Notes

- lightweight CNN (mobilenetv3) for set of facial landmarks
- grid sampling on the landmarks
- pass sampled landmarks to ViT
- ViT does recognition
- CosFace loss
- authors mention worse performance when training with small scale datasets such as CASIA-webface, even when using data augmentation strategies
- part fViT is better than baseline fViT on MS1M
- attention maps show that the baseline fViT lacks a couple of details, such as the eyes. only one of the heads pays attention to it, while part fViT has a few that take that into account

- uses non overlapping patches as in original ViT
- linear embedding layer
- learned positional embeddings
- MSA + MLP using classification tokens
- classification token is traned for face recognition using CosFace loss

## Questions

- it is not clear what the final output of the model is
- neither how the landmark cnn is jointly trained with the ViT