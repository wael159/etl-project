import json
import pandas as pd
import transform_components

# Load data
df = pd.read_csv('extracted_data.csv')

# Load config
with open('config.json') as f:
    config = json.load(f)

# Apply transformations
for step in config['transformations']:
    condition = step.get('condition')
    if condition:
        # Evaluate the condition in the context of the current DataFrame
        if not eval(condition, {}, {'df': df}):
            continue  # Skip this transformation if condition is False
    func = getattr(transform_components, step['name'])
    params = step.get('params', {})
    df = func(df, **params)

# Save cleaned data
df.to_csv('cleaned_data.csv', index=False)
print("Transformation complete. Data saved to cleaned_data.csv") 