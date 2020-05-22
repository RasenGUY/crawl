# all of the data schemes for the different classes
# ---------------------------------------------------

'''
This module contains all of possible tag strcuture schemes for the parsing the different tests of tests target website
'''

# selectors for getting the question structure
g_quest_sel = '.quiz-form .watu-question'
expl_sel = '#explanation h2, #explanation h3, #explanation h4, #explanation p, #explanation ul, #explanation img'
q_selectors = [('.question-content input.watupro-gap', 'gap_option'), ('.question-content select.watupro-gap option', 'gap_options'), ('.question-choices', 'multiple_c')]

# ---------------- Test Pages ----------
# level-test
level_test_scheme = {
    'title' : 'header h1', #test-title
    'sub_title' : '#exercises h5', #test subtitle 
    'content': dict(),
    'answers': dict()
}

# grammer-tests
grammer_scheme = {
    'title' : 'header h1', #test-title
    'ex_title': '#exercises h3', # exercise title
    'sub_title' : 'h5', #excercise subtitle
    'example_text' : '#exercises p:nth-child(3)', # test answers example
    'content' : dict(),
    'answers' : dict()
}

# ---------------------------------------------------
 
