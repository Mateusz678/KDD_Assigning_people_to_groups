import pandas as pd
import csv
import random

limits = {}
assignments_terms = {}
assignments_groups = {}
group_number = int(input("How many groups you want to create? "))
terms_number = int(input("How many terms for each group you want to create? ")) 
value = int(input(f"Insert limit for groups: "))

for i in range(group_number):
    key = input("Insert name of group (ex. A, B, C): ")
    for j in range(1, terms_number + 1):
        limits[key + str(j)] = value / terms_number
        assignments_groups[key + '*'] = []

groups_list = list(limits.keys())
groups_sum_list = list(assignments_groups.keys())
for j in range(1, terms_number + 1):
    assignments_terms['*' + str(j)] = []
terms_list = list(assignments_terms.keys())
assignments = {option: [] for option in groups_list}
assignments_count = {option: 0 for option in groups_list}
assignments_terms_count = {option: 0 for option in terms_list}
file_path = 'preferences_D2.csv'

# import .csv file
def import_csv_to_array(file_path):
    table = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', skipinitialspace=True)
        for row in reader:
            cleaned_row = [cell.strip() for cell in row if cell.strip()]
            if cleaned_row:
                table.append(cleaned_row)
    return table

# randomize list elements
def shuffle_list(data):
    shuffled_data = data[:]
    random.shuffle(shuffled_data)
    return shuffled_data

data_array = import_csv_to_array(file_path)
shuffled_array = shuffle_list(data_array)

# assign by first preference
for row in shuffled_array:
    if len(row) == 1:
        sorted_count = dict(sorted(assignments_count.items(), key=lambda item: item[1], reverse=True))
        sorted_list = list(sorted_count.keys())
        current_min = len(assignments[sorted_list[0]])
        current_group = sorted_list[0]
        for group in sorted_list:
            for j in range(1, terms_number + 1):
                if (len(assignments[group]) < current_min and row[0] not in assignments_terms['*' + str(j)] and row[0] not in assignments_groups[group[0] + '*'] and len(assignments[group]) < limits[group]):
                    current_min = len(assignments[group])
                    current_group = group
                if row[0] not in assignments_terms['*' + str(j)] and row[0] not in assignments_groups[current_group[0] + '*'] and len(assignments[group]) < limits[group]:
                    assignments[current_group].append(row[0])   
                    assignments_terms['*' + str(j)].append(row[0])  
                    assignments_groups[current_group[0] + '*'].append(row[0])  
                    assignments_count[current_group] += 1
    elif len(row) > 1:
        i = 1
        while (i < len(row)):
            for j in range(1, terms_number + 1):
                if row[i] + str(j) in groups_list:
                    pref = row[i] + str(j)
                    if len(assignments[pref]) < limits[pref] and row[0] not in assignments_terms['*' + str(j)] and row[0] not in assignments_groups[row[i] + '*']:
                        assignments[pref].append(row[0])
                        assignments_terms['*' + str(j)].append(row[0])   
                        assignments_groups[row[i][0] + '*'].append(row[0])   
                        assignments_count[pref] += 1  
            i += 1

# set the same lenght to each list
max_length = max(len(people) for people in assignments.values())
for key in assignments.keys():
    while len(assignments[key]) < max_length:
        assignments[key].append('')

# find people with group count different then 2
group_message = ''
for row in data_array:
    i = 0
    current_person_group_list = ''
    for group in groups_list:
        if row[0] in assignments[group]:
            i += 1
            current_person_group_list = current_person_group_list + group
    if i != 2:
        group_message = group_message + row[0] + ':' + current_person_group_list + '; '

print('List of people with group count different then 2: ' + group_message)

# Export assignments to file
assignments_df = pd.DataFrame(assignments)
assignments_df.to_csv('assignments_hours_D2_v1.csv', index=False)