from helpers import parse_tests_questions, parse_tests_answers, find_a_struct, find_q_struct, find_ca_feedback_struct, find_ca_struct, parse_tests_expls

def parse_tests_content(q_page, ca_page, scheme):
    '''
    Function for parsing the content of tests from tests website
    q_page = questions page -> the webpage which contains all of the questions and possible answers to be parsed
    ca_page = correct answers page -> the webpage which contains all of the correct answers for each test
    '''
    
    # get structs for questions, possible answers, correct answers
    q_struct = find_q_struct(scheme['questions'][0], q_page)
    a_struct = find_a_struct(q_struct[0], scheme['questions'][-1], scheme['questions'][0], q_page)
    
    # correct answer structs
    ca_sct = find_ca_struct(q_struct, ca_page)
    ca_fb_sct =  find_ca_feedback_struct(ca_sct, ca_page)

    print(q_struct)
    print(a_struct)
    print(ca_sct)
    print(ca_fb_sct)

    
    # get title of the test
    # get sub_title of the test -> exc 1, 2, 3, if any
    # get test instructions -> if any
    # get textBox -> if any 
    
    # parse questions, possible answers and correct answers
    questions = parse_tests_questions(scheme['questions'][0], q_page, q_struct, a_struct)
    p_answers = parse_tests_answers(q_struct[0], ca_page, ca_sct, ca_fb_sct)

    # parse the explanations if any
    if len(q_page.select(scheme['expl'])) != 0:
        expls = parse_tests_expls(q_page, scheme['expl']) 
    
    return (questions, p_answers, expls)

def parse_listening_test():
    pass

def parse_reading_test(page, scheme):
    '''
    parser function for retrieving the test material (i.e. texts, passeges) required for completing the test
    '''

    # get text material
    element = page.select(scheme['instructions'])[0]
    bs4_element = type(element)
    passage = list()

    while element.name != 'div':

        element = element.next_sibling
        
        if element.name == 'div':
            break
        
        else:
            
            if type(element) != bs4_element: 
                
                passage.append(element.string) 

            # store only full strings
            else: 
                
                if element.get_text() != '\xa0' or element.get_text() != '':

                    passage.append(element.get_text().replace('\xa0', ' ').strip())
        

    
    return passage








