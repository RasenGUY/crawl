import re
from helpers import parse_tests_questions, parse_tests_answers
from schemes import *

def parse_tests_content(page):
    '''
    Function for parsing the content of tests from tests website
    '''
    # parse questions
    questions = parse_tests_questions(g_quest_sel, q_selectors, page)

    # parse answers

    return questions




