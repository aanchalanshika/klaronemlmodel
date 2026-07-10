import pandas as pd

def load_data():
    """ loads the laptop dataset and return is as  a pandas dataframe"""
    df = pd.read_csv("data/laptop.csv")
    return df
if __name__ == "__main__":
    df= load_data()
    print("first 5 rows")
    print(df.head())
    print("\nDataset shape")
    print(df.shape)
