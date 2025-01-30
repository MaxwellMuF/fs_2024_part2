import csv
from dataclasses    import dataclass
from typing         import List, Dict, Any


#  --------------------------------------- Pipeline Classes ------------------------------------------------------

@dataclass
class RenameTargetColumn:
    target_column_list: List[str]

    def process(self, data: List[Dict[str,Any]]) -> List[Dict[str, Any]]:
        """Rename target column 'PLZ' if nessesary"""
        filtered_data = []
        for idx,row in enumerate(data):
            for key in row.keys():
                if key in self.target_column_list:
                    temp_dict = row.copy()
                    temp_dict["PLZ"] = temp_dict.pop(key)
            # using temp dict, cause data and row cannot be changed in the same iterration of key in row.keys
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

    def run(self, data: List[Dict[str, Any]])-> List[Dict[str, Any]]:
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


def activate_data_validator_pipeline(self):
    load_data_path = "domain/src/berlin_data_process/tests/test_file.csv"
    save_data_path = ""
    loader = LoadRawData(load_path= load_data_path)
    filter_columns = FilterColumns(required_columns =["PLZ", "Straße", "KW"])
    cleaner = Cleaner(reject_data                   =["", "None", "NaN", "0"])
    filter_berlin = FilterBerlin(filter_plz_min     =1000, filter_plz_max=1400, filter_column="PLZ")
    validator = Validator(required_types            ={"PLZ":int, "Straße":str, "KW":float})
    saver = SaveProcessedDate(save_path=save_data_path)
    pipeline = Pipeline(steps                       =[loader, filter_columns, cleaner, 
                                                        filter_berlin, validator, saver])