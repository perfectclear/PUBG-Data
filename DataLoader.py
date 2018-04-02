import pandas as pd
from pandas.io.json import json_normalize
import os


os.chdir('c:\\users\\michael\\documents\\code\\pubg\\past trials data\\trial 7 31147 matches')


def load_match():
    for df in pd.read_csv('PUBG_MatchData.tsv', header=None, sep='\t', usecols=[0], chunksize=1000):
        yield df
a = []
b = []
for i, test in enumerate(load_match()):
    for j, thing in enumerate(test[0]):
        a.append(json_normalize(eval(test[0][i*1000+j])))
        b.append(json_normalize(data=eval(test[0][i*1000+j]), record_path='deaths'))