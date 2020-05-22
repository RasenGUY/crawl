import re
from helpers import parse_tests_questions, parse_tests_answers, find_a_struct, find_q_struct, find_ca_feedback_struct, find_ca_struct, parse_tests_expls

from schemes import g_quest_sel, q_selectors, expl_sel

def parse_tests_content(q_page, ca_page):
    '''
    Function for parsing the content of tests from tests website
    q_page = questions page -> the webpage which contains all of the questions and possible answers to be parsed
    ca_page = correct answers page -> the webpage which contains all of the correct answers for each test
    '''

    # get structs for questions, possible answers, correct answers
    q_struct = find_q_struct(g_quest_sel, q_page)
    a_struct = find_a_struct(q_struct[0], q_selectors, g_quest_sel, q_page)
    
    # correct answer structs
    ca_sct = find_ca_struct(q_struct, ca_page)
    ca_fb_sct =  find_ca_feedback_struct(ca_sct, ca_page)

    print(q_struct)
    print(a_struct)
    print(ca_sct)
    print(ca_fb_sct)
    
    # parse questions, possible answers and correct answers
    questions = parse_tests_questions(g_quest_sel, q_page, q_struct, a_struct)
    answers = parse_tests_answers(q_struct[0], ca_page, ca_sct, ca_fb_sct)

    # parse the explanations if any
    if q_page.select(expl_sel) != 0:
        expls = parse_tests_expls(q_page, expl_sel) 
    
    return (questions, answers, expls)




