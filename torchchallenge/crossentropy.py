import numpy as np
from math import exp
# Write a function that takes as input a list of numbers, and returns
# the list of values given by the softmax function.
def softmax(L):
    sum_zi = 0
    for elem in L:
        sum_zi += exp(elem)
    softmax_zis = []
    for elem in L:
        e_zi = exp(elem)/sum_zi
        softmax_zis.append(e_zi)
    return softmax_zis