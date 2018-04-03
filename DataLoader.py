import pandas as pd
from pandas.io.json import json_normalize
import os


os.chdir('c:\\users\\michael\\documents\\code\\pubg\\past trials data\\trial 7 31147 matches')


def load_match():
    for df in pd.read_csv('PUBG_MatchData.tsv', header=None, sep='\t', usecols=[0], chunksize=1000):
        yield df

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

a = pd.DataFrame()
#b = []
#c = []
for i, test in enumerate(load_match()):
    for j, thing in enumerate(test[0]):
        tempdata = eval(test[0][i*1000+j])
        tempdata = flatten_json(tempdata)
        a = a.append(json_normalize(tempdata))
#        a.append(json_normalize(tempdata))
#        b.append(json_normalize(data=tempdata), record_path='deaths')
#        c.append(json_normalize(data=tempdata), record_path=['deaths','killer'],['deaths','victim'])