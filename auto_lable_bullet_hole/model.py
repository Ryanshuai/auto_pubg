import matplotlib.pyplot as plt
import numpy as np


def value(x, dx, a, x0):
    x = x - dx
    if x < 0:
        return 0
    if x > 0.9 * x0:
        x = 0.9 * x0
    y = -a * x * (x - x0)
    return y


def get_value(x):
    y = 0
    ddy = 0.3
    for i in range(30):
        y += value(x, ddy * i, 3, 1)
    return y


if __name__ == '__main__':
    xs = np.arange(0, 30, 0.01)
    ys = np.zeros_like(xs)
    for i, x in enumerate(xs):
        ys[i] = get_value(x)
    plt.plot(xs, ys)
    plt.show()
