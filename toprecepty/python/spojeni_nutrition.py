import pandas as pd

concatenated_df = pd.DataFrame()

for i in range(0, 18):
    
    input_file = f'nutrition{i}.csv'

    input_df = pd.read_csv(input_file)
    
    concatenated_df = pd.concat([concatenated_df, input_df], ignore_index=True)

concatenated_df.to_csv('all_nutrition.csv', index=True)