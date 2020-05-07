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
# ---------------- Test Pages -----------------------

grammer_tags_scheme = {
    'title' : 'h1',
    'sub_title' : 'h5' 
}
# notes
    # question number is extracted from question content
level_test_tags_scheme = {
    'title' : 'header h1:first-child',
    'sub_title' : '#exercises h5:first-child',
    'content': {
        'questions' : '.quiz-form .watu-question .question-content p',
        'options' : {
            'numbers' : ['.question-choices', 'i'],
            'body' : ['.question-choices', 'label']
        } 
    }
}





# ---------------------------------------------------
