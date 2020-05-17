import re
from helpers import *

def parse_tests_content(g_quest_sel, q_selectors, page):
    '''
    Function for parsing the content of tests from tests website
    '''
    # necessary variables 
    questions = page.select(g_quest_sel)
    q_struct = find_q_struct(g_quest_sel, page)
    a_struct = find_a_struct(q_struct[0], q_selectors, g_quest_sel, page)
    print(q_struct)
    print(a_struct)

    # empty questions and answers strings and question number counter
    parsed_q = []
    parsed_a = []
    q_number = 0

    # all questions in the test form
    questions = page.select(g_quest_sel)
    
    for question in questions:

        if q_struct[0] == 'form':

            # count questions
            if len(question.select('.numbox ')) != 0:
                
                q_number += len(question.select('.numBox'))
            
            else:

                q_number += len(question.select('.watupro_num'))
            
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
                    new_soup = rem_soup_ins_re(inputs, question, '_'*6)
                
                # parse questions with one gap or more gaps
                if new_soup.get_text().rfind('\xa0') != -1:

                    parsed_q.append(new_soup.get_text().encode('ascii', 'ignore').decode().strip())
                
                else:
                    
                    parsed_q.append(new_soup.get_text().strip())

            
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


        elif q_struct[0] == 'text' or q_struct[0] == 'dialogue' or q_struct[0] == 'special':       

            text = question
            new_soup = None 

            # number of possible answers
            answers = text.select(a_struct[-1])
            
            # parse answers only if options 
            if a_struct[0] == 'gap_options':
                
                parsed_a.append([[option.get_text() for option in answer if option.get_text() != ''] for answer in answers])
    
            # if there are Numboxes replace them with gaps, else replace inputs
            if len(text.select('.numBox')) > 0:
            
                for num_box in text.select('.numBox'):
                    
                    # count numbers
                    if num_box.get_text() == '0':
                        
                        num_box.string.replace_with("_"*1 + text.select('.textGap')[0].get_text() + "_"*1)

                        text.select('.textGap')[0].clear()

                        continue

                    else:

                        q_number += 1

                num_box.string.replace_with("_"*3 + num_box.get_text() + "_"*3)
           
            # replace inputs if special struct else clear the inputs
            elif q_struct[0] == 'special' and len(answers) > 0:

                new_soup = rem_soup_ins_re(answers, question, '_'*5)

            else:    

                # remove inputs or select
                for answer in answers:
                    answer.clear() 

            if q_struct[0] == 'text': 
                
                # parse questions
                for paragraph in text.select(q_struct[-1]):
                    
                    if paragraph.get_text() == '':

                        continue

                    if paragraph.get_text().rfind('\xa0') != -1 :
                    
                        parsed_q.append(paragraph.get_text().encode('ascii', 'ignore').decode().strip())

                    else:
                        parsed_q.append(paragraph.get_text().strip())
                    
            else:
                
                # change text to new soup
                if q_struct[0] == 'special':

                    text = new_soup

                # parse questions
                for line in text.find_all(['h4', 'p']):
                    
                    if line.get_text().rfind('\xa0') != -1:
                    
                        parsed_q.append(line.get_text().encode('ascii', 'ignore').decode().strip())

                    else:
                        parsed_q.append(line.get_text().strip())
        

            
        
    
    # return parsed content
    return (parsed_q, parsed_a, q_number)



def parse_tests_answers(page, scheme, test_structs):
    '''
    Function for parsing answers of tests from the tests website
    '''
    pass