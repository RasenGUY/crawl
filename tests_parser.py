from helpers import parse_tests_questions, parse_tests_answers, find_a_struct, find_q_struct, find_ca_feedback_struct, find_ca_struct, parse_tests_expls
import re
from bs4 import Tag, NavigableString, BeautifulSoup


def get_passage(page, scheme):
    '''

    Parser function for retrieving the test material (i.e. texts, passeges) required for completing the test
    '''

    # get text material    
    passage = list()
    element = page.select_one(scheme['instructions']).next_sibling

    while True:

        # store navigable strings
        if isinstance(element, NavigableString):

            if element.string == '\n' or element.string == '':
                
                pass

            else:

                passage.append(element.string) 

        # store normal tags
        elif isinstance(element, Tag):


            # check if malformed tag with 'div'
            str_tag = str(element)
            pattern = re.compile(r'<div.+')
            
            # if the tag is malformed and contains the form in it, remove
            if pattern.search(str_tag) != None: 
                
                match = pattern.search(str_tag)
                
                # create new bs element  
                n_element = str_tag.replace(str_tag[match.start():match.end()], '</' + str(element.name) + '>')
                n_soup = BeautifulSoup(n_element, 'html.parser').p
                
                # append altered text of element to passage
                passage.append(n_soup.get_text())
                element = element.next_sibling
                continue
            
            if element.get_text() == '\xa0' or element.get_text() == '' or element.get_text() == '\n': 
                pass

            else:
                
                passage.append(element.get_text().replace('\xa0', ' ').strip())
                
        
        if element.next_sibling.name == 'div':
            break
        else: 
            element = element.next_sibling        
    
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

    # print(q_struct)
    # print(a_struct)
    # print(ca_sct)
    # print(ca_fb_sct)

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

        # store words
        if key == 'words':
            
            if len(q_page.select(scheme['words'])) != 0:

                content[key] = q_page.select(scheme[key])[0].get_text().replace('\xa0', ' ').strip()
                q_page.select(scheme[key])[0].clear()
            
            else:
                
                content[key] = None

            continue

        # parse content
        elif key == 'questions' or key == 'expl' or key == 'c_answers':
            
            c = None
            if key == 'questions':
                
                if q_struct[0] == 'dialogue':

                    c = (None, questions[-1])
                
                else: 
                    
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

            if q_struct[0] == 'dialogue':
                    
                content[key] = questions[0]
            
            else:

                passage = get_passage(q_page, scheme)

                if len(passage) != 0:

                    content[key] = passage
                
                else:

                    content[key] = None

                    continue
        
        # get q_structs 
        elif key == 'q_struct':

            content[key] = q_struct[0]
            
        # get q_structs
        elif key == 'ca_fb_sct':

            content[key] = ca_fb_sct[0]
        
        # get p_url
        elif key == 'p_url':

            content[key] = scheme[key]
        
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







