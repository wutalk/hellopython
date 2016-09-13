import py_compile
import sys

if __name__ == "__main__":
    if sys.argv.__len__() >= 2:
        path = sys.argv[1]
        py_compile.compile(path)
        print "compiled " + path
    else:
        print "no file to compile"
