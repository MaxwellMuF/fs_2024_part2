import requests
import os

def data_download_from_url():
    """Download the data sets from given URLs and """
    ## URL of the CSV file

    # https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/start.html
    charging_stations_url   = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeulenregister_01122024.xlsx"
    # https://www.suche-postleitzahl.org/downloads
    residents_url           = "https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv"
    # https://daten.odis-berlin.de/de/dataset/plz/
    geo_json                = "https://tsb-opendata.s3.eu-central-1.amazonaws.com/plz/plz.geojson"

    # Specify the directory where you want to save the file
    save_directory          = "infrastructure/data/raw_data"

    for data_url in [charging_stations_url, residents_url, geo_json]:
        # Get the file name from the URL and replace _ at the end of the excel file
        file_name           = data_url.split("/")[-1]
        file_name           = "".join([char for char in file_name if char.isalpha() or char in ["_", "."]])
        if file_name.endswith("_.xlsx"):
            file_name       = file_name.replace("_.xlsx", ".xlsx")

        # Full path where the file will be saved
        file_path = os.path.join(save_directory, file_name)

        # Download the file and save it
        response = requests.get(data_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"File saved as {file_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    
    return
