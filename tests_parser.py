from helpers import *
from schemes import *  
import re
def parse_tests_content(page, scheme):
    '''
    Function for parsing the content of tests from tests website
    '''
    
    # determine question and answer structure
    q_struct = find_q_struct(g_quest_sel, page)
    a_struct = find_a_struct(q_struct[0], q_selectors, q_struct[-1], page)
    
    # locals 
    test_content = dict()
    pattern = re.compile(r'(\b\d+|\b[a-zA-Z]\.)')

    # parse headers
    
    # parse questions and answers
        # parse form questions and answers
        # parse text questions and answers  

def parse_tests_answers(page, scheme, test_structs):
    '''
    Function for parsing answers of tests from the tests website
    '''
    pass
