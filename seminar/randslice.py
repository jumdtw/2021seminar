import pandas as pd
import csv 
import sys
import glob

# python3 randslice.py savefilename 

savefilename = "default.csv"
path = ".\\data\\buf"

files = glob.glob(path+"\\*")
print(files)
lst = []
for file in files:
    with open(file) as f:
        a = [e for e in csv.reader(f)]
        lst = lst + a
df = pd.DataFrame(lst)

if len(sys.argv)>1:
    savefilename = sys.argv[1]
    

print(df)
df.to_csv(".\\data\\"+savefilename)