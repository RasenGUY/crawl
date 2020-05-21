from bs4 import BeautifulSoup
import requests
from tests_parser import *
from helpers import *
import re

# Links to extract
    # test with textbox 
        # https://test-english.com/grammar-points/b2/generic-pronouns/3/
    # test with example 
        # https://test-english.com/grammar-points/a2/asking-questions-in-english/4/

    # forms with multiple and single gaps
        # single gaps single options
            # https://test-english.com/grammar-points/a2/infinitives-and-gerunds/3/
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
            # https://test-english.com/writing/b1-b2/narrative-writing-step-by-step/
    # text 
        # gaps with single options
            # https://test-english.com/grammar-points/a2/however-although-time-connectors/3/

        # gaps with multiple options
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/
            # https://test-english.com/grammar-points/b1-b2/present-perfect-simple-continuous/
    
    # dialogue
        # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/


# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/2/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/3/

# special pages
    # writing (special cases)(done)
        # https://test-english.com/writing/b1-b2/for-against-essay-argumentative-writing/2/
    
    # not done completely
        # https://test-english.com/writing/b1-b2/narrative-writing-step-by-step/2/ 
        # https://test-english.com/writing/b1-b2/formal-email-letter-asking-information/4/
        # https://test-english.com/reading/b1/ebay-tips-selling-successfully/

# some notes for parsing answers
    # forms of feedback
        # bullet form 
        #     


headers = [
    {"User-Agent": "Mozilla/75.0"}, 
    [
        {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": "258"}
    ]
] 

req = requests.get('https://test-english.com/listening/b1/stonehenge/', headers=headers[0])

page = BeautifulSoup(req.text, 'lxml')
q_struct = find_q_struct(g_quest_sel, page)

# get quiz id
q_id = retr_q_id(page.select('.quiz-form')[0])
headers[-1][-1]['quiz_id'] = q_id
payload = headers[-1][-1]
post_link = 'https://test-english.com/staging01/wp-admin/admin-ajax.php'

req = requests.post(post_link, data=payload, headers=headers[-1][0])

page = BeautifulSoup(req.text, 'lxml')

parse_tests_answers(q_struct[0], page)


# all parsed content
# parsed_c = parse_tests_content(page)
# print(parsed_c[0])
# print(parsed_c[1])
# print(parsed_c[2])


































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



