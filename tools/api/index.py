#!/usr/bin/env python3.6

import pandas, json, sys

csvfile = '/path/to/aikatsu8.csv'

def main():
    try:
        df = pandas.read_csv(csvfile, header=None)
    except FileNotFoundError:
        print('csvfile {} is not found'.format(csvfile))
        sys.exit()

    data     = df.values
    rankings = []
    for line in data:
        count = 0
        rank  = []
        name  = []
        for column in line:
            if count == 0: 
                count += 1
                ranks = {"datetime": line[0].rstrip(' 現在のランキング')}
                continue
            rank_name = column.split('位')
            rank.append(int(rank_name[0]))
            name.append(rank_name[1])
        array = dict(zip(name, rank))
        ranks.update(array)
        rankings.append(ranks)

    
    dat_datetime = []
    for i in rankings:
        dat_datetime.append(i['datetime'])
    dat_output = {'datetime': dat_datetime}

    for charname in name:
        array = ""
        dat_charname = []
        for i in rankings:
            dat_charname.append(i[charname])
        array = {charname: dat_charname}
        dat_output.update(array)
        
    return dat_output

def application(env, start_response):
    res = main()
    start_response('200 OK', [('Content-Type','application/json; charset=utf-8'), ('Cache-Control','public, max-age=1')])
    return [bytes(json.dumps(res), 'utf-8')]

if __name__ == '__main__':
    print(main())
