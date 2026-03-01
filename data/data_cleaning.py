import pandas as pd

files = ['daily_sales_data_0.csv', 'daily_sales_data_1.csv', 'daily_sales_data_2.csv']
df_list = []

for file in files:
    df = pd.read_csv(file)
    df = df[df['product'] == 'pink morsel'].copy()
    df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
    df['sales'] = df['price'] * df['quantity']
    df = df[['sales', 'date', 'region']]
    df_list.append(df)

final_df = pd.concat(df_list, ignore_index=True)

output_filename = 'formatted_morsel_data.csv'
final_df.to_csv(output_filename, index=False)

print(f"Shape of final data: {final_df.shape}")
print("First 5 rows:")
print(final_df.head())