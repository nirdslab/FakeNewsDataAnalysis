import pandas as pd
import os

raw_data_path = r"Data/RawData"
processed_eye_movement_data_path = r"Data/ProcessedEyeMovementData"


def read_raw_data_file(file_path):
    print("Reading the file at " + str(file_path))
    df = pd.read_csv(file_path, sep='\t')
    return df


def filter_eye_movement_data(df):
    df = df[df.Sensor == 'Eye Tracker']
    return df


def remove_invalid_data(df):
    # Validity left/ Validity right: Indicates the confidence level that the left/ right eye has been correctly
    # identified. The available values are valid and invalid
    # Get indexes where Validity left and Validity right columns have "Invalid" values
    invalid_data_index = df[(df['Validity left'] == 'Invalid') & (df['Validity right'] == 'Invalid')].index
    # Delete these row indexes from dataFrame
    df.drop(invalid_data_index, inplace=True)

    df = df.dropna(axis=0, how="all", thresh=None, subset=["Gaze point right Y", "Gaze point left Y"], inplace=False)
    df = df.dropna(axis=0, how="all", thresh=None, subset=["Gaze point right X", "Gaze point left X"], inplace=False)

    df = df.dropna(axis=0, how="all", thresh=None, subset=["Pupil diameter left", "Pupil diameter right"],
                   inplace=False)

    return df


def replace_comma(x):
    return str(x).replace(",", ".")


# Since the comma is used as a decimal separator, update it with dot
def update_decimal_seperator(df):
    df["Pupil diameter left"] = df["Pupil diameter left"].apply(replace_comma)
    df["Pupil diameter right"] = df["Pupil diameter right"].apply(replace_comma)
    return df


def process_invalid_eye_movement_data(df):
    df['Gaze point left X'] = df['Gaze point left X'].fillna(0)
    df['Gaze point right X'] = df['Gaze point right X'].fillna(0)
    df['Gaze point left Y'] = df['Gaze point left Y'].fillna(0)
    df['Gaze point right Y'] = df['Gaze point right Y'].fillna(0)

    df['Pupil diameter left'] = df['Pupil diameter left'].fillna(0)
    df['Pupil diameter right'] = df['Pupil diameter right'].fillna(0)

    # The implementation is done with the assumption that X and Y gaze points are higher than the
    # resolution are 1920 and 1080
    df.loc[df['Gaze point left X'] > 1920, 'Gaze point left X'] = 1920
    df.loc[df['Gaze point right X'] > 1920, 'Gaze point right X'] = 1920

    df.loc[df['Gaze point left X'] < 0, 'Gaze point left X'] = 0
    df.loc[df['Gaze point right X'] < 0, 'Gaze point right X'] = 0

    df.loc[df['Gaze point left Y'] > 1080, 'Gaze point left Y'] = 1080
    df.loc[df['Gaze point right Y'] > 1080, 'Gaze point right Y'] = 1080

    df.loc[df['Gaze point left Y'] < 0, 'Gaze point left Y'] = 0
    df.loc[df['Gaze point right Y'] < 0, 'Gaze point right Y'] = 0

    return df


def split_data_by_presented_stimulus(df, file):
    stimuli = ['Stimulus1', 'Stimulus2', 'Stimulus3', 'Stimulus4', 'Stimulus5', 'Stimulus6', 'Stimulus7', 'Stimulus8',
               'Stimulus9', 'Stimulus10', 'Stimulus11', 'Stimulus12', 'Stimulus13', 'Stimulus14', 'Stimulus15',
               'Stimulus16', 'Stimulus17', 'Stimulus18', 'Stimulus19', 'Stimulus20', 'Stimulus21', 'Stimulus22',
               'Stimulus23', 'Stimulus24', 'Stimulus25', 'Stimulus26', 'Stimulus27', 'Stimulus28', 'Stimulus29',
               'Stimulus30', 'Stimulus31', 'Stimulus32', 'Stimulus33', 'Stimulus34', 'Stimulus35', 'Stimulus36',
               'Stimulus37', 'Stimulus38', 'Stimulus39', 'Stimulus40', 'Stimulus41', 'Stimulus42', 'Stimulus43',
               'Stimulus44', 'Stimulus45', 'Stimulus46', 'Stimulus47', 'Stimulus48', 'Stimulus49', 'Stimulus50',
               'Stimulus51', 'Stimulus52', 'Stimulus53', 'Stimulus54', 'Stimulus55', 'Stimulus56', 'Stimulus57',
               'Stimulus58', 'Stimulus59', 'Stimulus60']

    # To get eye movement data for all the presented stimulus
    # stimuli = df['Presented Stimulus name'].unique().tolist()

    for stimulus in stimuli:
        df_stimulus = df[df['Presented Stimulus name'] == stimulus]
        df_stimulus = df_stimulus[['Gaze point left X', 'Gaze point right Y', 'Gaze point left Y',
                                   'Gaze point right X', 'Pupil diameter left', 'Pupil diameter right',
                                   'Recording timestamp']]
        file_split = file.split("_")
        output_filename = "P" + file_split[0] + "_" + str(stimulus) + ".csv"
        print("Writing the file: " + str(output_filename))
        df_stimulus.to_csv(f"{processed_eye_movement_data_path}/{output_filename}")


if __name__ == "__main__":
    os.chdir(raw_data_path)
    filenames = os.listdir()
    os.chdir("../../")

    for file in filenames:
        if file.endswith(".tsv"):
            file_path = f"{raw_data_path}/{file}"
            df = read_raw_data_file(file_path)
            df = filter_eye_movement_data(df)
            df = remove_invalid_data(df)
            df = process_invalid_eye_movement_data(df)
            df = update_decimal_seperator(df)
            split_data_by_presented_stimulus(df, file)
