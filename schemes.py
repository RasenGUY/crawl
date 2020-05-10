# all of the data schemes for the different classes
# ---------------------------------------------------

'''
post = link for sending post request
    
    ---- information for tests ----
    test['id'] = "div -> form: class="quiz-form" id="quiz-<id>" 
    test['title'] = "h1: class="mb-4"
    test['subtitle'] = "h5"
    test['reading_text'] = div: id="excercises" constituted of all of the h4, h6 and all of the p tags
    
    --- information for questions --- 
    test['questions'] = class="watu-question" -> bs.find_all retrieves a list bs question objects

    test['questions']['question']['text_info'] = div: class="question-content" p (retrieve through regex)
        - if obj.is_gap = True
            - store text of text_info bs object
        - else
            - store as (use regex):
                - q_number
                - q_text

    test['questions']['question']['options'] = div: class="question-choices" -> used to return a list of options    
    test['questions']['question']['options']['option']['number'] = div: class="watupro-question-choice" <i> a., b. c. etc <i/>
    test['questions']['question']['options']['option']['text'] = class="watupro-question-choice" label: class=" answer" -> span: text resides inside this span tag

    --- information for answers ---
    answers['answers'] = div: class="watupro-choices-columns"
    answers['answers']['answer']['correct'] = div: class="show-questions-choices" -> ul -> li: class="correct-answer" -> span: class="answer"
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
test_scheme = {
    'title' : 'header h1',
    'sub_title' : '#exercises h5',
    'content': test_structs[-1][-1]
}

grammer_scheme = {
    'title' : 'h1',
    'sub_title' : 'h5' 
}

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
