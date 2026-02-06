import pandas as pd
import random
from datetime import datetime
import os

output_dir = "Input"
os.makedirs(output_dir, exist_ok=True)

records = []
for i in range(100):
    records.append({
        "RequestID": f"REQ-{1000+i}",
        "Amount": random.randint(100, 2000),
        "CustomerScore": random.randint(1, 10),
        "Urgency": random.randint(1, 5)
    })

df = pd.DataFrame(records)
filename = f"{output_dir}/requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(filename, index=False)
print(f"✅ Created {filename}")
