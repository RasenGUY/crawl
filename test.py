from bs4 import BeautifulSoup
import requests
# from schemes import *
from helpers import *
# from tests_parser import *
import re

# Links to extract
    # test with textbox 
        # https://test-english.com/grammar-points/b2/generic-pronouns/3/
    # forms with multiple and single gaps
        # single gaps single options
        # multiple gaps single options
            # https://test-english.com/grammar-points/b1-b2/review-verb-tenses-b1-b2/3/
        # single gaps multiple options
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/
        # multiple gaps multiple options
            # https://test-english.com/grammar-points/b1-b2/review-verb-tenses-b1-b2/

    # form with multiple choice
        # options
            # https://test-english.com/listening/b1-b2/actors-talk-acting/
        # bullets 
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/2/
        # boxes
            # 
    
    # text 
        # gaps with single options
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/3/
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/

        # gaps with multiple options
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/

# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/2/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/3/

headers = {"User-Agent": "Mozilla/75.0"}
pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
req = requests.get('https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/', headers=headers)
page = BeautifulSoup(req.text, 'lxml')

l_selectors = [('.question-content input.watupro-gap', 'gap_option'), ('.question-content select.watupro-gap', 'gap_options'), ('.watu-question .question-choices', 'multiple_c')]

q_struct, q_sel = find_q_struct('.quiz-form .watu-question', page)

# print(q_struct, q_sel)
a_struct = find_a_struct(q_struct, l_selectors, q_sel, page)

print('Question structure: {}, Answer strucre: {}'.format(q_struct, a_struct[0]))

# print(len(page.select('.quiz-form .watu-question')))
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



