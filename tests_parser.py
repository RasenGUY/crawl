from helpers import parse_tests_questions, parse_tests_answers, find_a_struct, find_q_struct, find_ca_feedback_struct, find_ca_struct, parse_tests_expls
import re

def get_passage(page, scheme):
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

            # store navigable strings
            if type(element) != bs4_element: 
                
                passage.append(element.string) 

            # store normal tags
            else: 
                
                if element.get_text() != '\xa0' or element.get_text() != '':

                    passage.append(element.get_text().replace('\xa0', ' ').strip())
        
    return passage
    
def parse_tests_content(q_page, ca_page, scheme):
    '''
    Function for parsing the content of tests from tests website
    q_page = questions page -> the webpage which contains all of the questions and possible answers to be parsed
    ca_page = correct answers page -> the webpage which contains all of the correct answers for each test
    '''

    # place to store information
    content = dict()

    # get structs for questions, possible answers, correct answers
    q_struct = find_q_struct(scheme['questions'][0], q_page)
    a_struct = find_a_struct(q_struct[0], scheme['questions'][-1], scheme['questions'][0], q_page)
    
    # correct answer structs
    ca_sct = find_ca_struct(q_struct, ca_page)
    ca_fb_sct = find_ca_feedback_struct(ca_sct, ca_page)

    print(q_struct)
    print(a_struct)
    print(ca_sct)
    print(ca_fb_sct)

    # parse questions, possible answers and correct answers
    questions = parse_tests_questions(scheme['questions'][0], q_page, q_struct, a_struct)
    c_answers = parse_tests_answers(q_struct[0], ca_page, ca_sct, ca_fb_sct)

    # parse the explanations if any
    if len(q_page.select(scheme['expl'])) != 0:
        expls = parse_tests_expls(q_page, scheme['expl']) 
    else:
        expls = None
    
    # parse headers and store already parsed data into a dictionary
    for key in scheme.keys():

        # store text_box
        if key == 'text_box':
            
            if len(q_page.select(scheme['text_box'])) != 0:

                content[key] = q_page.select(scheme[key])[0].get_text().replace('\xa0', ' ').strip()
                q_page.select(scheme[key])[0].clear()
            
            else:
                
                content[key] = None

            continue

        # parse content
        elif key == 'questions' or key == 'expl' or key == 'c_answers':
            
            c = None
            if key == 'questions':
                
                c = questions

            elif key == 'c_answers':

                c = c_answers
            
            else:
                
                if expls != None:
                    
                    c = expls
                
                else:

                    continue 

            # store if content is True
            if len(c) != 0:
                
                content[key] = c
            
            else:

                content[key] = None
        
        # pass audio 
        elif key == 'audio':

            continue 

        # get top part of the test 
        elif key == 'passage':
            
            passage = get_passage(q_page, scheme)

            if len(passage) != 0:

                content[key] = passage
            
            else:

                content[key] = None

                continue
        
        # parse content according to scheme 
        else:
            
            # check first if content exists 
            if len(q_page.select(scheme[key])) != 0:
                
                content[key] = q_page.select(scheme[key])[0].get_text().replace('\xa0', ' ').strip()
            
            else:

                continue
    
    # return content  
    return content 
        

def get_audio_link(page, scheme):
    
    # get link and store its href as a string
    link_str = str(page.select(scheme['audio'])[0].attrs['data-wpfc-original-src'])

    # get link substring
    pattern = re.compile(r'\#(.+)')
    match = pattern.search(link_str)
    sub_str = link_str[match.start()+1:match.end()]
    audio_link = 'https://www.youtube.com/embed/' + sub_str
    
    return audio_link







