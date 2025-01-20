import pandas as pd
from datetime import datetime

if False:
    print(pd.DataFrame({
                "PLZ": [10179, 10243],
                "Breitengrad": ["52.518611", "52.514233"],
                "Längengrad": ["13.408056", "13.454281"],
                "Bundesland": ["Berlin", "Berlin"],
                "Straße": ["Some Street", "Another Street"],
                "Hausnummer": ["1", "2"],
                "Ort": ["Berlin", "Berlin"],
                "KW": [22.0, 11.0],
                "Plug Types": ["Type2", "Type1"],
                "geometry": ["POINT (13.408056 52.518611)", "POINT (13.454281 52.514233)"]
            })
    )

if False:
    test_dict = {key:value for key,value in zip("abcde", range(5))}
    print(test_dict.keys())

if False:
    test_dict = pd.DataFrame({"col1":[1,2], "col2":[3,4]}).to_dict()
    print(test_dict)

if False:
    print([[""]*5]*2)

if False:
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

if True:
    for i in {"PLZ": {"1492": 12489}, 
            "Stra\u00dfe": {"1492": "Stromstra\u00dfe"}, 
            "Hausnummer": {"1492": "40"}, 
            "Anzahl Ladepunkte": {"1492": 2.0}, 
            "KW": {"1492": 22.0}, 
            "Rating": {"1492": "\u2b50\u2b50"}, 
            "Comment": {"1492": "slow!"}, 
            "Date": {"1492": "2025-01-20 18:55:19"}}.keys():
        print(i)

    print({"PLZ": {"1492": 12489}, 
            "Stra\u00dfe": {"1492": "Stromstra\u00dfe"}, 
            "Hausnummer": {"1492": "40"}, 
            "Anzahl Ladepunkte": {"1492": 2.0}, 
            "KW": {"1492": 22.0}, 
            "Rating": {"1492": "\u2b50\u2b50"}, 
            "Comment": {"1492": "slow!"}, 
            "Date": {"1492": "2025-01-20 18:55:19"}}.keys())
    
    assert_data_types = {"PLZ"              : int, 
                         "Straße"           : str, 
                         "Hausnummer"       : str, 
                         "Anzahl Ladepunkte": float, 
                         "KW"               : float, 
                         "Rating"           : str, 
                         "Comment"          : str, 
                         "Date"             : str}
    
    for column in data_of_one_user.keys():
        for col_value in data_of_one_user[column]:
            assert isinstance(col_value, assert_data_types[column])
