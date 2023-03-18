import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import patsy as pat
import sklearn.linear_model as sk_lmod
import sklearn.model_selection as sk_mod_sel
import sklearn.metrics as sk_metrics


def print_descritpion(df: pd.DataFrame) -> None:
    print("data frame ")
    print(df)
    print()

    print("Użycie metody head:")
    print(df.head())
    print()

    print("Użycie metody describe:")
    print(df.describe())
    print()

    print("Kształt tablicy:")
    print(df.shape)
    print()


def print_model(str_data: str, predictor_name: str, output_data_name: str) -> None:
    data = pd.read_csv(os.path.join(str_data))

    print_descritpion(data)
    predictor = data[f"{predictor_name}"]
    output_data = data[f"{output_data_name}"]

    plt.scatter(predictor, output_data)
    plt.xlabel(f"{predictor_name}")
    plt.ylabel(f"{output_data_name}")
    plt.title("Wstępny wykres danych")
    plt.grid()
    plt.show()

    X = predictor
    y = output_data
    X_train, X_test, y_train, y_test = sk_mod_sel.train_test_split(X, y, train_size=0.3)

    X_train = np.array(X_train).reshape(-1, 1)
    y_train = np.array(y_train)

    X_test = np.array(np.array(X_test)).reshape(-1, 1)
    y_test = np.array(y_test)

    model = sk_lmod.LinearRegression().fit(X_train, y_train)
    coef_str = model.coef_[0]
    intercept_str = model.intercept_

    print("wyliczone wskaźniki dla modelu: coef_ :")
    print(coef_str)
    print("oraz intercept_ :")
    print(intercept_str)

    out = model.predict(X_test)

    plt.plot(X_test, out)
    plt.scatter(X_test, y_test)
    plt.grid()

    plt.show()

    print(f"Średni błąd bezwzględny: {sk_metrics.mean_absolute_error(y_test, out)}")
    print(f"Pierwiastek błędu średniokwadratowego: {sk_metrics.mean_squared_error(y_test, out, squared=False)}")
    print(f"Błąd średniokwadratowy: {sk_metrics.mean_squared_error(y_test, out)}")
