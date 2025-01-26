import csv
from dataclasses    import dataclass
from typing         import List, Dict, Any


#  --------------------------------------- Pipeline Classes ------------------------------------------------------

@dataclass
class FilterColumns:
    """Filer columns by given List[str] and remove unnessesary ones"""
    required_columns: List[str]

    def process(self, data: List[Dict[str, Any]]):#
        filtered_data = []
        for row in data:
            try:
                # Create a filtered row containing only required columns
                filtered_row = {key: row[key] for key in self.required_columns}
                filtered_data.append(filtered_row)
            except KeyError as e:
                raise KeyError(f"Missing required column: {e.args[0]} in row: {row}")
        return filtered_data


@dataclass
class Cleaner:
    """Cleans the data by removing rows with missing values."""
    
    def process(self, data: List[Dict[str, Any]], reject_data: List[str]):
        cleaned_data = [row for row in data if all(value not in reject_data for value in row.values())]
        print(f"Cleaner: Removed {len(data)-len(cleaned_data)} rows")
        return cleaned_data


@dataclass
class FilterBerlin:
    """Filer rows by given List[str] and remove unnessesary ones"""
    filter_plz_min: int
    filter_plz_max: int

    def process(self, data: List[Dict[str, Any]]):
        return [row for row in data if self.filter_plz_min < int(row['PLZ']) < self.filter_plz_max]
        
    
