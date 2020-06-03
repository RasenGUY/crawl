
from bs4 import BeautifulSoup
import requests
from tests_parser import *
from helpers import *
import re
from schemes import *
from urllib import parse
import os

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
        # note (does not contain correct answers)
    
    # not done completely
        # https://test-english.com/writing/b1-b2/narrative-writing-step-by-step/2/ 
        # https://test-english.com/writing/b1-b2/formal-email-letter-asking-information/4/
        # https://test-english.com/reading/b1/ebay-tips-selling-successfully/
        # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/
            # check correct answers 
        # https://test-english.com/grammar-points/a2/however-although-time-connectors/3/
            # check correct answers 
# some notes for parsing answers
    # forms of feedback
        # bullet form 
        #     


headers = [
    {"User-Agent": "Mozilla/75.0"}, 
    [
        {"User-Agent": "Mozilla/75.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": "258"}
    ]
] 

# 'https://test-english.com/staging01/wp-content/uploads/Verb-tenses-summary-B1-B2.png'
# https://test-english.com/staging01/wp-content/uploads/Questions-word-order.new_.png


link = 'https://test-english.com/level-test/'
p_link = parse.urlparse(link)
req = requests.get(link, headers=headers[0])


# soup = BeautifulSoup(req.text, 'html.parser')

# imgs = soup.select('#explanation img')
# pattern = re.compile(r'(?<=.)(-(\d{1,4}x\d{1,4})(?=\.))')

# if len(imgs) != 0:

#     counter = 0
#     for img in imgs:
        
#         img_link = img['data-wpfc-original-src']
#         print(img_link)
#         match = pattern.search(img_link)
        
#         if match != None:
        
#             img_link = img_link.replace(match.group(), '').replace('/website18', '')
        
        
#         req = requests.get(img_link, headers=headers[0])

        
#         with open('img-'+ str(counter+1) + '.png', 'wb') as img:
            
#             print('saving image: {}'.format(img_link))
#             img.write(req.content)
        
#         counter += 1 



q_page = BeautifulSoup(req.text, 'html.parser')


# get quiz id
q_id = retr_q_id(q_page.select('.quiz-form')[0])
headers[-1][-1]['quiz_id'] = q_id
payload = headers[-1][-1]


post_link = 'https://test-english.com/staging01/wp-admin/admin-ajax.php'
req = requests.post(post_link, data=payload, headers=headers[0])

ca_page = BeautifulSoup(req.text, 'lxml')

content = parse_tests_content(q_page, ca_page, general_scheme)

# print(content['passage'])
# post_link = 'https://www.easymp3converter.com/models/convertProcess.php'
# audio_link = get_audio_link(q_page, listening_scheme)

# payload = {'search_txt': audio_link}

# hdrs = {'User-Agent': 'Mozilla/75.0'}
# req = requests.post(post_link, data=payload, headers=headers[-1][0])

# ad_page = BeautifulSoup(req.text, 'lxml')
 
# d_links = ad_page.find_all('option')
# d_link = None

# for link in d_links:
    
#     if  link.get_text() == 'mp3\xa0128kbps':
#         d_link = 'https:' + link.attrs['data-link']

# print(d_link)

# create filename
f_qs = '/' + content['test_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-QUESTIONS' + '.txt'
f_as = '/' + content['test_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-ANSWERS' + '.txt'
f_ex = '/' + content['test_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-EXPLS' + '.txt'

# get folder path 
f_path = os.path.dirname('/home/rasguy92/Downloads/' + 'tests' + str(p_link.path))


# write_questions(f_path, f_qs, content)
# write_answers(f_path, f_as, content)
# write_explanations(f_path, f_ex, content)
