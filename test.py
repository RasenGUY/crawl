
from bs4 import BeautifulSoup
import requests
from tests_parser import *
from helpers import *
import re
from schemes import *


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
        {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0 Chrome/73.0.3683.103", "X-Requested-With": "XMLHttpRequest"}, {"action": "watupro_submit", "quiz_id": "258"}
    ]
] 

req = requests.get('https://test-english.com/listening/b1-b2/actors-talk-acting/', headers=headers[0])

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
# ils = feed_crawler_links('eng_test_links.txt')
# ins = find_pattern_inst(re.compile(rf'https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/4.*'), ils)
# print(ins)

# write parsed questions
print('\n'*2)
for key in content.keys():

    # handle passage
    if key == 'passage':

        if isinstance(content[key], list):
            
            for line in content[key]: 
                
                if line == '\n':
                    pass 
                elif line == '':
                    pass
                else:
                    print(line, end='\n')

            print('\n')
    
    # handle questions
    elif key == 'questions':

        counter = 0
        for question in content[key][0]:

            print(str(counter+1)+ '. ' + question, end='\n')
            
            # if questions multiple choice 
            if len(content[key][-1]) != 0:
                
                p_as = content[key][-1][counter] 
                for i in range(len(p_as)): 
                    
                    if isinstance(p_as, list):
                        
                        p_a = chr(ord('A') + i) + '. ' + p_as[i]
                        
                        print('\t' + p_a, end='\n')
                
                    else:

                        print(p_as)
                
                print('\n')
        
            print('\n')
            
            counter+= 1
    
    elif key == 'sub_title' or key == 'test_title' or key == 'instructions' or key == 'words':

        if content[key] != None: 

            print(key + ': ' + content[key], end='\n')
            print('\n')
    
    # pass parsed answers
    else:

        pass

# write parsed answers
print('\n'*2)

for key in content.keys():

    if key == 'c_answers':

        if content['ca_fb_sct'] == 'ca_multiple_bullets_wf':

            counter = 0
            # store single answers 
            
            for c_answer in content[key][0]:

                # store multiple correct answers  with feedback multiple
                if isinstance(content[key][-1][0], list) != True:
                    
                    c_a = ''
                    if isinstance(c_answer, list):
                    
                        for answer in c_answer:
                                
                            c_a += answer[3:len(answer)] + ', '

                    else:

                        c_a = c_answer[3:len(c_answer)] 
                    
                    print(str(counter + 1) + '. ' + c_a) 
                            
                # store single correct answers 
                else:

                    c_a = str(counter + 1) + '. ' + c_answer
                    
                    print(c_a)
                
                # write if feedback is a list
                if isinstance(content[key][-1][counter], list):
                    
                    for line in content[key][-1][counter]:

                        print('\t' + line)
                
                # write feedback is not list   
                else: 

                    print('\t' + content[key][-1][counter])

                print('\n')
                
                counter += 1
            
        
        elif content['ca_fb_sct'] == 'ca_multiple_normal':
            
            counter = 0
            # print correct answers wf
            for line in content[key][0]:
                
                
                if line[0:1] == '\n':

                    print(str(counter+1) + '. ' + line[1:-1])
                
                else:
                    print(str(counter+1) + '. ' + line)
                
                if line[-1:-2] != '\n':
                    
                    print('\n')

                counter += 1
        
    elif key == 'sub_title' or key == 'test_title' or key == 'instructions' or key == 'words':

        if content[key] != None: 

            print(key + ': ' + content[key], end='\n')
            print('\n')
            
print(content)