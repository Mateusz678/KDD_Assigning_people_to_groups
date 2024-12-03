import pandas as pd
import csv
import random

limits = {}
group_number = int(input("How many groups you want to create? "))
for i in range(group_number):
    key = input("Insert name of group (ex. A, B, C): ")
    value = int(input(f"Insert limit for group '{key}': "))
    limits[key] = value

groups_list = list(limits.keys())
assignments = {option: [] for option in groups_list}
assignments_count = {option: 0 for option in groups_list}
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
            if (len(assignments[group]) < current_min and row[0] not in assignments[group] and len(assignments[group]) < limits[group]):
                current_min = len(assignments[group])
                current_group = group
        if row[0] not in assignments[current_group]:
            assignments[current_group].append(row[0])   
            assignments_count[current_group] += 1
    elif len(row) > 1:
        i = 1
        while (i < len(row)):
            if row[i] in groups_list:
                pref = row[i]
                if len(assignments[pref]) < limits[pref]:
                    assignments[pref].append(row[0])   
                    assignments_count[pref] += 1
                    break         
            i += 1

# assign by second preference
for row in shuffled_array[::-1]:
    if len(row) == 1 or len(row) == 2:
        sorted_count = dict(sorted(assignments_count.items(), key=lambda item: item[1], reverse=True))
        sorted_list = list(sorted_count.keys())
        current_min = len(assignments[sorted_list[0]])
        current_group = sorted_list[0]
        for group in sorted_list:
            if (len(assignments[group]) < current_min and row[0] not in assignments[group] and len(assignments[group]) < limits[group]):
                current_min = len(assignments[group])
                current_group = group
        if (row[0] not in assignments[current_group] and len(assignments[current_group]) < limits[current_group]):
            assignments[current_group].append(row[0])   
            assignments_count[current_group] += 1
    elif len(row) > 2:
        i = 2
        while (i < len(row)):
            if row[i] in groups_list:
                pref = row[i]
                if len(assignments[pref]) < limits[pref] and row[0] not in assignments[pref]:
                    assignments[pref].append(row[0])
                    assignments_count[pref] += 1
                    break         
            i += 1

# assign people who has less then 2 assignments
for row in shuffled_array[::-1]:
    i = 0
    for group in groups_list:
        if row[0] in assignments[group]:
            i += 1
    if i < 2:
        sorted_count = dict(sorted(assignments_count.items(), key=lambda item: item[1], reverse=True))
        sorted_list = list(sorted_count.keys())
        current_min = len(assignments[sorted_list[0]])
        current_group = sorted_list[0]
        for group in sorted_list:
            if (len(assignments[group]) < current_min and row[0] and len(assignments[group]) < limits[group]):
                current_min = len(assignments[group])
                current_group = group
            if (row[0] not in assignments[current_group] and len(assignments[current_group]) < limits[current_group]):
                assignments[current_group].append(row[0])   
                assignments_count[current_group] += 1
                break

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
assignments_df.to_csv('assignments_D2_v1.csv', index=False)