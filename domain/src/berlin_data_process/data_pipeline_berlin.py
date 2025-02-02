import csv
from dataclasses    import dataclass
from typing         import List, Dict, Any


#  --------------------------------------- Pipeline Classes ------------------------------------------------------

@dataclass
class RenameTargetColumn:
    rename_column: Dict[str,str]

    def process(self, data: List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        """Rename target column 'PLZ' if nessesary"""
        for idx,row in enumerate(data):
            temp_dict = {}
            temp_dict = row.copy()
            for key in row.keys():
                if key in self.rename_column.keys():
                    temp_dict[self.rename_column[key]] = temp_dict.pop(key)
            # using temp dict, cause data and row cannot be changed in the same iterration of key in row.keys
            if temp_dict != row:
                data[idx] = temp_dict
                
        return data
    

@dataclass
class FilterColumns:
    required_columns: List[str]

    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filer columns by given List[str] and remove unnessesary ones"""
        filtered_data = []
        for row in data:
            try:
                # Create a filtered row containing only required columns
                filtered_row = {key: row[key] for key in self.required_columns}
                filtered_data.append(filtered_row)
            except KeyError as e:
                raise KeyError(f"FilterColumns: Missing required column: {e.args[0]} in row: {row}")
        return filtered_data


@dataclass
class Cleaner:
    reject_data: List[str]
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cleans the data by removing rows with missing values."""
        cleaned_data = [row for row in data if all(value not in self.reject_data for value in row.values())]
        print(f"Cleaner: Removed {len(data)-len(cleaned_data)} rows")
        return cleaned_data


@dataclass
class FilterBerlin:
    filter_plz_min: int
    filter_plz_max: int
    filter_column: str

    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filer rows by given List[str] and remove unnessesary ones"""
        return [row for row in data if self.filter_plz_min < int(row[self.filter_column]) < self.filter_plz_max]

@dataclass
class Validator:
    required_types: Dict[str, Any]

    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate if column value can be converted to required type"""
        validated_data = []
        for row in data:
            try:
                for col, col_type in self.required_types.items():
                    row[col] = col_type(row[col])
                validated_data.append(row)

            except ValueError as e:
                raise ValueError(f"Validator: Skipped invalid row: {row}. Error: {e}")
            
        print(f"Validator: Validated data types. Remaining rows: {len(validated_data)}")
        return validated_data
        

@dataclass
class Pipeline:
    steps: List[Any]  

    def run(self, data: List[Dict[str, Any]] = None)-> List[Dict[str, Any]]:
        """Executes a series of steps to process the data."""
        for step in self.steps:
            data = step.process(data)
        return data

@dataclass
class LoadRawData:
    load_path: str

    def process(self, data=None) -> List[Dict[str, Any]]: # data=None for testing
        """Load raw data from directory"""
        with open(self.load_path, mode="r", encoding="utf-8") as csvfile:
            reader = list(csv.DictReader(csvfile))
        print(f"Loaded data '{self.load_path.split('/')[-1]}' successfully")
        return reader
    
@dataclass
class SaveProcessedDate:
    save_path: str

    def process(self, data: List[Dict[str, Any]])-> List[Dict[str, Any]]:
        """Save processed data at given path"""
        if not data:
            print("No data to save.")
            return
        with open(self.save_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved data '{self.save_path.split('/')[-1]}' successfully")
        return data # for Testing


def activate_data_pipeline_berlin():
    """"Activate pipeline and init properties of pipeline classes"""
    load_data_path = "infrastructure/data/raw_data"
    save_data_path = "domain/data/processed_data_for_ui"
    list_file = ["geodata_berlin_plz.csv", "Ladesaeulenregister.csv", "plz_einwohner.csv"]
    dict_rename_columns = {"Postleitzahl"                       : "PLZ", 
                           "Nennleistung Ladeeinrichtung [kW]"  : "KW",
                           "plz"                                : "PLZ", 
                           "einwohner"                          : "Residents"}
    list_filter_columns = [["PLZ","geometry"], 
                           ["PLZ","Straße","Hausnummer","Art der Ladeeinrichung","Anzahl Ladepunkte",
                            "KW"],
                           ["PLZ","Residents"]]
    list_required_types = [{"PLZ":int},
                           {"PLZ":int, "Straße":str,"Hausnummer":str, "Art der Ladeeinrichung":str,
                            "Anzahl Ladepunkte":int, "KW":float},
                           {"PLZ":int, "Residents":int}]


    for idx in range(len(list_file)):
        loader                      = LoadRawData(load_path                 =f"{load_data_path}/{list_file[idx]}")
        renamer                     = RenameTargetColumn(rename_column      =dict_rename_columns)
        filter_columns              = FilterColumns(required_columns        =list_filter_columns[idx])
        cleaner                     = Cleaner(reject_data                   =["", "None", "NaN"])
        filter_berlin               = FilterBerlin(filter_plz_min           =10000,filter_plz_max=14200,filter_column="PLZ")
        validator                   = Validator(required_types              =list_required_types[idx])
        saver                       = SaveProcessedDate(save_path           =f"{save_data_path}/{list_file[idx]}")
        pipeline                    = Pipeline(steps                        =[loader, renamer, filter_columns, cleaner, 
                                                                              filter_berlin, validator, saver])
        pipeline.run()
    
    return

if __name__ == "__main__":
    activate_data_pipeline_berlin()
