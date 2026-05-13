import pandas as pd
import csv
import random
from collections import defaultdict

# import .csv file
def import_csv_to_array(file_path):
    table = []
    # with open(file_path, newline='', encoding='utf-8') as csvfile:
    with open(file_path, newline='', encoding='cp1250') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', skipinitialspace=True)
        for row in reader:
            cleaned_row = [cell.strip() for cell in row if cell.strip()]
            if cleaned_row:
                table.append(cleaned_row)
    return table

# randomize list elements
# def shuffle_list(data):
#     shuffled_data = data[:]
#     random.shuffle(shuffled_data)
#     return shuffled_data
def shuffle_list(data):
    # Grupujemy elementy według drugiego elementu (np. 0, 1, 2...)
    groups = defaultdict(list)
    for item in data:
        key = item[1]
        groups[key].append(item)
    
    # Dla każdej grupy wykonujemy losowe przetasowanie
    for group in groups.values():
        random.shuffle(group)
    
    # Łączymy przetasowane grupy w kolejności rosnącej kluczy
    sorted_keys = sorted(groups.keys(), reverse=True)
    result = []
    for key in sorted_keys:
        result.extend(groups[key])
    
    # Usunięcie drugiego elementu (indeks 1) z każdej podlisty
    shuffled_data = [[item[0], item[2], item[3], item[4], item[5]] for item in result]

    return shuffled_data

file_path = 'preferences_25_D2_v2.csv'
output_file_path = 'assignments_hours_25_T2_D2_v3.csv'

m = 0
group_message = '.'
while group_message != '':
    limits = {}
    assignments_terms = {}
    assignments_groups = {}
    groups_insterted_by_user = []
    groups_insterted_by_user_temp = []
    group_message = ''
    # group_number = int(input("How many groups you want to create? "))
    # terms_number = int(input("How many terms for each group you want to create? ")) 
    # value = int(input(f"Insert limit for groups: "))
    group_number = 4
    terms_number = 2 
    value = 66
    calculated_value_default = value / terms_number
    calculated_value_exception = 27

    for i in range(group_number):
        # key = input("Insert name of group (ex. A, B, C): ")
        calculated_value = calculated_value_default
        if i == 0:
            key = 'A'
        elif i == 1:
            key = 'B'
        elif i == 2:
            key = 'C'
            # calculated_value = calculated_value_exception
        else:
            key = 'D'
        
        for j in range(1, terms_number + 1):
            limits[key + str(j)] = calculated_value
            assignments_groups[key + '*'] = []
            groups_insterted_by_user.append(key)
        # print(limits)
    groups_list = list(limits.keys())
    groups_sum_list = list(assignments_groups.keys())
    for j in range(1, terms_number + 1):
        assignments_terms['*' + str(j)] = []
    terms_list = list(assignments_terms.keys())
    assignments = {option: [] for option in groups_list}
    assignments_count = {option: 0 for option in groups_list}
    assignments_terms_count = {option: 0 for option in terms_list}

    data_array = import_csv_to_array(file_path)
    # print(data_array)

    # add missing prefernces
    for row in data_array:
        groups_insterted_by_user_temp = groups_insterted_by_user
        i = 1
        # print(row)
        while len(row) < 6 and i <= 100:
            groups_insterted_by_user_size = len(groups_insterted_by_user)
            group_random_selection = groups_insterted_by_user[random.randrange(groups_insterted_by_user_size) - 1]
            if group_random_selection not in row:
                row.append(group_random_selection)
            i += 1
        # print(row)

    shuffled_array = shuffle_list(data_array)

    # print(shuffled_array)
    # assign by first preference
    for row in shuffled_array:
        if len(row) == 1:
            sorted_count = dict(sorted(assignments_count.items(), key=lambda item: item[1], reverse=True))
            sorted_list = list(sorted_count.keys())
            current_min = len(assignments[sorted_list[0]])
            current_group = sorted_list[0]
            for group in sorted_list:
                direct_par = random.choice([-1, 1])
                for j in range(1, terms_number + 1)[::direct_par]:
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
                direct_par = random.choice([-1, 1])
                for j in range(1, terms_number + 1)[::direct_par]:
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

    print('Solution #' + str(m + 1) + ': List of people with group count different then: ' + group_message)
    m += 1
    if m == 9999:
        break

# Export assignments to file
assignments_df = pd.DataFrame(assignments)
assignments_df.to_csv(output_file_path, index=False)