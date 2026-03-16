import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("Loading Dataset...")

data = pd.read_csv("dataset/kddcup.data_10_percent_corrected", header=None)

columns = [f"feature_{i}" for i in range(41)] + ["label"]
data.columns = columns

print("Dataset Loaded Successfully ✅")

# Convert label
data['label'] = data['label'].apply(lambda x: "normal" if x == "normal." else "attack")

print("Labels Converted ✅")

# 🚀 FORCE ENCODE IMPORTANT CATEGORICAL COLUMNS
categorical_columns = ['feature_1', 'feature_2', 'feature_3', 'label']

encoder = LabelEncoder()

for column in categorical_columns:
    data[column] = encoder.fit_transform(data[column])

print("Categorical Data Encoded ✅")

# Save dataset
data.to_csv("dataset/processed_data.csv", index=False)

print("Preprocessing Completed Successfully 🚀")