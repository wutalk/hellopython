#! D:/owendir/programs/Python275/pythonw.exe
# digest demo
import hashlib
import getpass
import sys


def digest(input_str, alg_method):
    h = hashlib.new(alg_method)
    h.update(input_str)
    return h.hexdigest()


if __name__ == "__main__":
    alg = 'sha1'
    if sys.argv.__len__() >= 2:
        alg = sys.argv[1]
    origin_text = getpass.getpass('Input: ')
    if sys.argv.__len__() >= 3:
        if sys.argv[2] == 'show':
            print(origin_text + ", " + alg)
    print(digest(origin_text, alg))
