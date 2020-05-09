from bs4 import BeautifulSoup
import requests
from schemes import *
from helpers import *
import re
headers = {"User-Agent": "Mozilla/75.0"}
pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
req = requests.get('https://test-english.com/grammar-points/b1/present-simple-present-continuous/', headers=headers)
page = BeautifulSoup(req.text, 'lxml')




# def scrape_test_content(page, scheme):

scheme = test_scheme
content = dict()

    # struct_type = find_page_struct(page, test_structs) 
    # scrape multiple choice questions
    # if struct_type == 'multiple-c':

for s_key in scheme.keys():
    struct = 'g-w-o'

    if s_key == 'title' or s_key == 'sub_title':
        
        content[s_key] = page.select(scheme[s_key])[0].get_text().strip()
    
    elif s_key == 'content': 
        
        content[s_key] = {}
        for c_key in scheme[s_key].keys(): 

            # ------------------------- parse multiple choice questions tests

            # parse questios
            if c_key == 'questions' and struct == 'multiple-c':
                content[s_key][c_key] = [
                    [   # get question number
                        ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                        # get question content
                        tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
                    ] 
                    for tag in page.select(scheme[s_key][c_key])
                    ]

            # parse possible answers 
            elif c_key == 'options' and struct == 'multiple-c':
                content[s_key][c_key] = [
                                    [
                                [   # get option number
                                    ''.join(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip())[0]),
                                    # get option content
                                    ''.join(option.get_text().encode('ascii', 'ignore').decode().split(''.join(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip()))+''))
                                ]
                                for option in options.select(scheme[s_key][c_key][-1])
                            ]

                            for options in page.select(scheme[s_key][c_key][0])
                            ]


            # --------------------- parse gap answers with options -----------------------
            # parse questions  
            if c_key == 'questions' and struct == 'g-w-o':

                content[s_key][c_key] = [
                                [   # get question number
                                    ''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                                    # join all options in the text into one string and remove them from the question and remove number
                                    questions.get_text().encode('ascii', 'ignore').decode().strip().replace(''.join([question.get_text() for question in questions.select(scheme['content']['options'][-1]) if question.get_text() != '']), '_'*5).strip(''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())))

                                ]
                                    # parse questions from documents
                                    for questions in page.select(scheme[s_key][c_key])
                            ]

            # parse possible answers 
            elif c_key == 'options' and struct == 'g-w-o':
                
                content[s_key][c_key] = [
                                [   # parse all option in column retrieve text 
                                    option.get_text() for option in column.select(scheme[s_key][c_key][-1]) if option.get_text() != ''
                                ]
                            # parse all option columms
                            for column in page.select(scheme[s_key][c_key][0])
                            ]
            # --------------------- parse gap tests with single answers -----------------------
            # parse questions  
            if c_key == 'questions' and struct == 'g-w-s':

                content[s_key][c_key] = [
                                [   # get question number
                                    ''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
                                    # join all options in the text into one string and remove them from the question and remove number
                                    questions.get_text().encode('ascii', 'ignore').decode().strip().replace(''.join([question.get_text() for question in questions.select(scheme['content']['options'][-1]) if question.get_text() != '']), '_'*5).strip(''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())))

                                ]
                                    # parse questions from documents
                                    for questions in page.select(scheme[s_key][c_key])
                            ]

            # parse possible answers 
            elif c_key == 'options' and struct == 'g-w-s':
                
                content[s_key][c_key] = [
                                [   # parse all option in column retrieve text 
                                    option.get_text() for option in column.select(scheme[s_key][c_key][-1]) if option.get_text() != ''
                                ]
                            # parse all option columms
                            for column in page.select(scheme[s_key][c_key][0])
                            ]

print(content)           








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


