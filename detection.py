import joblib
import pandas as pd

print("Loading Trained Model...")

model = joblib.load("model.pkl")

print("Model Loaded ✅")

data = pd.read_csv("dataset/processed_data.csv")

sample = data.drop("label", axis=1).iloc[0:5]

print("\n🔍 Running Detection...\n")

predictions = model.predict(sample)

for i, pred in enumerate(predictions):
    if pred == 1:
        print(f"Packet {i+1}: 🚨 ATTACK DETECTED")
    else:
        print(f"Packet {i+1}: ✅ NORMAL TRAFFIC")