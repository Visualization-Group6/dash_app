import pandas as pd


def read_data(encoded_data, filename, content_type) -> pd.DataFrame:
    if not encoded_data:
        raise(Exception("markoerror"))
    print(encoded_data.decode())
    print(filename, content_type)
    return pd.DataFrame({'test':[1,2,3,4,5,6]})  # TEST
