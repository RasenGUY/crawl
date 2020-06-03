import os
from helpers import write_answers, write_explanations, write_questions

class Content:
    '''
    common base class for all content
    '''

    def __init__(self, url, title, content):
        self.url = url #string 
        self.title = title # string
        self.body = content


    def show_parsed_items(self):
        '''

        Class utility for printing parsed content
        '''
        
        print('URL: {}'.format(self.url)) 
        print('Page Title: {}'.format(self.title)) 
        print('Content: {}'.format(self.body))

   
    def create_folder_path(self, link_p, home):
        '''

        Utility function for creating a folder path which can be utilized to store data
        returns a directory path, the home variable is refers to the home directory used for storing the tests if no home directory is given, home variable will take on the home path of the users machine
        '''
        
        if home == None:
            home = os.environ['HOME']

        # remove number at the back of the folder
        if link_p[-1].isdigit() == True:
            
            link_p = link_p.strip(link_p[-1])

        # create folderpath
        f_path = os.path.dirname(home + link_p + '/')

        if os.path.exists(f_path) == False:
            os.makedirs(f_path)

        return f_path 
        


    def create_file_name(self, f_path ,p_nums):
        '''

        Utility function for creating filenames, arguments include a download folder path and  
        '''
        
        title = f_path.split('/')[-1]       
        sub = False

        if p_nums == 0 or p_nums == 1:
        
            # if subtitle exists
            for key in self.body.keys():
            
                if key == 'sub_title':
                    
                    sub = True 
                    
            if sub == True:

                f_as = '/' + self.body['sub_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-ANSWERS' + '.txt'
                f_qs = '/' + self.body['sub_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-QUESTIONS' + '.txt'

            else:

                f_qs = '/' + title + '-QUESTIONS' + '.txt'
                f_as = '/' + title + '-ANSWERS' + '.txt'
                
        else:

            f_qs = '/' + self.body['sub_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-QUESTIONS' + '.txt'
            f_as = '/' + self.body['sub_title'].replace('-', '').replace(',', '').replace(' ', '-') + '-ANSWERS' + '.txt'

        f_ex = '/' + 'EXPLS' + '.txt'
        
        return(f_qs, f_as, f_ex)
    

    def write_parsed_questions_answers(self, f_path, f_qs, f_as):
        '''
        
        Utility function for storing data into text files
        '''

        print('\n')
        print("Downloading Q & A  ...... ...... ....... ")
        print('\n')
        # write questions and answers
        write_questions(f_path, f_qs, self.body)
        print('-Questions downloaded successfully-')
        write_answers(f_path, f_as, self.body)
        print('-Answers downloaded successfully-')
        print('\n')


    
    def write_parsed_explanantions(self, f_path, f_ex):
        '''

        Class utility function for storing text explanations in text files
        '''
        print('\n')
        print("Downloading Explanations  ...... ...... ....... ")
        # write explanations
        write_explanations(f_path, f_ex, self.body)
        print('-Explanations downloaded successfully-')
        print('\n')

        

class Listening(Content):

    '''
    Subclass for content parsed from listening tests
    '''

    def ___init__(self, url, title, content, audio_response):
        
        # initialize subclass GT
        Content.__init__(self, url, title, content)

        self.audio_response = audio_response # req response -> to use for storing 

    
    def write_audio(self, a_path, audio_response):
        '''

        utility function for retrieving audio
        '''

        with open(a_path + '/AUDIO' + '.mp3', 'wb') as audio:
            print('\n')
            print('Downloading audio from {}'.format(self.body['p_url']))
            print('\n')
            
            audio.write(audio_response.content)

        