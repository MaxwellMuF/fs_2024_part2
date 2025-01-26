import csv
from dataclasses    import dataclass
from typing         import List, Dict, Any


#  --------------------------------------- Pipeline Classes ------------------------------------------------------

@dataclass
class FilterColumns:
    """Filer columns by given List[str] and remove unnessesary ones """


@dataclass
class Cleaner:
    """Cleans the data by removing rows with missing values."""
    
    def process(self, data: List[Dict[str, Any]], reject_data: List[str]):
        cleaned_data = [row for row in data if all(value not in reject_data for value in row.values())]
        print(f"Cleaner: Removed {len(data)-len(cleaned_data)} rows")
        return cleaned_data