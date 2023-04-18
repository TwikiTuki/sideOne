from spider import *

def test_get_domain(url):
    print(f'url: {url}')
    domain = get_domain(url)
    ok = 'OK' if domain == 'https:barcelonactiva.cat' else 'KO'
    print(f' {ok} domain: {domain}\n')

def test_clean_link(url):
    print(f'url: {url}')
    short = clean_link(url)
    print(f'short: {short}')


test_get_domain('https:www.barcelonactiva.cat/barcelonactiva/cat/index.jsp')
test_get_domain('https:www.barcelonactiva.cat:8000/barcelonactiva/cat/index.jsp')

test_clean_link('https://www.42barcelona.com/')
test_clean_link('https:42barcelona.com/')
test_clean_link('https://42barcelona.com/')
test_clean_link('https:www.42barcelona.com/')
test_clean_link('https://www.42barcelona.com/')
test_clean_link('https:www.42barcelona.com/')


#Test get_ur
get_url('Should not give error')
get_url('https://www.42barcelona.com/')
get_url('https:42barcelona.com/')
get_url('https://42barcelona.com/')
get_url('https:www.42barcelona.com/')
get_url('https://www.42barcelona.com/')
get_url('https:www.42barcelona.com/')

print('\nShould give error')
get_url('https://42malaga.com')
