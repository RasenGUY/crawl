from bs4 import BeautifulSoup
import requests
from schemes import *
from helpers import *
from tests_parser import *
import re

# Links to extract
    # test with textbox 
        # https://test-english.com/grammar-points/b2/generic-pronouns/3/
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
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/3/

        # gaps with multiple options
            # https://test-english.com/grammar-points/a2/present-continuous-future-arrangements/

# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/2/
# https://test-english.com/grammar-points/a1/present-simple-forms-of-to-be/3/

headers = {"User-Agent": "Mozilla/75.0"}
# pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')
req = requests.get('https://test-english.com/grammar-points/a2/infinitives-and-gerunds/3/', headers=headers)
page = BeautifulSoup(req.text, 'lxml')




# for each question find the input that has a value of ""
# soup = page.select(g_quest_sel)[1].select('.question-content')[0]
# inputs = soup.find_all('input', attrs={'class': 'watupro-gap'})
# elem = str(soup.contents[0])



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
if q_struct[0] == 'form':
    
    # bools
    has_mul = False

    # parse all of the questions of the page and remove the numbers
    questions = page.select(g_quest_sel)

    for question in questions:
        
        # remove number from questions
        question.select('.watupro_num')[0].string.replace_with('')
        
        # ----------------- parse multiple choice questions -------------

        # parse multiple choice options answers
        if a_struct[0] == 'multiple_c_options':

            # parse answers
            parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1])])
        
        # parse multiple choice bullet answers
        elif a_struct[0] == 'multiple_c_bullets':

            # remove bullets
            for answer_n in question.select('i'):
                
                answer_n.clear()

            # parse answers
            parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1])])
        
        # parse multiple choice boxes answers
        elif a_struct[0] == 'multiple_c_boxes':
            
            parsed_a.append([answer.get_text() for answer in question.select(a_struct[-1])])
        
        # parse gap_option (just has questions no options to select from)
        elif a_struct[0] == 'gap_option':
            
            # strip numbers from the questions
            for quest_n in question.select('.watupro_num'):
                
                quest_n.clear()
                
            # replace inputs with literal gap string
            inputs = question.select(a_struct[-1])
            
            elem = str(question)
            for input in inputs:    
                pattern = re.compile(r''+str(input))
                match = pattern.search(elem)

                if match != None:

                    new = elem.replace(elem[match.start():match.end()], '_'*8)

                    elem = new

            parsed_q.append((BeautifulSoup(elem, 'lxml').get_text().strip()))
            
print(parsed_q)
# print(parsed_a)


        






# answers = page.select(q_struct[-1])[0].select('.question-content input.watupro-gap')

# print(answers)



    
    # parse data according to keys in scheme 
    # for s_key in scheme.keys():

    #     if s_key == 'title' or s_key == 'sub_title' or s_key == 'ex_title':
    #         test_content[s_key] = page.select(scheme[s_key])[0].get_text().encode('ascii', 'ignore').decode().strip()
        
    #     elif s_key == 'example_text': # store example_text with arrows
    #         test_content[s_key] = page.select(scheme[s_key])[0].get_text().strip()
        
    #     # parse test content
    #     elif s_key == 'content': 
            

    #         test_content[s_key] = {}
    #         for c_key in scheme[s_key].keys(): 

    #             # ------------------------- parse multiple choice questions with bullet point answers tests-------------------------

    #             # parse questions
    #             if c_key == 'questions' and struct == 'multiple-c-w-b':
    #                 test_content[s_key][c_key] = [
    #                     [   # get question number
    #                         ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
    #                         # get question content
    #                         tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
    #                     ] 
    #                     for tag in page.select(scheme[s_key][c_key])
    #                     ]

    #             # parse possible answers 
    #             elif c_key == 'options' and struct == 'multiple-c-w-b':
    #                 test_content[s_key][c_key] = [
    #                                 [
    #                                     # get option content
    #                                     ''.join(option.get_text().encode('ascii', 'ignore').decode().split(pattern.findall(option.get_text().encode('ascii', 'ignore').decode().strip())[0]+''))

    #                                 for option in options.select(scheme[s_key][c_key][-1])
    #                                 ]

    #                             for options in page.select(scheme[s_key][c_key][0])
    #                             ]
    #             # ------------------------- parse multiple choice questions options answers tests-------------------------

    #             # parse questions
    #             elif c_key == 'questions' and struct == 'multiple-c-w-o':
    #                 test_content[s_key][c_key] = [
    #                     [   # get question number
    #                         ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
    #                         # get question content
    #                         tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
    #                     ] 
    #                     for tag in page.select(scheme[s_key][c_key])
    #                     ]

    #             # parse possible answers 
    #             elif c_key == 'options' and struct == 'multiple-c-w-o':
    #                 test_content[s_key][c_key] = [
    #                     [
    #                         option.get_text() for option in o_column.select(scheme[s_key][c_key][-1])
    #                     ]
    #                     for o_column in page.select(scheme[s_key][c_key][0])
    #                 ]

    #             # --------------------- parse gap tests with options -----------------------

    #             # parse questions  
    #             elif c_key == 'questions' and struct == 'g-w-o':

    #                 test_content[s_key][c_key] = [
    #                                 [   # get question number
    #                                     questions.get_text().encode('aremove number from questions.decode().strip().replace(''.join([question.get_text() for question in questions.select(scheme['content']['options'][-1]) if question.get_text() != '']), '_'*5).strip(''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip())))
    #                                     ''.join(pattern.findall(questions.get_text().encode('ascii', 'ignore').decode().strip()) or gap options
    # 'multiple_c'join all options in the text into one string and remove them from the question and remove number

    #                                 ]
    #                                     # parse questions from documents
    #                                     for questions in page.select(scheme[s_key][c_key])
    #                             ]

    #             # parse possible answers 
    #             elif c_key == 'options' and struct == 'g-w-o':
                    
    #                 test_content[s_key][c_key] = [
    #                                 [   # parse all option in column retrieve text 
    #                                     option.get_text() for option in column.select(scheme[s_key][c_key][-1]) if option.get_text() != ''
    #                                 ]
    #                             # parse all option columms
    #                             for column in page.select(scheme[s_key][c_key][0])
    #                             ]
                
    #             # --------------------- parse gap tests with single answers (text)-----------------------
    #             # parse questions  
    #             elif c_key == 'questions' and struct == 'g-w-s-text':
                    
                    
    #                 test_content[s_key][c_key] = []
                        
    #                 for paragraph in page.select(scheme[s_key][c_key][0]):
                        
    #                     for numbox in paragraph.select('.numBox'):
                        # remove number from questionsy][c_key].append(paragraph.get_text().encode('ascii', 'ignore').decode())        
    #                         numbox.string.replace_with('___'+numbox.get_text()+'___')
                    
                    
    #             # no options t or gap options
    #             elif c_key == ''multiple_c' struct == 'g-w-s-text':
    #                 pass
                
    #             # --------------------- parse gap tests with single answers (form) -----------------------
    #             # parse questions  
    #             elif c_key == 'questions' and struct == 'g-w-s-form':
                    
                    
    #                 test_content[s_key][c_key] = [
    #                     [   # get question number
    #                         ''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())[0]+"."),
    #                         # get question content
    #                         tag.get_text().encode('ascii', 'ignore').decode().strip().strip(''.join(pattern.findall(tag.get_text().encode('ascii', 'ignore').decode().strip())))
    #                     ] 
    #                     for tag in page.select(scheme[s_key][c_key])
    #                     ]      
                    
    #             # no options to parse
    #             elif c_key == 'options' and struct == 'g-w-s-form':
    #                 pass

    # return test_content




































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



