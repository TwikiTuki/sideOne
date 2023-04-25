from spider import solve_host
from spider import *

def test(absolute, relative, expected):
    print(f'absolute: {absolute}')
    print(f'relative: {relative}')
    result = solve_host(absolute, relative)
    print('OK' if result == expected else 'KO', result)
    print()

test('https://www.42barcelona.com/', 'https://www.42barcelona.com/', 'https://www.42barcelona.com/')
test('https://www.42barcelona.com/', 'https://www.43barcelona.com/', 'https://www.43barcelona.com/')

test('https://www.42barcelona.com/stuff/', 'more_stuff', 'https:42barcelona.com/stuff/more_stuff')
test('https://www.42barcelona.com/stuff/', './more_stuff', 'https:42barcelona.com/stuff/more_stuff')
test('https://www.42barcelona.com/stuff/', '/more_stuff', 'https:42barcelona.com/more_stuff')

test('https://www.42barcelona.com/', 'more_stuff', 'https:42barcelona.com/more_stuff')
test('https://www.42barcelona.com/', '/more_stuff', 'https:42barcelona.com/more_stuff')
test('https://www.42barcelona.com/', './more_stuff', 'https:42barcelona.com/more_stuff')

print("Whit some arguments")
test('https://www.42barcelona.com/?some_arguments', 'https://www.42barcelona.com/', 'https://www.42barcelona.com/')
test('https://www.42barcelona.com/?some_arguments', 'https://www.43barcelona.com/', 'https://www.43barcelona.com/')
test('https://www.42barcelona.com/stuff/?some_arguments', 'more_stuff', 'https:42barcelona.com/stuff/more_stuff')
test('https://www.42barcelona.com/stuff/?some_arguments', './more_stuff', 'https:42barcelona.com/stuff/more_stuff')
test('https://www.42barcelona.com/stuff/?some_arguments', '/more_stuff', 'https:42barcelona.com/more_stuff')

print("Whit empty model")
test('', 'https://www.42barcelona.com/', 'https://www.42barcelona.com/')
test('', 'https://www.43barcelona.com/', 'https://www.43barcelona.com/')
test('', 'more_stuff', 'more_stuff')
test('', './more_stuff', './more_stuff')
test('', '/more_stuff', '/more_stuff')

print('with empty incomplet')
test('https://www.42barcelona.com/?some_arguments', '', '')
