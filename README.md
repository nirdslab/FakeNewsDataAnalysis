# FakeNewsDataAnalysis
This repository contains the scripts that are used for analysing FakeNewsPerception dataset.


## Dataset

There are two datasets.

* Processed dataset (172 MB): https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/C1UD2A
* Raw dataset (23 GB): We obtained the raw data from the authors [[1]](#1)

### Raw Data
The raw eye tracking data are recorded and exported using the eye tracker computer (Tobii Pro-Spectrum) and Tobii Pro-Lab software.

## Instructions

### Setup
* **Python Version: 3.9**

### Install packages
* Install pandas:
``` pip install pandas```

### Process Raw Data
Here, we read the raw data and process them.
1. filter out mouse data
2. remove invalid data
3. replace comma with decimal point
4. process invalid eye data
5. split data by stimulus
6. remove unwanted columns

* Run `process_raw_data.py`
* Input Data: "Data/RawData"
* Output Data: "Data/ProcessedEyeMovementData" 

### Normalize Data
Prior to sending the data to RAEMAP pipeline we,
1. normalize the data using resolution 
2. generate mean x, mean y using Gaze point x and y values for left and right eye. 
3. generate mean pupil diameter using left and right pupil diameters

* Run `normalize_eye_movements.py`
* Input Data: "Data/ProcessedEyeMovementData" 
* Output Data: "Data/ReformattedData" 


## References
<a id="1">[1]</a> Ömer Sümer, Efe Bozkir, Thomas Kübler, Sven Grüner, Sonja Utz, and Enkelejda Kasneci. 2021. FakeNewsPerception: An eye movement dataset on
the perceived believability of news stories. Data in Brief 35 (2021), 106909. https://doi.org/10.1016/j.dib.2021.106909
