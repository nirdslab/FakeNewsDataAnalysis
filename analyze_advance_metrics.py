import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


def analyze_processed_features():
    df = pd.read_csv("Data/PublicDataset/ProcessedFeatures/D2-Features.csv")
    print(df[['meanPupilDiamater', 'fixationCount', 'saccadeCount', 'version']].groupby(['version']).agg(['mean', 'count']))


def analyze_generated_data_avg():
    df = pd.read_csv("./Data/REAMAP_Output/generated_dataset_with_version.csv")

    print(df[['IPA', 'LHIPA', 'pavg', 'pcpd', 'version']].groupby(['version']).mean())

    ax = df.groupby(['version'])['IPA'].mean().plot(kind='bar')
    ax.set_xlabel("Version")
    ax.set_ylabel("IPA")
    plt.show()

    # ax = df.groupby(['version'])['LHIPA'].mean().plot(kind='bar')
    # ax.set_xlabel("Version")
    # ax.set_ylabel("LHIPA")
    # plt.show()

    # ax = df.groupby(['version'])['pavg'].mean().plot(kind='bar')
    # ax.set_xlabel("Version")
    # ax.set_ylabel("PAVG")
    # plt.show()

    # ax = df.groupby(['version'])['pcpd'].mean().plot(kind='bar')
    # ax.set_xlabel("Version")
    # ax.set_ylabel("PCPD")
    # plt.show()


def analyze_generated_data_ttest():
    df = pd.read_csv("./Data/REAMAP_Output/generated_dataset_with_version.csv")

    group1 = df[df['version'] == 'fake']
    group2 = df[df['version'] == 'true']

    # perform independent two sample t-test
    print("IPA:")
    print(ttest_ind(group1['IPA'], group2['IPA']))
    print("\nLHIPA:")
    print(ttest_ind(group1['LHIPA'], group2['LHIPA']))
    print("\npavg:")
    print(ttest_ind(group1['pavg'], group2['pavg']))
    print("\npcpd:")
    print(ttest_ind(group1['pcpd'], group2['pcpd']))


if __name__ == "__main__":
    # analyze_processed_features()
    # analyze_generated_data_avg()
    analyze_generated_data_ttest()
