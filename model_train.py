import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import random

np.random.seed(42)
random.seed(42)

records = []
for i in range(2500):
    amount = random.randint(100, 2000)
    customer_score = random.randint(1, 10)
    urgency = random.randint(1, 5)

    # Base probability
    base_prob = 0.65

    # Influence factors (stronger signal)
    if amount < 700:
        base_prob += 0.25
    elif amount > 1500:
        base_prob -= 0.25

    if customer_score >= 7:
        base_prob += 0.25
    elif customer_score <= 3:
        base_prob -= 0.25

    if urgency <= 2:
        base_prob += 0.1
    elif urgency >= 4:
        base_prob -= 0.15

    # Add a little randomness (5% noise)
    base_prob += np.random.normal(0, 0.05)
    base_prob = np.clip(base_prob, 0, 1)

    approved = np.random.binomial(1, base_prob)
    records.append([amount, customer_score, urgency, approved])

df = pd.DataFrame(records, columns=["Amount", "CustomerScore", "Urgency", "Approved"])

# Train/test split
X = df[["Amount", "CustomerScore", "Urgency"]]
y = df["Approved"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=6)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "approval_model.pkl")
print("✅ Model trained and saved as approval_model.pkl")
