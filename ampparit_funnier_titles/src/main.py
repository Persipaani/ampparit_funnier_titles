'''
Created on 9.10.2015

Versio 0.4

Retrieves the most popular titles from Ampparit.com and mixes them together
to form funny titles. Doesn't use API because Ampparit.com doesn't have one to my
knowledge. May sometimes get confused with some weird titles because I can't predict
what journalist come up next ;)

@author: Sampo
'''
import urllib.request
import random

class FunnierTitles(object):
    '''
    this class makes funnier titles
    '''

    def __init__(self, amount):
        '''
        Constructor
        '''
        self.howmany = amount
        self.retries = 0
        self.begins = []
        self.ends = []
        self.get_data_from_url()
        
        #for debugging purposes:
        #self.altparse('Maanjäristykset saivat Uuden-Seelannin kaaokseen - Suomalaismies: "Rosvot vyöryvät täyttä päätä"')
        #print(self.ends)
        #print(self.begins)
        
    
    def get_data_from_url(self):
        '''
        Gets html-data from ampparit.com.
        '''
        html_file, headers = urllib.request.urlretrieve('http://www.ampparit.com/suosituimmat')
        self.read_html_file(html_file)
        
        self.fix_quotes(self.begins)
        self.fix_quotes(self.ends)
        
        
        if(self.begins == [] and self.retries < 10):
            print("Empty html, Retrying...")
            self.get_data_from_url()
            self.retries += 1
        elif(self.retries < 10):
            self.generate_funny(self.howmany)
        else:
            print("10 retries and no result, You are out of luck buddy...")
            return
    
    def altparse(self,full_title):
        
        '''
        Parses title and puts it in containers
        '''
        
        while(full_title.count(" - ") != 0 or full_title.count(": ")!=0 or full_title.count("–")!=0):
            
            if(full_title.count(" - ") != 0):
                first = full_title[:full_title.index(" - ")]
                full_title = full_title[full_title.index(" - ") + 1:]
            
            elif(full_title.count(": ") != 0):
                first = full_title[:full_title.index(": ")]
                full_title = full_title[full_title.index(": ") + 1:]
                
            elif(full_title.count("–") != 0):
                first = full_title[:full_title.index("–")]
                full_title = full_title[full_title.index("–") + 1:]
            
            self.begins.append(first.strip(" - "))
            
        
        full_title = full_title.strip(" - ");
        self.ends.append(full_title.strip())      
    
    
    def read_html_file(self,file):
        '''
        Reads html and puts data in container for usage
        '''
        html = open(file, encoding="utf8")
        linecount = 0 #keeps count of read lines
        
        try:
            for line in html:
                linecount += 1
                if(line.count("10 suosituinta viimeisen 1 tunnin ajalta") != 0):
                    for word in line.split("div"):
                        if(word.count("_blank") != 0 and word != ""):
                            #print(word[word.index('_blank">') + 8 : word.index("</a")])
                            full_title = word[word.index('_blank">')+8:word.index("</a")]
                            #print(full_title)
                            
                            self.altparse(full_title)
                            
                            '''
                            OLD MESSIER METHOD
                            #Division by –
                            if(full_title.count("–") == 1):
                                self.begins.append(full_title[:full_title.index("–")])
                                self.ends.append(full_title[full_title.index("–")+1:])
                            #Division by small -
                            elif(full_title.count(" - ") == 1):
                                self.begins.append(full_title[:full_title.index(" - ")])
                                self.ends.append(full_title[full_title.index(" - ")+1:])
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
                            '''
                                
        except Exception as error:
            print(error)
            print("Fail at line " + str(linecount))
                       
        #html handled
    def fix_quotes(self, list):
        '''
        Does some small tweaks to the final results
        '''
        
        for index in range(len(list)):
            if(list[index].count("&quot;") != 0):
                new = list[index].replace('&quot;','"')
                list[index] = new
      
    
    def generate_funny(self,amount):
        '''
        Handles the whole generation process by calling other functions
        '''
        
        for v in range(amount):
            try:
                print(self.begins[random.randint(0,len(self.begins)-1)] + " – " + self.ends[random.randint(0,len(self.ends)-1)])
            except Exception as error:
                print(error)
                print("Fail at  " + str(v))
        

FunnierTitles(10);