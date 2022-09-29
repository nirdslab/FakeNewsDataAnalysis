import pandas as pd
import os


indir = "./Data/ReformattedData/"
outdir = "./Data/TimestampReformattedData/"


def reformat(path):
    print("Reading " + str(path))
    df = pd.read_csv(path)
    size = int(len(df))
    timestamp = []
    for i in range(size):
        if i == 0:
            timestamp.append(0)
        else:
            timestamp.append(i/600)
    df['t'] = timestamp
    filename = path.split("/")[-1]
    df.to_csv(outdir + "/" + filename)
    exit(0)


if os.path.isdir(indir):
    for top, dirs, listing in os.walk(indir):
        for file in listing:
            path = os.path.join(top, file)
            dname = path.split('/')[2]
            base = os.path.basename(path)
            if base.endswith('.csv'):
                reformat(path)