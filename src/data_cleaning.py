import re
import pandas as pd
from data_loader import load_data
df = load_data()
df= df.copy()
df.drop(columns = ["Unnamed: 0"], inplace = True)
#remove the missing value
df.dropna()
df = df[df["spec_score"]!=0]
# cleaning the white spaces 
object_columns = df.select_dtypes(include="object").columns
for column in object_columns:
    df[column] = df[column].str.strip()
for column in object_columns:
    df[column] = df[column].str.replace(r"\s+"," ", regex= True)
    #this portion makes the text consistent
#here we are saving the cleaned dataset
df.to_csv("data/cleaned_laptops.csv",index = False)
print("Cleaned dataset saved successfully.")

# ================================
# Verify Cleaning
# ================================

print("Shape Before Cleaning :", load_data().shape)
print("Shape After Cleaning  :", df.shape)

print("\nRemaining Missing Values")
print(df.isnull().sum())

print("\nRemaining Spec Score = 0")
print((df["spec_score"] == 0).sum())

print("\nCleaned dataset saved successfully.")

