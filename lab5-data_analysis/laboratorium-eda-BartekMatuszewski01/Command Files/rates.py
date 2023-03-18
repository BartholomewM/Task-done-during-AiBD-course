import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import path


def rates(df: pd.DataFrame):
    rates = df[["Ocena"]]
    output = rates.value_counts()
    k = output.keys()

    x = []
    y = []

    for it in k:
        x.append(it[0])

    x.sort()

    for it in x:
        y.append(output[it])

    return x, y


def plot_data(x, y, title, xlabel, ylabel):
    plt.bar(x, y,
            color="green",
            align="center",
            width=0.4
            )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.show()

