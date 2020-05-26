# all of the data schemes for the different classes
# ---------------------------------------------------

'''
This module contains all of possible tag strcuture schemes for the parsing the different tests of tests target website
'''

# selectors for getting the question structure
g_quest_sel = '.quiz-form .watu-question'
q_selectors = [('.question-content input.watupro-gap', 'gap_option'), ('.question-content select.watupro-gap option', 'gap_options'), ('.question-choices', 'multiple_c')] # for defining q page structs
expl_sel = '#explanation h2, #explanation h3, #explanation h4, #explanation p, #explanation ul, #explanation img'

# ---------------- Test Pages ----------

# general tag scheme -> level-test, grammer test, reading scheme
general_scheme = {
    'test_title' : '.header h1', #test-title
    'sub_title' : '#exercises h3', #test subtitle 
    'instructions' : '#exercises h5', #instructions for the test
    'text_box' : '.textBox', # if there is a textbox 
    'questions' : [g_quest_sel, q_selectors],
    'expl' : expl_sel
}

# listening-tests
listening_scheme = general_scheme
listening_scheme['audio_url'] = 'iframe' 
# https://www.youtube.com/embed/-5iUfno6gPI


