# Siamese networks

- DeepFace was developed using siamese networks (https://ieeexplore.ieee.org/document/6909616)
- dimensionality reduction: reducing dimensions to a lower dimensional representation that preserves information about the input, such that distances between outputs vectors capture intended differences between inputs.
- siamese networks exemplify the use of contrastive loss, where the loss considers if two pairs are equal of different
- constrastive loss can be used for face verification tasks (e.g. "is this person #1?")
- facenet introduced the idea of triplet loss, where you compare positive and negative pairs with an anchor example