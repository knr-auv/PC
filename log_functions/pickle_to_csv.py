import pickle
import csv

plik = open("plik.dat", "rb")

def pickle_to_csv(plik):
    with open('wynik.csv', 'w', newline='') as csvfile:
        fieldnames = ['Motor0', 'Motor1', 'roll_offset', 'pitch_offset', 'vertical', 'dt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            try:
                tmp = pickle.load(plik)
                writer.writerow({'Motor0': tmp[0], 'Motor1': tmp[1], 'roll_offset': tmp[2],
                                 'pitch_offset': tmp[3], 'vertical': tmp[4], 'dt': tmp[5]})
                # print(tmp)
            except:
                break


pickle_to_csv(plik)
