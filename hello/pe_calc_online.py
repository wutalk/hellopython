import numpy as np
import pandas as pd
import bisect
from datetime import timedelta


def get_index_fundamentals(code, date):
    stocks = get_index_stocks(code, date)
    #     if(stocks.count(u'300498.XSHE') > 0):
    #         stocks.remove(u'300498.XSHE') # exclude wensi gufen
    q = query(valuation).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date)
    return df


# 计算方法2：理论平均市盈率=该类股票中总股本的总市值/这些股票产出的税后利润
def get_index_avg_pe_by_date(df):
    sum_p = 0
    sum_e = 0
    for i in range(0, len(df)):
        sum_p = sum_p + df['market_cap'][i]
        sum_e = sum_e + df['market_cap'][i] / df['pe_ratio'][i]
    if sum_e > 0:
        pe2 = sum_p / sum_e
    else:
        pe2 = float('NaN')
    return pe2


# 计算方法5：等权重，每支股票市值为1，剔除了PE为负的股票
def get_index_avg_pe_by_date_eq(df):
    pe_plus_num = 0
    sum_e = 0
    for i in range(0, len(df)):
        pe_i = df['pe_ratio'][i]
        if pe_i >= 0:
            pe_plus_num += 1
            sum_e += 1.0 / pe_i
    if sum_e > 0:
        pe5 = pe_plus_num / sum_e
    else:
        pe5 = float('NaN')
    return pe5


def get_index_avg_pb_by_date(index_code, date):
    df = get_index_fundamentals(index_code, date)
    sum_p = 0
    sum_e = 0
    for i in range(0, len(df)):
        sum_p = sum_p + df['market_cap'][i]
        sum_e = sum_e + df['market_cap'][i] / df['pb_ratio'][i]
    if sum_e > 0:
        pe2 = sum_p / sum_e
    else:
        pe2 = float('NaN')
    return pe2


# 指数历史PE,PB
def get_index_history_pe_pb(index_code, start, end):
    dates = []
    pes = []
    pes_eq = []
    pbs = []
    for d in pd.date_range(start, end, freq='M'):  # 频率： M 每月, W-FRI 每周五
        dates.append(d)
        df = get_index_fundamentals(index_code, d)
        pes.append(get_index_avg_pe_by_date(df))
        pes_eq.append(get_index_avg_pe_by_date_eq(df))
    # pbs.append(get_index_avg_pb_by_date(index_code,d))
    d = {'PE': pd.Series(pes, index=dates), 'PE_EQ': pd.Series(pes_eq, index=dates)}
    PB_PE = pd.DataFrame(d)
    return PB_PE


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


today = pd.datetime.today()
# today= '2015-06-01'
td = timedelta(days=365 * 10)
start = today - td

index_choose = ['000016.XSHG', '000015.XSHG', '000922.XSHG', '000925.XSHG', '000300.XSHG', '000905.XSHG', '399006.XSHE','000932.XSHG']
# index_choose = ['000015.XSHG']
all_index = get_all_securities(['index'])
df_pe_pb = pd.DataFrame()
frames = pd.DataFrame()
columns=[u'名称',u'当前估值',u'5年百分位%', u'10年分位点%',u'最小估值']+['%d%%'% (i*10) for i in range(1,10)]+[u'最大估值' , u"数据个数"]
# columns = [u'名称', u'当前', u'5年百分位%', u'10年百分位%', u'10年最小'] + [u'10年最大', u"数据个数"]
pe_results = []
for code in index_choose:
    index_name = all_index.ix[code].display_name
    print u'正在处理: ', index_name
    df_pe_pb = get_index_history_pe_pb(code, start, today)

    pe_list = df_pe_pb['PE']
    print "pe"
#     print pe_list
    pe_latest_half = pe_list[len(pe_list) / 2:]

    results = []
    df = get_index_fundamentals(code, today)
    pe = get_index_avg_pe_by_date(df)

    quantile_pe = calc_quantile(pe_list, pe)
    quantile = quantile_pe[0]
    q_pes = quantile_pe[1]
    quantile_half = calc_quantile(pe_latest_half, pe)[0]

    item = [index_name, '%.2f'% pe, '%.2f' % (quantile_half * 10), '%.2f'% (quantile*10)] \
            + ['%.2f'%q  for q in q_pes]+[df_pe_pb['PE'].count()]
#     item = [index_name, '%.2f' % pe, '%.2f' % (quantile_half * 10), '%.2f' % (quantile * 10)] \
#            + ['%.2f' % q_pes[0], '%.2f' % q_pes[len(q_pes) - 1]] + [pe_list.count()]
    results.append(item)
    pe_results.append(item)

    # pe eq
    pe_eq_list = df_pe_pb['PE_EQ']
    print "pe eq"
#     print pe_eq_list
    pe_eq_latest_half = pe_eq_list[len(pe_eq_list) / 2:]
    pe_eq = get_index_avg_pe_by_date_eq(df)

    quantile_pe_eq = calc_quantile(pe_eq_list, pe_eq)
    quantile_eq = quantile_pe_eq[0]
    q_pes_eq = quantile_pe_eq[1]
    quantile_eq_half = calc_quantile(pe_eq_latest_half, pe_eq)[0]

    item = [index_name, '%.2f'% pe_eq, '%.2f' % (quantile_eq_half * 10), '%.2f'% (quantile_eq*10)] \
            + ['%.2f'%q  for q in q_pes_eq]+[pe_eq_list.count()]
#     item = [index_name, '%.2f' % pe_eq, '%.2f' % (quantile_eq_half * 10), '%.2f' % (quantile_eq * 10)] \
#            + ['%.2f' % q_pes_eq[0], '%.2f' % q_pes_eq[len(q_pes_eq) - 1]] + [pe_eq_list.count()]
    results.append(item)
    pe_results.append(item)

    #    df= pd.DataFrame(data=results,index=['PE','PB'],columns=columns)
    df = pd.DataFrame(data=results, index=['PE', 'PE_EQ'], columns=columns)
    frames = pd.concat([frames, df])

date_str = u'统计区间: ' + start.strftime('%Y-%m-%d') + ' ~ ' + today.strftime('%Y-%m-%d')

print date_str
print ', '.join(columns)
for item in pe_results:
    line = [str(a) for a in item]
    print ', '.join(line)
# end

print date_str
frames
