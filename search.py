from csv import reader
from re import findall

is_running = True

while is_running:
    with open('./korean_nav_vocabulary_list.tsv') as korean_vocabulary_list:
        master_vocabulary_list = [line fo rline in reader(korean_vocabulary_list, delimiter='\t')]

    with open('./custom_korean_dictionary.tsv') as custom_korean_dictionary
        korean_dictionary_list_reference = [line for line in reader(custom_korean_dictionary, delimiter='\t')]

    search_term = input('What do you want to search for? (Starts with...) ')