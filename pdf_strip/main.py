import fitz
from re import findall
from os import listdir, getcwd
# doc = fitz.open('./ appLaunch  null  ko  verbLabel description updated.pdf')

# for page in doc:
#     text = page.get_text_blocks()
#     for t in text:
#         print(t)

# target = f'{getcwd()}/Korean Ontology'
# print('\n'.join([f for f in listdir(target)]))

def create_line(line_list):
    return '\t'.join(list(map(lambda s: s.strip(), line_list)))

file_path = fitz.open('')

with fitz.open(file_path) as doc:
    content = ''.join([page.get_text() for page in doc])
    content = content.replace(' \n', '\n')

usages = findall('Ex\)\n(.*)\n(.*)\n=(.*)\n', content)
# usages = findall('Ex\)\n(.*)\n=(.*)\n', content)
print(content)

for usage in usages:
    (korean, transliteration, english) = usage
    # (korean, english) = usage
    print(create_line([korean, english]))

# examples = findall('[0-9]\.\n(.*)\n(.*)\n=(.*)\n', content)
examples = findall('[0-9]\.(.*)\n(.*)\n=(.*)\n', content)
# examples = findall('[0-9]\.(.*)\n=(.*)\n', content)


for example in examples:
    (korean, transliteration, english) = example
    # (korean, english) = example
    print(create_line([korean, english]))