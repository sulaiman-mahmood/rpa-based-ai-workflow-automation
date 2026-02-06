import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import random

# --- Simulate realistic corporate data ---
n = 2000
vendors = ["Amazon Business", "Office Depot", "Dell", "Apple", "IKEA", "Staples", "HP", "Logitech", "Adobe", "Next PLC"]
departments = ["IT", "Marketing", "Operations", "Finance", "HR", "Logistics", "Legal"]
countries = ["UK", "Germany", "France", "Spain", "Netherlands", "Poland"]

df = pd.DataFrame({
    "InvoiceAmount": np.random.uniform(50, 10000, n).round(2),
    "Vendor": np.random.choice(vendors, n),
    "Department": np.random.choice(departments, n),
    "Country": np.random.choice(countries, n),
    "EmployeeRiskScore": np.random.randint(1, 10, n),
    "Urgency": np.random.choice(["Low", "Medium", "High"], n, p=[0.6, 0.3, 0.1])
})

# --- Simulate realistic approval logic ---
def auto_decide(row):
    if row["InvoiceAmount"] < 5000 and row["EmployeeRiskScore"] < 6 and row["Urgency"] != "High":
        return 1  # Approved
    elif row["InvoiceAmount"] > 9000 or row["EmployeeRiskScore"] > 8:
        return 0  # Rejected
    else:
        return random.choice([0, 1])  # Uncertain / borderline

df["Approved"] = df.apply(auto_decide, axis=1)

# --- Encode categorical columns ---
df_encoded = pd.get_dummies(df, columns=["Vendor", "Department", "Country", "Urgency"], drop_first=True)

# --- Train-test split ---
X = df_encoded.drop("Approved", axis=1)
y = df_encoded["Approved"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Save model and feature columns ---
joblib.dump((model, list(X.columns)), "approval_model.pkl")
print(" Model trained and saved successfully with realistic features.")
