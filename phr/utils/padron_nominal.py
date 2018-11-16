# coding=utf-8
import csv


def padron2014():
    with open('/home/cj/Documents/PadronNominal/padron_nominal_31122014/padron_nominal_31122014.csv', newline='',
              encoding='latin-1') as f:
        rows = csv.reader(f)
        for line in rows:
            print(line)
