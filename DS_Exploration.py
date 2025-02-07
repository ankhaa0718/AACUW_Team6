# Loading in the dataset

#some needed import statements 
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

print("Hello")

df = pd.read_csv("Seattle_Rescue_Plan.csv")

print(df.shape)

print(df.columns)

# print("This is the mean: " + str(df["Budgeted"].mean()))