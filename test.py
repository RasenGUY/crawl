from bs4 import BeautifulSoup
import requests
from schemes import *
from helpers import *
from tests_parser import *
import re

# https://test-english.com/listening/b1-b2/actors-talk-acting/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/2/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/3/

headers = {"User-Agent": "Mozilla/75.0"}
pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
req = requests.get('https://test-english.com/grammar-points/a1/this-that-these-those/3/', headers=headers)
page = BeautifulSoup(req.text, 'lxml')

scheme = level_test_scheme
content = parse_tests_content(page, scheme, test_structs)

print(content)

# parse answers

# print()
# print(content['title'])
# print(content['sub_title'])
# print()
# for i in range(len(content['content']['questions'])):
#     q_num = content['content']['questions'][i][0]
#     q_body = content['content']['questions'][i][-1]

#     print('{} {}'.format(q_num, q_body))
    
#     for j in range(len(content['content']['options'][i])):

#         o_num = content['content']['options'][i][j][0]
#         o_body = content['content']['options'][i][j][-1]
        
#         print('\t {} {}'.format(o_num, o_body))
    
#     print()


