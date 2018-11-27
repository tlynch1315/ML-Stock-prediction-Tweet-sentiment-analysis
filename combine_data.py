#!/usr/bin/env python3

import pandas
import glob

allFiles = glob.glob("data/clean/d*/*.txt")
frame = pandas.DataFrame()
list_ = []

for file in allFiles:
	df = pandas.read_csv(file, header=None, names=['followers', 'polarity', 'subjectivity', 'value'])
	list_.append(df)

frame = pandas.concat(list_)

frame.to_csv('.csv')