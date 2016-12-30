import bisect
import pandas as pd

df_pe = pd.read_csv('D:/owu/PycharmProjects/hellopython/hello/test_data.csv', header=0)
results = []

pe_list = df_pe["HSCEI PE"]
# print pe_list
print 'min:', pe_list.quantile(0)
print 'max:', pe_list.quantile(1)

qpes = [pe_list.quantile(i / 10.0) for i in range(11)]
print 'qpes: ', qpes
pe = 15
idx = bisect.bisect(qpes, pe)
print 'pe: ', pe, ', idx: ', idx
if (idx == 0):
    quantile = 0
elif (idx == 11):
    quantile = 10
else:
    quantile = idx - (qpes[idx] - pe) / (qpes[idx] - qpes[idx - 1])
print 'quantile', quantile
