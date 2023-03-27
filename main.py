# import webbrowser
# import sys

# VALID_WEBSITES = [
#     'reddit.com',
#     'stackoverflow.com',
#     'stackexchange.com',
#     'medium.com'
# ]

# CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

# def create_filter(valid_websites):
#     return '(' + ' OR '.join(f'site:{website}' for website in valid_websites) + ')'

# def create_query():
#     if len(sys.argv) < 2:
#         print('Error: Please provide a search query.')
#         sys.exit()
#     return ' '.join(sys.argv[1:])

# def create_url(query, filter):
#     return f"http://www.google.com/search?q={query}{filter}"

# def open_browser(url, browser_path):
#     webbrowser.get(browser_path).open(url)

# def main():
#     filter = create_filter(VALID_WEBSITES)
#     query = create_query()
#     url = create_url(query, filter)
#     open_browser(url, CHROME_PATH)

# if __name__ == '__main__':
#     main()


import webbrowser 
import sys

url = "http://www.google.com/search?q="

valid_websites = [
    'reddit.com',
    'stackoverflow.com',
    'stackexchange.com',
    'medium.com'
]

# chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

def create_filter():
    filter = '('
    for index, website in enumerate(valid_websites):
        filter += 'site:' + website
        if index == len(valid_websites) - 1:
            filter += ')'
        else:
            filter += ' OR '
    return filter

def create_query():
    query = sys.argv[1:]
    return ' '.join(query)

def create_url():
    if len(sys.argv[1:]) == 0:
        print('Error')
    else:
        final_url = url + create_query() + create_filter() 
        webbrowser.get(chrome_path).open(final_url)

create_url()



