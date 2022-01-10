from csv import reader, writer
from re import findall
from datetime import datetime

with open('./korean_nav_vocabulary_list.tsv') as korean_nav_vocabulary_list:
    master_vocabulary_list = [line for line in reader(korean_nav_vocabulary_list, delimiter='\t')]

output_vocabulary = []
output_days = []

def korean_regex(string):
    return ''.join(findall(r'[\uac00-\ud7a3]', string))

for line in master_vocabulary_list:
    [day, frequency, korean, pos, hanja, english, english2, hint, level, percentage] = line
    if english != '':
        if day.isdigit() and day not in output_days:
            output_days.append(day)
        korean = korean_regex(korean)
        output_vocabulary.append([day, korean, english, english2, hanja, pos])

for d in output_days:
    with open(f'./vocabulary_lists/Day_{d}_Vocabulary_List.tsv', 'w') as output:
        tsv_writer = writer(output, delimiter='\t')
        tsv_writer.writerow(['day', 'korean', 'english', 'english2', 'hanja', 'pos'])
        for line in output_vocabulary:
            [day, korean, english, english2, hanja, pos] = line
            if d == day:
                tsv_writer.writerow(line)