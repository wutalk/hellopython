# -*- coding: utf-8 -*-
import sys, getopt
import bisect
import pandas as pd
import time

today = time.strftime("%Y-%m-%d")
print today

df_pe = pd.read_csv('hscei-hsi-10-year-history-pe.csv', header=0)
results = []


def calc_quantile(pe_list, pe):
    q_pes = [pe_list.quantile(i / 10.0) for i in range(11)]
    idx = bisect.bisect(q_pes, pe)
    if (idx == 0):
        print 'history lowest'
        quantile = 0
    elif (idx == 11):
        print 'history highest'
        quantile = 10
    else:
        quantile = idx - (q_pes[idx] - pe) / (q_pes[idx] - q_pes[idx - 1])
    return quantile, q_pes


def calc_percent(col_name, pe):
    pe_list = df_pe[col_name]
    pe_latest_half = pe_list[len(pe_list) / 2:]

    quantile_pe = calc_quantile(pe_list, pe)
    quantile = quantile_pe[0]
    q_pes = quantile_pe[1]
    quantile_half = calc_quantile(pe_latest_half, pe)[0]

    line = [col_name, '%.2f' % pe, '%.2f' % (quantile_half * 10), '%.2f' % (quantile * 10)] \
           + ['%.2f' % q_pes[0], '%.2f' % q_pes[len(q_pes) - 1]] + [pe_list.count()]
    sline = [str(a) for a in line]
    print ', '.join(sline)
    results.append(line)


columns = ['Index Name', 'Current', '5 year %', '10 year %', '10y min', '10y max', 'data count']
# df = pd.DataFrame(data=results, columns=columns)
# frames = pd.DataFrame()
# frames = pd.concat([frames, df])

# print frames
print ', '.join(columns)

if __name__ == "__main__":
    # 2016-12-30
    hsi_pe = 13.63
    hscei_pe = 8.45
    if sys.argv.__len__() >= 3:
        hsi_pe = float(sys.argv[1])
        hscei_pe = float(sys.argv[2])
    # print 'main'
    calc_percent('HSI', hsi_pe)
    calc_percent('HSCEI', hscei_pe)
