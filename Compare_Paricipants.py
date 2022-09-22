import pandas as pd
import os


def write_participant_data():
    df = pd.read_csv("Data/RawData/D2_Processed_features.tab", sep='\t')
    split_values = df['participant'].unique().tolist()
    print(split_values)
    for value in split_values:
        df1 = df[df['participant'] == value]
        output_filename = "participant" + "_" + str(value) + ".csv"
        print(output_filename)
        df1.to_csv(f"Data/Participants/{output_filename}")


def read_participant_data_file(file_path):
    print("Reading the file at " + str(file_path))
    df = pd.read_csv(file_path)
    return df


def count_fake_true_believability_rate(df, file):
    participant_id = file.split(".")[0]

    correct_fake_count = 0
    correct_true_count = 0
    incorrect_fake_count = 0
    incorrect_true_count = 0
    unsure_count = 0
    for index, row in df.iterrows():
        if row['believability'] > -1:
            if row['version'] == 'fake' and (row['believability'] == 1 or row['believability'] == 2):
                correct_fake_count = correct_fake_count + 1
            elif row['version'] == 'fake' and (row['believability'] == 4 or row['believability'] == 5):
                incorrect_fake_count = incorrect_fake_count + 1
            elif row['version'] == 'true' and (row['believability'] == 4 or row['believability'] == 5):
                correct_true_count = correct_true_count + 1
            elif row['version'] == 'true' and (row['believability'] == 1 or row['believability'] == 2):
                incorrect_true_count = incorrect_true_count + 1
            else:
                unsure_count = unsure_count + 1

    print(participant_id, correct_fake_count, correct_true_count, incorrect_fake_count, incorrect_true_count,
          unsure_count)


write_participant_data()

Participants_data_path = r"Data/Participants/"
os.chdir(Participants_data_path)

filenames = os.listdir()
os.chdir("../..")

for file in filenames:
    if file.endswith(".csv"):
        file_path = f"{Participants_data_path}/{file}"
        df = read_participant_data_file(file_path)
        count_fake_true_believability_rate(df, file)
