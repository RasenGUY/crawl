# all of the data schemes for the different classes
# ---------------------------------------------------

# there are more types
    # https://test-english.com/listening/b1-b2/actors-talk-acting/


'''
This module contains all of possible tag strcuture schemes for the parsing the different tests of tests target website
'''

# selectors test structures
test_structs = [
    [
        ('.question-content .watupro-gap option', 'g-w-o'), # g-w-o
        {
            'questions': '.quiz-form .watu-question .question-content p',
            'options': ['select.watupro-gap', 'option']  
        }
    ], 
    [
        ('.watu-question .question-choices', 'multiple-c'), # multiple-c
        { 
            'questions': '.quiz-form .watu-question .question-content p', 
            'options': ['.question-choices', '.watupro-question-choice']
            }
    ],
    [
        ('.watu-question input.watupro-gap', 'g-w-s'), # g-w-s
        {   
            'questions': ['.quiz-form .watu-question .question-content p', '.numBox'],
            'options': None
        }
    ]
]

# content structures


# ---------------- Test Pages ----------
# level-test
level_test_scheme = {
    'title' : 'header h1', #test-title
    'sub_title' : '#exercises h5',
    'content': dict(),
    'answers': dict()
}

# grammer-tests
grammer_scheme = {
    'title' : 'header h1', #test-title
    'ex_title': '#exercises h3', # exercsise title
    'sub_title' : 'h5', #excercise subtitle
    'content' : dict(),
    'answers' : dict()
}
# use of english test



# notes
    # three type schemes
        # 1. gap with options
            # - everything is the same but the options of the questions are in a select tab in the "question-content" div  select tag is called watupro_gap
            # store in list without numbers, numbers can be created when print
        # 2. gap with bullets
            # question are in question-choices, label
        # 3. gap with single answers
            # options are in a div class=textBox above the excercise
            # there is only one class=question-content 


# todo 
# write function that determines the test_format
    # return gap-w-o
    # return gap-w-b
    # return gap-w-s

# normalizing things
    # grammer and writing texts both have excercises
    # reading and listening are usually consist of just one excercise




# ---------------------------------------------------
