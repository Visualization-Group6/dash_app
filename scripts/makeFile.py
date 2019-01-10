import gzip
import io
import numpy as np
import time
import os
import pandas as pd
from scripts import preProcessing
import io
import gzip


def make_oregon_file():
    files = ['oregon1_010331.txt.gz', 'oregon1_010407.txt.gz', 'oregon1_010414.txt.gz', 'oregon1_010421.txt.gz',
             'oregon1_010428.txt.gz', 'oregon1_010505.txt.gz', 'oregon1_010512.txt.gz', 'oregon1_010519.txt.gz',
             'oregon1_010526.txt.gz']
    f = open('Oregon.txt', 'w')
    f.write('Time Start Target Weight')
    f.write('\n\n')
    times = 1
    count = 0
    for n in range(0, len(files)):
        file = files[n]
        with gzip.open(file) as input_file:
            with io.TextIOWrapper(input_file, encoding='utf-8') as dec:
                output = dec.read()

        for line in output.split('\n')[4:4004]:
            res = [str(times)]
            line = line.split('\t')
            if len(line) == 2:
                for i in line:
                    res.append(i)
                res.append('1')
                res = ' '.join(res)
                res = res + '\n'
                f.write(res)
                count = count + 1
        # print(res)
        times += 7
    print('.txt file saved')
    f.close()
    return None


def csv_gz_to_txt(dataset):
    if '.'.join(dataset.split('.')[-2:]) != 'csv.gz':
        print('This is not the correct file extension.')
    if '.'.join(dataset.split('.')[-2:]) == 'csv.gz':
        print('csv.gz file!')
        data = pd.read_csv(preProcessing.get_working_dir() + str(dataset), compression='gzip', header=-1)
        data = data.rename(index=int, columns={0: "Start", 1: "Target", 2: 'Weight', 3: 'Time'})

        f = open(preProcessing.get_working_dir() + dataset.split('.')[0] + '.txt', 'w')
        f.write('Time Start Target Weight')
        f.write('\n\n')
        for i in range(len(data)):
            # print(data['Time'][i])
            res = [str(int(data['Time'][i])), str(data['Start'][i]), str(data['Target'][i]), str(data['Weight'][i])]
            res = ' '.join(res)
            res = res + '\n'
            f.write(res)
        print('.txt file saved')
        f.close()
        return None




def dat_gz_to_txt(dataset):
    print('dat_.gz file!')
    f = open(preProcessing.get_working_dir() + dataset.split('.')[0] + '.txt', 'w')
    f.write('Time Start Target Weight')
    f.write('\n\n')
    with gzip.open(preProcessing.get_working_dir() + str(dataset)) as input_file:
        with io.TextIOWrapper(input_file, encoding='utf-8') as dec:
            output = dec.read()
            for line in output.split('\n'):
                line = line.split(' ')
                if len(line) == 3:
                    line[0] = str(int((int(line[0]) - 32520)/10))
                    line.append('1') # all get weight 1
                    line = ' '.join(line)
                    line = line + '\n'
                    f.write(line)
    print('.txt file saved')
    f.close()
    return None