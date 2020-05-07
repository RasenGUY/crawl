
class Content:
    '''
    common base class for all content
    '''

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body
    
    def print(self):
        '''

        printing function for content
        '''
        
        print('URL: {}'.format(self.url)) 
        print('Title: {}'.format(self.url)) 
        print('Body: {}'.format(self.url)) 