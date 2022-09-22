import pandas as pd
import os
import json

stimulus_regions_df = pd.DataFrame(columns=['stimulus id', 'version', 'start x', 'start y', 'width', 'height',
                                            'end x', 'end y', 'region'])
participant_stimulus_version = None

in_dir = "./Data/ProcessedEyeMovementData/"
out_dir = "./Data/ProcessedEyeMovementWithAOI/"


def read_annotations():
    global stimulus_regions_df
    annotations_df = pd.read_csv("Data/PublicDataset/AOI_data/annotations.csv")

    for index, row in annotations_df.iterrows():
        filename = row["filename"]
        file = (str(filename.split(".png")[0])).split("_")
        stimulus_id = int(file[0].replace("Q", ""))
        version = file[1]

        region_shape_attributes = row["region_shape_attributes"]
        region_shape_attributes_json = json.loads(region_shape_attributes)
        start_x = region_shape_attributes_json['x']
        start_y = region_shape_attributes_json['y']
        width = region_shape_attributes_json['width']
        height = region_shape_attributes_json['height']
        end_x = int(start_x) + int(width)
        end_y = int(start_y) + int(height)

        region_attributes = row["region_attributes"]
        region = json.loads(region_attributes)["region type"]

        new_data = pd.DataFrame({
            "stimulus id": [stimulus_id],
            "version": [version],
            "start x": [start_x],
            "start y": [start_y],
            "width": [width],
            "height": [height],
            "end x": [end_x],
            "end y": [end_y],
            "region": [region]
        })

        stimulus_regions_df = pd.concat([stimulus_regions_df, new_data])


def read_processed_features():
    global participant_stimulus_version
    features = pd.read_csv("Data/PublicDataset/ProcessedFeatures/D2-Features.csv")
    participant_stimulus_version = features[['participant', 'question', 'version']]


def get_stimulus_version_read_by_participant(participant_id, stimulus_id):
    # Given the participant id and stimulus id, this function will return the version (fake or true) of the stimulus
    # that the given participant has read
    version = participant_stimulus_version.loc[(participant_stimulus_version.participant == participant_id) &
                                               (participant_stimulus_version.question == stimulus_id)].version.item()

    return version


def get_region_details(stimulus_id, version):
    # Given the stimulus id and the version, this function will return aoi region information

    if version == "fake":
        regions = stimulus_regions_df.loc[(stimulus_regions_df["stimulus id"] == stimulus_id) &
                                      (stimulus_regions_df["version"] == "false")]
    else:
        regions = stimulus_regions_df.loc[(stimulus_regions_df["stimulus id"] == stimulus_id) &
                                          (stimulus_regions_df["version"] == "true")]
    return regions


def getx(row):
    xl = row['Gaze point left X']
    xr = row['Gaze point right X']

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
    yl = row['Gaze point left Y']
    yr = row['Gaze point right Y']

    if yl > 0.0 and yr > 0.0:
        y = str((yl + yr) / 2.0)
    elif yl > 0.0:
        y = str(yl)
    elif yr > 0.0:
        y = str(yr)
    else:
        y = '-1'
    return y


def get_aoi_label(row, regions):
    x = float(getx(row))
    y = float(gety(row))
    aoi = regions.loc[(regions["start x"] <= x) & (regions["end x"] >= x) & (regions["start y"] <= y) &
                      (regions["end y"] >= y)].region
    if len(aoi) == 0:
        return None
    else:
        return aoi.item()


def read_reformatted_eye_movements_data(file_path, filename):
    ignore_list = ['P03-Stimulus7.csv', 'P03-Stimulus32.csv',
                   'P05-Stimulus17.csv',
                   'P10-Stimulus1.csv', 'P10-Stimulus2.csv',
                   'P10-Stimulus5.csv', 'P10-Stimulus7.csv', 'P10-Stimulus8.csv', 'P10-Stimulus12.csv',
                   'P10-Stimulus15.csv', 'P10-Stimulus19.csv', 'P10-Stimulus24.csv', 'P10-Stimulus28.csv',
                   'P10-Stimulus46.csv', 'P10-Stimulus52.csv',
                   'P11-Stimulus43.csv',
                   'P12-Stimulus7.csv', 'P12-Stimulus14.csv', 'P12-Stimulus16.csv', 'P12-Stimulus20.csv',
                   'P12-Stimulus22.csv', 'P12-Stimulus25.csv', 'P12-Stimulus29.csv', 'P12-Stimulus34.csv',
                   'P12-Stimulus35.csv', 'P12-Stimulus41.csv', 'P12-Stimulus43.csv', 'P12-Stimulus45.csv',
                   'P12-Stimulus50.csv', 'P12-Stimulus53.csv', 'P12-Stimulus55.csv', 'P12-Stimulus59.csv',
                   'P12-Stimulus60.csv',
                   'P18-Stimulus8.csv',
                   'P21-Stimulus2.csv',
                   'P24-Stimulus7.csv', 'P24-Stimulus9.csv',
                   'P26-Stimulus5.csv', 'P26-Stimulus12.csv', 'P26-Stimulus13.csv', 'P26-Stimulus15.csv',
                   'P26-Stimulus17.csv', 'P26-Stimulus20.csv', 'P26-Stimulus23.csv', 'P26-Stimulus27.csv',
                   'P26-Stimulus28.csv', 'P26-Stimulus30.csv', 'P26-Stimulus39.csv', 'P26-Stimulus47.csv',
                   'P26-Stimulus59.csv', 'P26-Stimulus60.csv']
    if filename in ignore_list:
        return
    participant_stimulus = ((filename.split(".csv")[0]).split("_"))
    participant_id = int(participant_stimulus[0].replace("P", ""))
    stimulus_id = int(participant_stimulus[1].replace("Stimulus", ""))
    version = get_stimulus_version_read_by_participant(participant_id, stimulus_id)

    print("Participant " + str(participant_id) + " has read stimulus: " + str(stimulus_id) + ", version: " +
          str(version))

    regions = get_region_details(stimulus_id, version)

    print("Reading the file at " + str(file_path))
    df = pd.read_csv(file_path)

    new_df = pd.DataFrame(columns=["Gaze point left X", "Gaze point right Y", "Gaze point left Y", "Gaze point right X",
                                   "Pupil diameter left", "Pupil diameter right", "Recording timestamp", "AOI_Label"])

    for index, row in df.iterrows():
        aoi_label = get_aoi_label(row, regions)

        new_data = pd.DataFrame({
            "Gaze point left X": [row["Gaze point left X"]],
            "Gaze point right X": [row["Gaze point right X"]],
            "Gaze point left Y": [row["Gaze point left Y"]],
            "Gaze point right Y": [row["Gaze point right Y"]],
            "Pupil diameter left": [row["Pupil diameter left"]],
            "Pupil diameter right": [row["Pupil diameter right"]],
            "Recording timestamp": [row["Recording timestamp"]],
            "AOI_Label": [aoi_label]
        })

        new_df = pd.concat([new_df, new_data])

    new_df.to_csv(out_dir + filename)


if __name__ == "__main__":
    os.chdir(in_dir)
    filenames = os.listdir()
    os.chdir("../../")

    read_annotations()
    read_processed_features()

    for file in filenames:
        if file.endswith(".csv"):
            file_path = f"{in_dir}/{file}"
            read_reformatted_eye_movements_data(file_path, file)
