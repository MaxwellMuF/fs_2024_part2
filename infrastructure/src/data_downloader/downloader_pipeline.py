from infrastructure.src.data_downloader import download_data
from infrastructure.src.data_downloader import data_cleaner_and_format

## Pipeline

def activate_dowload():
    # Download all required data: 3 data sets 
    download_data.data_download_from_url()

    # process right format, delete old files
    data_cleaner_and_format.process_excel_to_csv()
    data_cleaner_and_format.process_geojson_to_csv()
    
    return