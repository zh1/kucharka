import pandas
import csv
import logging

first_page = 0
last_page = 485

tables = ['comment', 'ingredient', 'nutrition', 'recipe', 'step', 'tag']

for table in tables:
    
    concatenated_df = pandas.DataFrame()    
    for i in range(first_page, last_page):
        
        input_file = f'data/{table}{i}.csv'

        input_df = pandas.read_csv(input_file)
        
        concatenated_df = pandas.concat([concatenated_df, input_df], ignore_index=True)

    concatenated_df.to_csv(f'{table}.csv', sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    print(table)