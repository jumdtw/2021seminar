import pandas as pd
import csv 
import sys
import glob

# python randslice.py savefilename 

HEADER = [
    "Duration",
    "Service",
    "Source bytes",
    "Destination bytes",
    "Count",
    "Same_srv_rate",
    "Serror_rate",
    "Srv_serror_rate",
    "Dst_host_count",
    "Dst_host_srv_count",
    "Dst_host_same_src_port_rate",
    "Dst_host_serror_rate",
    "Dst_host_srv_serror_rate",
    "Flag",
    "IDS_detection",
    "Malware_detection",
    "Ashula_detection",
    "Label",
    "Source_IP_Address",
    "Source_Port_Number",
    "Destination_IP_Address",
    "Destination_Port_Number",
    "Start_Time",
    "Protocol"
]

savefilename = "default.csv"

files = glob.glob("./data/buf/*.txt")
print(files)
lst = [HEADER]
for file in files:
    with open(file) as f:
        a = [e for e in csv.reader(f, delimiter="\t")]
        for i, b in enumerate(a):
            if len(b)!=len(HEADER):
                a.pop(i)

        lst = lst + a
    
df = pd.DataFrame(lst)

if len(sys.argv)>1:
    savefilename = sys.argv[1]
    
df.to_csv("./data/"+savefilename, header=False, index=False)