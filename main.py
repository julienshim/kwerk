from csv import reader, writer
from re import findall
from datetime import datetime

# options
is_running = True

while is_running:
    # master_list
    with open('./korean_nav_vocabulary_list.tsv') as korean_vocabulary_list:
        master_vocabulary_list = [line for line in reader(korean_vocabulary_list, delimiter='\t')]

    # korean_dictionary_list_reference
    with open('./custom_korean_dictionary.tsv') as custom_korean_dictionary:
        korean_dictionary_list_reference = [line for line in reader(custom_korean_dictionary, delimiter='\t')]

    # functions
    def korean_regex(string):
        return ''.join(findall(r'[\uac00-\ud7a3]', string))

    def find_duplicates(string):
        pass

    def determine_conversion(string):
        try:
            string = int(string)
        except ValueError:
            string = string.lower()
        return string


    # target_day_selection
    valid_days = []
    for line in master_vocabulary_list[1:]:
        if line[0] not in valid_days:
            valid_days.append(line[0])

    target_day_selection = input('What day would you like to view? (Type number or Q to "Quit") ') 

    while target_day_selection not in valid_days and target_day_selection not in ['q', 'quit']:
        target_day_selection = input('Selection not in range. What day would you like to view? ')

    target_day_indexes = []

    if target_day_selection in valid_days:

        is_selecting = True

        while is_selecting:

            # display
            print(f'\n**** Day {target_day_selection} Vocabulary ****')
            for index, line in enumerate(master_vocabulary_list):
                [day, frequency, korean, pos, hanja, english, english2, hint, level, percentage] = line
                if day == target_day_selection:
                    print(f'{index}: {[day, frequency, korean, pos, hanja, english, english2, hint, level, percentage]}')
                    target_day_indexes.append(index)

            # selected_vocabulary
            selected_vocabulary_index = determine_conversion(input(f'\nWhat word you like to define? (Type index, X to "Cancel", or Q to "Quit") '))

            while selected_vocabulary_index not in target_day_indexes and selected_vocabulary_index not in ['x', 'X', 'q', 'Q']:
                selected_vocabulary_index = determine_conversion(input(f'Selection not in range. What word you like to define? (Type index, X to "Cancel", or Q to "Quit") '))

            is_defining = True

            while is_defining:
            
                if selected_vocabulary_index in target_day_indexes:

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

                        definition_selection = determine_conversion(input(f'\nHow would you like to define {selected_vocabulary[2]}? (Type index, X to "Cancel", or Q to "Quit") '))

                        while definition_selection not in target_definition_indexes and definition_selection not in ['x', 'X', 'q', 'Q']:
                            definition_selection = determine_conversion(input (f'Selection not in range. How would you like to define {selected_vocabulary[2]}? (Type index, X to "Cancel", or Q to "Quit") '))

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
                                print('SAVING CHANGES...')
                                master_vocabulary_list[selected_vocabulary_index] = [day, frequency, korean, pos, hanja, english_c, english2_c, hint, level, 'TRUE']
                                print('WRITING CHANGES...')
                                with open('./korean_nav_vocabulary_list.tsv', 'w') as output:
                                    tsv_writer = writer(output, delimiter='\t')
                                    for line in master_vocabulary_list:
                                        tsv_writer.writerow(line)
                                print(f'SAVED: {master_vocabulary_list[selected_vocabulary_index]}')
                                is_defining = False

                        elif definition_selection in ['x', 'X']:
                            print('Selection Skipped.')
                            is_defining = False

                        elif definition_selection in ['q', 'Q']:
                            is_selecting = False
                            is_defining = False
                            is_running_day = False
                            is_running = False

                elif selected_vocabulary_index in ['x', 'X']:
                    is_selecting = False
                    is_defining = False
                    is_running_day = False

                elif selected_vocabulary_index in ['q', 'Q']:
                    is_selecting = False
                    is_defining = False
                    is_running_day = False
                    is_running = False

    elif target_day_selection.lower() in ['q', 'Q']:
        is_selecting = False
        is_defining = False
        is_running_day = False
        is_running = False


print('QUITTING...')

now = datetime.now()
dt_string = now.strftime("%Y-%d-%m_%H.%M.%S")

print('CREATING BACKUP...')

with open(f'./backup/korean_nav_vocabulary_list_{dt_string}.tsv', 'w') as output:
    tsv_writer = writer(output, delimiter='\t')
    for line in master_vocabulary_list:
        tsv_writer.writerow(line)

print('BACKUP CREATED')
    
print('SEE YOU TOMORROW!\n')
