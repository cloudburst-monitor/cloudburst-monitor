import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Simple realistic pattern (rain_percent based)
rain = [5,10,15,25,35,45,55,65,75,85,95]
label = [0,0,0,0,1,1,1,1,2,2,2]

df = pd.DataFrame({"rain_percent": rain, "label": label})

model = RandomForestClassifier(n_estimators=50)
model.fit(df[["rain_percent"]], df["label"])

joblib.dump(model, "model.pkl")

print("✅ model.pkl created")