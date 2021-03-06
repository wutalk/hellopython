#! D:/owendir/programs/Python38/pythonw.exe
# digest demo
# from tkinter import Tk
import getpass
import hashlib
import sys
import time

import pyperclip


def digest(input_str, alg_method):
    h = hashlib.new(alg_method)
    h.update(input_str.encode('utf-8'))
    return h.hexdigest()


def upper_by(str, step):
    ori_list = list(str)
    new_list = []
    index = 0
    for ele in ori_list:
        if index % step == 0:
            new_list.append(ele.upper())
        else:
            new_list.append(ele)
        index += 1
    return ''.join(new_list)


if __name__ == "__main__":
    alg = 'sha1'
    if sys.argv.__len__() >= 2:
        alg = sys.argv[1]
    origin_text = getpass.getpass('Input: ')
    if sys.argv.__len__() >= 3:
        if sys.argv[2] == 'show':
            print(origin_text + ", " + alg)
    hashed = digest(origin_text, alg)
    hashed = upper_by(hashed, 3)
    # print(hashed)
    # copy to clipboard
    # r = Tk()
    # r.withdraw()
    # r.clipboard_clear()
    # r.clipboard_append(hashed)
    # r.destroy()
    pyperclip.copy(hashed)
    print('copied to clipboard')
    # waiting
    # print("Enter to exit")
    # raw_input()
    time.sleep(0.1)
    exit(0)
