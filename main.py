from csv import reader, writer
from re import findall
from datetime import datetime

# options
is_showing_english = True
is_running = True
is_running_day = True

while is_running:
    # master_list
    with open('./korean_nav_vocabulary_list.tsv') as korean_vocabulary_list:
        master_vocabulary_list = [line for line in reader(korean_vocabulary_list, delimiter='\t')]

    # korean_dictionary_list_reference
    with open('./custom_korean_dictionary.tsv') as custom_korean_dictionary:
        korean_dictionary_list_reference = [line for line in reader(custom_korean_dictionary, delimiter='\t')]

    # target_day
    valid_days = []
    for line in master_vocabulary_list[1:]:
         if line[0] not in valid_days:
             valid_days.append(line[0])
    target_day = input('What day would you like to view? ')
    while target_day not in valid_days:
        target_day = input('Selection not in range. What day would you like to view? ')
    target_day_indexes = []

    # functions
    def korean_regex(string):
        return ''.join(findall(r'[\uac00-\ud7a3]', string))

    def find_duplicates(string):
        pass

    while is_running_day:
        # display
        print(f'\n**** Day {target_day} Vocabulary ****')
        for index, line in enumerate(master_vocabulary_list):
            [day, frequency, korean, pos, hanja, english, english2, hint, level, percentage] = line
            if day == target_day:
                print(f'{index}: {[day, frequency, korean, pos, hanja, english if is_showing_english else "", english2 if is_showing_english else "", hint, level, percentage]}')
                target_day_indexes.append(index)

        # selected_vocabulary
        selected_vocabulary_index = int(input(f'\nWhat word you like to define? (Select Index) '))
        if selected_vocabulary_index not in target_day_indexes:
            selected_vocabulary_index = int(input(f'Selection not in range. What word you like to define? (Select Index {target_day_indexes[0]}-{target_day_indexes[-1]}) '))
        selected_vocabulary = master_vocabulary_list[selected_vocabulary_index]
        print('\n**** ENTRY ****')
        print(selected_vocabulary)

        # selected_vocabulary_duplicates
        for index, line in enumerate(master_vocabulary_list):
            [day, frequency, korean, pos, hanja, english, english2, hint, level, percentage] = line
            if index != selected_vocabulary_index and korean_regex(selected_vocabulary[2]) == korean_regex(korean):
                print(f'    WARNING --> {line}')

        # definitions
        target_definition_indexes = []
        print('\n**** DEFINITIONS ****')
        for index, entry in enumerate(korean_dictionary_list_reference):
            [vocabulary, vocabulary_type, pos, hanja, level, meaning, english1, english2] = entry
            if korean_regex(vocabulary).startswith(korean_regex(selected_vocabulary[2])) and selected_vocabulary[3] in pos:
                target_definition_indexes.append(index)
                print(f'{index}: {[vocabulary, pos, hanja, english1, english2]}')

        definition_selection = int(input(f'\nHow would you like to define {selected_vocabulary[2]}? (Select Index or type S to "Skip") '))

        while definition_selection not in target_definition_indexes and definition_selection != 's':
             definition_selection = int(input (f'Selection not in range. How would you like to define {selected_vocabulary[2]}? (Select Index or type S to "Skip") '))

        if definition_selection in target_definition_indexes:
            [day, frequency, korean, pos, hanja, english, english2, hint, level, percentage] = master_vocabulary_list[selected_vocabulary_index]
            [vocabulary_c, vocabulary_type_c, pos_c, hanja_c, level_c, meaning_c, english_c, english2_c] = korean_dictionary_list_reference[definition_selection]
            pre = ''
            if pos == '동사':
                pre = 'to '
            elif pos == '형용사':
                pre = 'to be '
            english_c = pre + english_c
            print(f'\nBEFORE: {[frequency, korean, pos, hanja, english, english2, hint, level]}')
            print(f'AFTER: {[frequency, korean, pos, hanja, english_c, english2_c, hint, level]}')

            confirmation_input = input('\nWould you like to make the above changes? (Y/N) ')

            while confirmation_input.lower() not in ['y', 'yes', 'n', 'no']:
                confirmation_input = input('Sorry, didn\'t get your selection. Would you like to make the above changes? (Y/N) ')

            if confirmation_input.lower() in ['y', 'yes']:
                master_vocabulary_list[selected_vocabulary_index] = [day, frequency, korean, pos, hanja, english_c, english2_c, hint, level, 'TRUE']
                print('SAVING CHANGES...')
                with open('./korean_nav_vocabulary_list.tsv', 'w') as output:
                    tsv_writer = writer(output, delimiter='\t')
                    for line in master_vocabulary_list:
                        tsv_writer.writerow(line)
                print(f'SAVED: {master_vocabulary_list[selected_vocabulary_index]}')
        
        elif definition_selection.lower() == 's':
            print('Selection Skipped.')

        is_running_day_selection = input(f'\nWould you like to define another word from Day {target_day}? (Y/N) ')
        
        while is_running_day_selection.lower() not in ['y', 'yes', 'n', 'no']:
            is_running_day_selection = input(f'Sorry, didn\'t get your selection. Would you like to define another work from Day {target_day}? (Y/N) ')

        if is_running_day_selection.lower() in ['n', 'no']:
            is_running_day = False
    
    is_running_selection = input('\nWould you like to select another day\'s vocabulary list? (Y/N) ')

    while is_running_selection.lower() not in ['y', 'yes', 'n', 'no']:
        is_running_selection = input(f'Sorry, didn\'t get your selection. Would you like to select another day? ')

    if is_running_selection.lower() in ['y', 'no']:
        target_day = input('What day would you like to view? ')
        while target_day not in valid_days:
            target_day = input('Selection not in range. What day would you like to view? ')
        target_day_indexes = []

    if is_running_selection.lower() in ['n', 'no']:
        is_running = False

print('SAVING VOCABULARY LIST...')

with open('./korean_nav_vocabulary_list.tsv', 'w') as output:
    tsv_writer = writer(output, delimiter='\t')
    for line in master_vocabulary_list:
        tsv_writer.writerow(line)

now = datetime.now()
dt_string = now.strftime("%Y-%d-%m_%H.%M.%S")

print('CREATING BACKUP...')

with open(f'./backup/korean_nav_vocabulary_list{dt_string}.tsv', 'w') as output:
    tsv_writer = writer(output, delimiter='\t')
    for line in master_vocabulary_list:
        tsv_writer.writerow(line)
    
print('SEE YOU TOMORROW!\n')
