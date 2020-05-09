# utility for crawling to websites and extracting information from them 
class Crawler:
    """

    Utility for cralwling and extracting information from target websites 
    """
    def __init__(self, site):
        self.site = site
        self.ils = set()

    def get_page(self, url, method, headers, return_req_object=False, parser='html.parser'):
        """
        utility function that sends a request to a target website
        method can be get or post and return a soup object 
        """

        if method.lower() == "GET":
            try:
                req = requests.get(url, headers=headers)
            except requests.exceptions.RequestException:
                return None
            
            return BeautifulSoup(req.text, parser)

        else:
            try:
                req = requests.get(url, headers=headers)
            except requests.exceptions.RequestException:
                return None
            
            if return_req_object == False:
                return BeautifulSoup(req.text, parser)
            if return_req_object == True:
                return BeautifulSoup(req.text, parser), req

    def get_links(self, url):
        """
        utility function for getting all of internal links of a website based on a chosen selector with g_links being the tags for the search
        """
        # get all the internal links of webpage
        try:
            for link in self.get_page(url, 'GET', self.site.headers[0]).find_all(self.site.ils_if[0], attrs=self.site.ils_if[-1]):
                print("-"*20)
            
                if re.compile(r'\?p=[0-9]*').match(link.attrs['href']) != None:
                    link.attrs['href'] = self.site.abs_url + link.attrs['href']

                if link.attrs['href'] not in self.ils:
                    self.ils.add(link.attrs['href'])
                    print('Stored: {}'.format(link.attrs['href']))
                    print('Surfing --> {}'.format(link.attrs['href']))
                    
                    self.get_links(link.attrs['href'])
            
                else:
                    print(link.attrs['href'], end=' ')
                    print("already exists surfing to new link")
                    continue

        except AttributeError as e:
            print(e)
            print("continuing")


    def check_if_target(self, url, pattern=None, list=None, look_for_inst=False):
        
        '''
        class utility to for determining whether a page url contains target information defined by the page_target parameters 
        if look_for_inst is set to true, then the function will also require a list and pattern by default those are set to None
        '''
        # see if the page has a form all test_pages on this site have one
        target_exists = self.get_page(url, 'GET', self.site.headers[0]).find(self.site.target_params[0], attrs= self.site.target_params[-1])
        
        # find and return test page with instance  
        if target_exists != None:
            
            # only if all of the internal links have already been extracted from the website
            if look_for_inst == True: 
                inst = find_pattern_inst(pattern, list)

                return url, inst

            else:
                return url
        else:
            return None
            
       
    def parse_tests_page(self):

        # loop through links
        for link in self.ils:

            # determine target_page type
            target = self.check_if_target(link, pattern=re.compile(rf'{link}.*'), list=test_crawler.ils, look_for_inst=True)

            print("-"*100)
            if target != None:
                print("Found target {}".format(target[0]))
                page, req = self.get_page(target[0], 'GET', self.site.headers[0], return_req_object=True)
                page_type = parse.urlparse(req.url).path.strip('/').split('/')[0]
                print(page_type)
                pass
                
                # if test-category is level-test 
                if page_type == 'level-test':
                    # scrape_test_level()
                    # check 
                    # if page.select(self.site.page['content']['options']['.watupro-question-choice'])
                    pass
                    
                
                # if page is title is grammer-points do something
                # elif page_type == 'grammar-points':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is listening do something
                # elif page_type == 'listening':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is reading do something
                # elif page_type == 'reading':
                #     print('Page Type {}'.format(page_type))
                
                # if page is title is writing do something
                # elif page_type == 'writing':
                #     print('Page Type {}'.format(page_type))

                
            else:
                print("Target not found")
                print("Continuing.........")
                