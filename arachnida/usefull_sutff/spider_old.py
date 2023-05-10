#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import sys
import os
import requests
from html.parser import HTMLParser

def get_flags(args):
    usage = 'usage: ./spider [-r -l -p -S] URL'
    if (len(args) < 2):
        print(usage)

    flags={'url': None ,'recurse': False ,'depth': -1 ,'path': None}
    flags['url'] = args[-1]
    i = 1
    max_i = len(args) - 1
    # Get the flags
    while i < max_i:
        flag = args[i][1:]
        # Assert the last flags arguments does not require an aditional argument
        if (i == max_i - 1 and flag in ['p', 'l']):
            print(usage)
            raise ValueError(f'Expected argument for -{flag}')
        # Now get the flags
        if (flag == 'r'):
            flags['recurse'] = True  
            i += 1
        elif (flag == 'p'):
            flags['path'] = args[i + 1]
            path = flags['path']
            if (not os.path.isdir(flags['path'])):
                raise FileNotFoundError(f'No such file or direcotry: {path}')
            i += 2
        elif (flag == 'l' ):
            flags['depth'] = args[i + 1]
            if (not flags['depth'].isdigit()):
                raise TypeError("depth (-l) must be a non negative integer")
            flags['depth'] = int(flags['depth'])
            i += 2
        else:
            print(usage)
            raise ValueError(f'flag "{flag}" at index {i} is not allowed \n {usage}')
        if (not flags['recurse']):
            flags['depth'] = 0
    return (flags)

log_file = 'log_file.txt'
class Parser(HTMLParser):

    def __init__(self, flags, depth = None, visited =  {}):
        print("initilializing")
        super().__init__()
        self.flags = flags
        self.visited = visited
        self.depth = depth if depth != None else flags['depth']
        self.domain = get_domain(flags['url'])
        self.pending
    def handle_starttag(self, tag ,attrs):
        # Handle the links tag
#        print(f'>>> {tag}, {attrs}')
        if (tag == 'a'):
            ln = len(self.visited)
            href = [attr for attr in attrs if attr[0] == 'href']
            if not len(href):
                return
            link = href[0][1]
            shorted = clean_link(link)
            domain = get_domain(shorted)
            print(f"The link is {link}")
            if (get_domain(shorted) == self.domain and shorted not in self.visited and self.depth != 0):
                    print(f"The short is {shorted}")
                    self.visited[shorted] = {'short': shorted, 'original': link} 
                    print("\t\tI like this link")
                    assert shorted in self.visited, "wooops didnt add the link"
                    log = open(log_file, 'a')
                    log.write(link)
                    log.write('\n')
                    log.close()

                    Parser(self.flags, depth = self.depth - 1, visited = self.visited)
                    resp = get_url(shorted)
                    try:
                        parser.feed(resp['text'])
                    except Exception as e:
                        print(f"THE ERROR LINK IS: {link}")

            else:
                print("\t\tdont like this link")

        # Handle the images tag
        elif (tag == 'img'):
            ...


    def handle_endtag(self, tag):
        ...

    def handle_data(self, data):
        ...

def clean_link(link):
    link = link.replace('https://', 'https:', 1)
    link = link.replace('https:www.', 'https:', 1)
    return link
def get_domain(link):
    link = clean_link(link)
    # cut subdirectory
    scheme_end = len('https:') + 1
    if ('/' in link):
        link = link[0:link.find('/')]
    # cut port
    if (':' in link[scheme_end:]):
        link=link[:link.find(':', scheme_end)]
    return link

def get_url(url):
    print(f'get_url inital link: {url}')
    assert get_domain(url) == "https:42barcelona.com", 'The domain is not valid!!!!'
    # Asser url is valid for get_url
    url = clean_link(url)[len('https:'):]
    url = 'https://' + url
    res_dct = {}
    print(f'get_url link: {url}')
    resp = requests.get(url)
    res_dct['content'] = resp.content 
    res_dct['url'] = url
    res_dct['text'] = resp.text
    res_dct['encoding'] = resp.encoding
    return res_dct

def scrap_url(url, visited):

    raise "Shouldnt be here"
    resp = get_url("https://www.42barcelona.com/")
    parser = Parser()
    parser.feed(resp['text'])

if (__name__ == '__main__'):
    urls = {}

    flags = get_flags(sys.argv)
    resp = get_url("https://www.42barcelona.com/")
    resp = get_url("https://www.42barcelona.com/es/actualidad/actitud-42-dani-lopez/")
    print("flags:", flags)
    parser = Parser(flags)
#   parser.feed(resp['content'].decode('utf-8'))
    print('------------sdaf-----------')
#    text = resp['text'][resp['text'].find('<'):]
    text = resp['text']
    parser.feed(text)
