# Healthy-Data

### Streamlit dashboard for easy access to datasets
These datasets were preprocessed and curated to support data driven professional Hackathons. 

## Documentation

### Starting up
The Streamlit webapp lives in the `app.py` and can be started locally by running `streamlit run path/to/src/app.py`. Make sure all packages in **requirements.txt** are installed.

### Add new datasets
Step-by-step guide to add new datasets:
1. Copy the dataset under `src/data/`. File extension must be .csv
2. Run `data_prep.py` from terminal. This is a command line tool that scans the data folder for any new files and can be used to add new datasets or delete older ones. Once a file selected its attributes has to be added.
3. Every newly added dataset will be an entry in `data_inventory.csv`, the app scans this file and loads the preview for each dataset.

### About the Dataset object
Every entry in the `data_inventory.csv` file creates a Dataset object (from `Data.py`). This object is then used to filter, handle and display the data in the app. 

### Add new plots
Every plot in the app uses Plotly. Currently a conditional statement on the filename can be used to display plots, interactive widgets or any other dataset-specific element. For this, use the `plotting.py` file.