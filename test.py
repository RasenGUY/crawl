from bs4 import BeautifulSoup
import requests
from schemes import *
from helpers import *
from tests_parser import *
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
            # 
    
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

headers = {"User-Agent": "Mozilla/75.0"}
# pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
req = requests.get('https://test-english.com/grammar-points/a2/however-although-time-connectors/', headers=headers)
page = BeautifulSoup(req.text, 'lxml')


questions = page.select(g_quest_sel)
q_struct = find_q_struct(g_quest_sel, page)
a_struct = find_a_struct(q_struct[0], q_selectors, g_quest_sel, page)

# # def parse_q_and_a(q_struct, a_struct, q_sel, a_sel, page):
#     # '''
#     # helper function for parsing form or text data from a target tests page
#     # '''
    
parsed_q = []
parsed_a = []
print(q_struct)
print(a_struct)


# parse all of the questions of the page and remove the numbers
questions = page.select(g_quest_sel)

for question in questions:
    
    if q_struct[0] == 'form':
        
        # remove number from questions
        question.select('.watupro_num')[0].clear()

        # ----------------- parse form  questions and answers -------------------
    
        # replace inputs and parse answers if gap_options or gap_option
        if a_struct[0] == 'gap_option' or a_struct[0] == 'gap_options':
            
            # replace inputs with literal gap string
            inputs = question.select(a_struct[-1])
            
            if a_struct == 'gap_option': 
                new_soup = rem_soup_ins_re(inputs, question, '_'*5)
            else:
                new_soup = rem_soup_ins_re(inputs, question, '_'*2)
            
            # parse questions with one gap or more gaps
            parsed_q.append(new_soup.get_text().encode('ascii', 'ignore').decode().strip())
        
            # parse answers unless gap_option
            if a_struct[0] == 'gap_options':

                parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1]) if answer.get_text() != ''])         
                
        else:
            
            # parse questions 
            if question.select(q_struct[-1])[0].get_text().rfind('\xa0') != -1:
            
                parsed_q.append(question.select(q_struct[-1])[0].get_text().encode('ascii', 'ignore').decode().strip())
            else:
                parsed_q.append(question.select(q_struct[-1])[0].get_text().strip())

            # --------------- parse form answers -------------
        
            # remove bullets for answers with bullet points
            if a_struct[0] == 'multiple_c_bullets':
                
                for answer_n in question.select('i'):
                    
                    answer_n.clear()
                    
            parsed_a.append([answer.get_text().encode('ascii', 'ignore').decode().strip() for answer in question.select(a_struct[-1])])


    elif q_struct[0] == 'text' or q_struct[0] == 'dialogue':
        
        text = question

        # number of questions 
        q_number = len(text.select('.numBox'))
        answers = text.select(a_struct[-1])
        
        # store answers if options
        if a_struct[0] == 'gap_options':

            parsed_a.append([[option.get_text() for option in answer if option.get_text() != ''] for answer in answers])

        # replace numbox with gap
        for num_box in text.select('.numBox'):
        
            num_box.string.replace_with("_"*3 + num_box.get_text() + "_"*3)

        # remove inputs or select
        for answer in answers:
            answer.clear() 

        if q_struct[0] == 'text': 
            
            # parse questions
            for paragraph in text.select(q_struct[-1]):
            
                if paragraph.get_text().rfind('\xa0') != -1:
                
                    parsed_q.append(paragraph.get_text().encode('ascii', 'ignore').decode().strip())
                else:
                    parsed_q.append(paragraph.get_text().strip())

        else:
            
            # parse questions
            for line in text.find_all(['h4', 'p']):
                
                if line.get_text().rfind('\xa0') != -1:
                
                    parsed_q.append(line.get_text().encode('ascii', 'ignore').decode().strip())

                else:
                    parsed_q.append(line.get_text().strip())

        

            
# print(q_number)
print(parsed_q)
print(parsed_a)




































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



