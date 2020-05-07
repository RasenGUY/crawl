import requests
from bs4 import BeautifulSoup
import os
import re
from urllib import parse


class Tests:
    '''
    
    Common base class for all tests on the website
    '''
    def __init__(self, url, id, title, subtitle, body):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body # this an object



class Crawler:
    '''

    Utility for cralwling and extracting information from target websites 
    '''

    def get_page(self, url, method, headers):
        '''
        utility function that sends a request to a target website
        method can be get or post and return a soup object
        '''
    
        if method.lower() == 'GET':
            try:
                req = requests.get(url, headers)
            except requests.exceptions.RequestException:
                return None
            return BeautifulSoup(req.text, 'html.parser')
        
        else:
            try:
                req = requests.get(url, headers)
            except requests.exceptions.RequestException:
                return None
            return BeautifulSoup(req.text, 'html.parser')

    
        
    
