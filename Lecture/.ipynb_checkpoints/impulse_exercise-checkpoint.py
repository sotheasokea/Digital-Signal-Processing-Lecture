import numpy as np
def ex4_1(x):
    x = np.array(x)
    y = 4*x
    return y

def ex4_2(x):
    x = np.array(x)
    y = 2*x + 2
    return y

def ex4_3(x):
    x = np.array(x)
    y = x - 8
    return y

def ex4_4(x):
    x = np.array(x)
    y = x**2
    return y

def ex4_5(x):
    x = np.array(x)
    n = np.arange(0, len(x))
    y = n * x
    return y

def ex4_6(x):
    x = np.array(x)
    y = np.zeros_like(x)

    for n in range(len(x)):
        x_n = x[n]
        x_n1 = x[n - 1] if n - 1 >= 0 else 0
        x_n2 = x[n - 2] if n - 2 >= 0 else 0
        y[n] = (x_n + x_n1 + x_n2) / 3

    return y