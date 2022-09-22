import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_scanpath(file_name):
    df = pd.read_csv(file_name)

    # Print eventTypes available
    print(df['eventType'].unique())

    # Get the Fixation data
    p01_s01_fake_df_fixation = df[df['eventType'] == 'Fixation']

    # Get the Saccade data
    p01_s01_fake_df_saccade = df[df['eventType'] == 'Saccade']

    # Sort the dataframe with start time column
    p01_s01_fake_df_fixation.sort_values('starttime')
    p01_s01_fake_df_saccade.sort_values('starttime')

    fixation_x = p01_s01_fake_df_fixation['meanX'].tolist()
    fixation_y = p01_s01_fake_df_fixation['meanY'].tolist()
    fixation_number = list(np.arange(1, len(p01_s01_fake_df_fixation.index.values.tolist())+1))

    # Plot eye fixations as a scatter plot
    fig, ax = plt.subplots()
    ax.scatter(fixation_x, fixation_y, s=15, color="red")

    for i, txt in enumerate(fixation_number):
        ax.annotate(txt, (fixation_x[i], fixation_y[i]), fontsize=8)

    # Plot saccades as arrows from (startSccadeX, startSaccadeY) to (endSaccadeX, endSaccadeY)
    start_saccade_x = p01_s01_fake_df_saccade['startSaccadeX'].to_numpy()
    end_saccade_x = p01_s01_fake_df_saccade['endSaccadeX'].to_numpy()
    start_saccade_y = p01_s01_fake_df_saccade['startSaccadeY'].to_numpy()
    end_saccade_y = p01_s01_fake_df_saccade['endSaccadeY'].to_numpy()

    for i in range(len(start_saccade_x)):
        plt.arrow(start_saccade_x[i], start_saccade_y[i], end_saccade_x[i] - start_saccade_x[i],
                  end_saccade_y[i] - start_saccade_y[i], head_width=8, length_includes_head=True, color="lightblue")

    plt.title(file_name.split("/")[-1].replace(".csv", ""))
    plt.show()


processed_data_path = "Data/PublicDataset/EyeMovementsData/"
dir_list = os.listdir(processed_data_path)
for file in dir_list:
    create_scanpath(processed_data_path + file)
