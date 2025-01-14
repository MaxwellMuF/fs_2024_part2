import pandas as pd
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