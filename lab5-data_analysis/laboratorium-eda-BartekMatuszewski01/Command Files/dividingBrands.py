import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def divider(filePath: str = "../Analysis Data/malopolski_copy.csv", savePath="../Analysis Data/futher changes"):
    df = pd.read_csv(filePath)
    brands = set(df.Marka)

    for brand in brands:
        x = df[df["Marka"] == brand]
        x.drop(columns="Unnamed: 0")
        x.to_csv(savePath + f"/{brand}.csv")


# divider()
