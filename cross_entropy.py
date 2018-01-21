#!/usr/bin/env python

import numpy as np
from softmax import softmax

"""
TODO: Add regularization to compute the cost function
TODO: Understand if you have to divide the cross_entropy_gradient in linear and activation
TODO: Update cross_entropy_gradient in order to make adaptable for a deep neural network
TODO: Add regularization to the gradient
"""

def cross_entropy_loss(Z, y):
    """
    Arguments:
    Z -- numpy array of shape (n,m) on which apply the softmax
    y -- numpy array of shape (n,m) representing real output. n usually is 1 or
         it can be more than 1 in case of Word2Vec skip n-grams. m is the number of samples

    Return:
    L -- numpy array of shape (n,m) with the log probability assigned to the correct class

    """
    A, cache = softmax(Z)
    L = -np.log(A[np.arange(Z.shape[0]), np.argmax(y, axis=0)])
    L = L.reshape(y.shape[0], y.shape[1]) # To avoid (,m) issues

    assert y.shape == L.shape

    return L


def cross_entropy_cost(AL, y):
    """
    Arguments:
    AL -- numpy array of any (n,m) of predictions (softmax output)
    y -- numpy array of shape (n, m) representing real output. n usually is 1 or
         it can be more than 1 in case of Word2Vec skip n-grams. m is the number of samples

    Return:
    cost -- cost value equals to the average of the cross-entropy loss of each sample
    activation_cache -- numpy array of shape (n,m) generated by the softmax function useful for backpropagation
    """
    m = y.shape[1]
    L = cross_entropy_loss(AL, y)
    cost = np.sum(L)
    cost = np.squeeze(cost)

    assert(cost.shape == ())
    assert isinstance(cost, float)

    return cost


def cross_entropy_gradient(dA, cache, y):
    """
    Arguments:
    dA -- numpy array representing the activation output of the previous layer (X if the previous one is the first)
    cache -- numpy array of shape (m, n) generated by the softmax function
    y -- numpy array of shape (m,) representing real output. m is the number of samples

    Return:
    dW -- gradient of the cross entropy cost function in W
    db -- gradient of the cross entropy cost function in b
    """

    dscores = cache
    dscores[range(y.shape[0]),y] -= 1 # Gradient of cross_entropy applied to the softmax
    dscores /= y.shape[0]

    dW = np.dot(A.T, dscores)
    db = np.sum(dscores, axis=0, keepdims=True)

    assert A.shape[1] == dW.shape[0]
    assert dW.shape[1] == db.shape[1]

    return dW, db


def test_cross_entropy_and_its_gradient():
    print("Test cross entropy and its gradient...")

    Z = np.array([
            [200,700,40,30],
            [300,100,30,20],
            [500,200,30,50]])

    y = np.array([[0,0,0]]) # It must be a vector of dimension (m,)

    test1 = cross_entropy_loss(Z, y)
    print(test1)
    ans1 = np.array([[
                    300.0000000004685,
                    200,
                    0]])

    assert np.allclose(ans1, test1, rtol=1e-05, atol=1e-06)


    A, cache = softmax(Z)
    test2 = cross_entropy_cost(A, y)
    print(test2)
    ans2 = 1.05145914568

    assert np.allclose(ans2, test2, rtol=1e-05, atol=1e-06)

    """
    X = np.array([
                [1,2],
                [3,4],
                [5,6],
                [6,7]
                ])

    dW, db = cross_entropy_gradient(X, A, y)
    """

    print("... end test")


if __name__ == "__main__":
    test_cross_entropy_and_its_gradient()
