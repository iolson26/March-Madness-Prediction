import pandas as pd
data = {
    'Name': ['james', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)

# 2. Write the DataFrame to a CSV file
df.to_csv('output_data.csv')


new_row = pd.DataFrame([{
    "Name": "Dave",
    "Age": 27,
    "City": "Houston"
}])

new_row.to_csv(
    "output_data.csv",
    mode="a",
    index=False,
    header=False
)

