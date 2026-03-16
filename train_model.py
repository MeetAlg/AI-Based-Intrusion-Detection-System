import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

print("Loading Processed Dataset...")

# Load processed data
data = pd.read_csv("dataset/processed_data.csv")

print("Dataset Loaded ✅")

# Features & Label
X = data.drop("label", axis=1)
y = data["label"]

print("Splitting Dataset...")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print("Training Model...")

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

print("Model Trained ✅")

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("\n🔥 MODEL RESULTS 🔥")
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", cm)

# Save Model
joblib.dump(model, "model.pkl")

print("\nModel Saved Successfully ✅")