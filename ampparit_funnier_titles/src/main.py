'''
Created on 9.10.2015

@author: Sampo
'''
import urllib.request
import random

class FunnierTitles(object):
    '''
    this class makes funnier titles
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.retries = 0
        self.begins = []
        self.ends = []
        self.get_data_from_url()
        
    
    def get_data_from_url(self):
        '''
        Gets html-data from ampparit.com.
        '''
        html_file, headers = urllib.request.urlretrieve('http://www.ampparit.com/suosituimmat')
        self.read_html_file(html_file)
        #print(self.begins)
        #print(self.ends)
        
        self.fix_quotes(self.begins)
        self.fix_quotes(self.ends)
        
        
        if(self.begins == [] and self.retries < 10):
            print("Empty html, Retrying...")
            self.get_data_from_url()
        elif(self.retries < 10):
            self.generate_funny(10)
        else:
            print("10 retries and no result, You are out of luck buddy...")
            return
    
    def read_html_file(self,file):
        '''
        Reads html and puts data in container for usage
        '''
        html = open(file, encoding="utf8")
        linecount = 0 #keeps count of read lines
        
        try:
            for line in html:
                linecount += 1
                if(linecount == 348):
                    for word in line.split("div"):
                        if(word.count("_blank") != 0 and word != ""):
                            #print(word[word.index('_blank">') + 8 : word.index("</a")])
                            full_title = word[word.index('_blank">')+8:word.index("</a")]
                            #print(full_title)
                            #Division by –
                            if(full_title.count("–") == 1):
                                self.begins.append(full_title[:full_title.index("–")])
                                self.ends.append(full_title[full_title.index("–")+1:])
                            #Division by two -'s
                            elif(full_title.count("–") == 2):
                                self.begins.append(full_title[:full_title.index("–")])
                                full_title = full_title[full_title.index("–"):]
                                self.begins.append(full_title[1:full_title.index("–")])
                                self.ends.append(full_title[full_title.index("–")+1:])
                            #Division by :
                            elif(full_title.count(":") != 0):
                                self.begins.append(full_title[:full_title.index(":")])
                                self.ends.append(full_title[full_title.index(":")+1:])
                                
        except Exception as error:
            print(error)
            print("Fail at line " + str(linecount))
                       
        #html handled
    def fix_quotes(self, list):
        for index in range(len(list)):
            if(list[index].count("&quot;") != 0):
                new = list[index].replace('&quot;','"')
                list[index] = new
      
    
    def generate_funny(self,amount):
        for v in range(amount):
            try:
                print(self.begins[random.randint(0,len(self.begins)-1)] + " - " + self.ends[random.randint(0,len(self.ends)-1)])
            except Exception as error:
                print(error)
                print("Fail at  " + str(v))
        

FunnierTitles();