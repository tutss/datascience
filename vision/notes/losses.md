# Ranking losses ([ref](https://gombru.github.io/2019/04/03/ranking_loss/))

Ranking loss, margin loss, contrastive loss, triplet loss and hinge loss have similar formulations but kind of used in different contexts with some nuances.

## TODOs

- implement the losses on Pytorch
- see CosFace, ArcFace, L-softmax

## Pairwise

- objective is to predict relative distances between inputs, also called **metric learning**
- reduce distance between positive pairs, increase distance between negative pairs
- there's a margin for negative pair. when datapoint is outside the margin, we penalize by its value $m$:

$$
L = \begin{cases}
d(r_a, r_n) & \text{if } positive \\
\max(0, m - d(r_a, r_n)) & \text{if } negative
\end{cases}
$$

## Triplet loss

- differently from the pairwise loss, this method uses the triplet all at once when calculating the distances
- selecting the correct triplets and negative examples is key for the network to update the weights properly. There's 2 terms related to this: **negative selection** and **triplet mining**. It can be done during or before batch selection in training

$$
L(r_a, r_p, r_n) = \max(0, m + d(r_a, r_p) - d(r_a, r_n))
$$

1. if distance between anchor and negative is bigger than positive and anchor + margin, that means negative is already distant enough, so loss is not updated
2. if the distance between positive (+ margin) is bigger than the negative, we need to update the weights to reduce the distance from positive and anchor

### Visual

<iframe src="triplet_loss_visualization.html" width="100%" height="800" frameborder="0"></iframe>


## CosFace


## ArcFace

## SphereFace2

## Further reading

- https://omoindrot.github.io/triplet-loss