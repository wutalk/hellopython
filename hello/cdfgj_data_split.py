import codecs
import os.path

tmp_dir = 'D:/data/cdfgj-data/'
page = 'cdfgj_cj_2019-02-22.html'

if os.path.isfile(tmp_dir + page):
    print 'start split %s' % page
    out_file = tmp_dir + "cdfgj_cj_data.csv"
    with codecs.open(out_file, "r", "utf-8") as f:
        f.read_line()

