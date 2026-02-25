import pandas as pd

df = pd.DataFrame(columns=["Name", "Age", "City"])
df.to_csv("output_data.csv", index=False)

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