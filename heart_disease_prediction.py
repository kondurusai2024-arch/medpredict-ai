import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -------------------------------
# 1. Load Dataset
# -------------------------------
df = pd.read_csv("heart.csv")

print("First 5 Rows:")
print(df.head())

print("\nDataset Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())

# -------------------------------
# 2. One-hot encode categorical columns
# -------------------------------
df_encoded = pd.get_dummies(df, columns=['cp', 'restecg', 'thal'], drop_first=True)

print("\nEncoded Columns:")
print(df_encoded.columns.tolist())

# -------------------------------
# 3. Split Features and Target
# -------------------------------
X = df_encoded.drop("target", axis=1)
y = df_encoded["target"]

# Save training columns
training_columns = X.columns.tolist()

# -------------------------------
# 4. Train Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 5. Scaling
# -------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------
# 6. Train Model
# -------------------------------
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# -------------------------------
# 7. Evaluate
# -------------------------------
y_pred = model.predict(X_test_scaled)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# -------------------------------
# 8. Save model, scaler, columns
# -------------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
pickle.dump(training_columns, open("columns.pkl", "wb"))

print("\n✅ model.pkl, scaler.pkl, columns.pkl saved successfully!")

# -------------------------------
# 9. Print one sample for testing
# -------------------------------
print("\n==============================")
print("Heart Disease Sample (target = 1):")
print(df[df["target"] == 1].head(1).to_string(index=False))

print("\n==============================")
print("No Heart Disease Sample (target = 0):")
print(df[df["target"] == 0].head(1).to_string(index=False))