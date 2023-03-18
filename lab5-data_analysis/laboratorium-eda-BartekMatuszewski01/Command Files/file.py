import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import path
import rates


def age_statistics(df: pd.DataFrame):
    ages = df[["Wiek kupującego"]]
    output = ages.value_counts()
    k = output.keys()

    x = []
    y = []

    for it in k:
        x.append(it[0])

    x.sort()

    for it in x:
        y.append(output[it])

    return x, y


def gender_statistics(df: pd.DataFrame):
    ages = df[["Plec kupujacego"]]
    output = ages.value_counts()
    k = output.keys()

    x = []
    y = []

    for it in k:
        x.append(it[0])

    x.sort()

    for it in x:
        y.append(output[it])

    return x, y


def plot_data2(x, y, title, xlabel="wiek", ylabel="liczba osób"):
    plt.plot(x, y, color="green")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.show()


def plot_data3(x, y, title="", xlabel="płeć", ylabel="ilość osób"):
    plt.bar(x, y, color="green")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.show()

