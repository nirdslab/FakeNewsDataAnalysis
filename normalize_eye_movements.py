import pandas as pd
import os


indir = "./Data/ProcessedEyeMovementData/"
outdir = "./Data/ReformattedData/"


def getx(row):
    # data not already normalized, need to divide by screen size
    xl = row['Gaze point left X']/1920
    xr = row['Gaze point right X']/1920

    if xl > 0.0 and xr > 0.0:
        x = str((xl + xr) / 2.0)
    elif xl > 0.0:
        x = str(xl)
    elif xr > 0.0:
        x = str(xr)
    else:
        x = '-1'
    return x


def gety(row):
    # data not already normalized, need to divide by screen size
    yl = row['Gaze point left Y']/1080
    yr = row['Gaze point right Y']/1080

    if yl > 0.0 and yr > 0.0:
        y = str((yl + yr) / 2.0)
    elif yl > 0.0:
        y = str(yl)
    elif yr > 0.0:
        y = str(yr)
    else:
        y = '-1'
    return y


def getpd(row):
    if row['Pupil diameter left'] > 0 and row['Pupil diameter right'] > 0:
        pd = (row['Pupil diameter left'] + row['Pupil diameter right']) / 2
    elif row['Pupil diameter left'] > 0 and row['Pupil diameter right'] == 0.0:
        pd = row['Pupil diameter left']
    elif row['Pupil diameter left'] == 0.0 and row['Pupil diameter right'] > 0:
        pd = row['Pupil diameter right']
    else:
        pd = 0.0
    return pd


def reformat(path, subj, trial):
    df = pd.DataFrame(columns=["x", "y", "d", "t"])
    dframe = pd.read_csv(path)
    df["x"] = dframe.apply(getx, axis=1)
    df["y"] = dframe.apply(gety, axis=1)
    df["d"] = dframe.apply(getpd, axis=1)
    df["t"] = dframe["Recording timestamp"]

    filename = subj+"-"+trial+".csv"

    df.to_csv(outdir+filename,index=False)


if os.path.isdir(indir):
    for top, dirs, listing in os.walk(indir):
        for file in listing:
            path = os.path.join(top, file)
            dname = path.split('/')[2]
            base = os.path.basename(path)
            if base.endswith('.csv'):
                basename = base[:base.rfind('.csv')]
                subj = basename.split("_")[1]
                trial = basename.split("_")[2]

                print(path, basename, subj, trial)

                reformat(path, subj, trial)
