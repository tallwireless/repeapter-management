import sys
from csv import DictReader
from pprint import pprint as pp

a = DictReader(open(sys.argv[1]))
for i in a:
    j = i
pp(a.fieldnames)
pp(i)
