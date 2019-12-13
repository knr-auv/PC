import pickle
import time
import pandas as pd


def csv_to_pickle():
    plik = open("plik.dat", "wb")
    data = pd.read_csv('wynik.csv')
    for d in data.values:
        plik.write(pickle.dumps(d))


csv_to_pickle()
