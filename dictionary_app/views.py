from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup as bs


def get_html_content(word, url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    word = word.replace(' ', '+')
    html_content = session.get(url+word).text
    return html_content


def Dictionay(request):
    result = None
    if 'word' in request.GET:
        word = request.GET.get('word')
        info1 = 'start'
        Antonyms = 'start'
        URL_1 = "https://www.merriam-webster.com/thesaurus/"
        URL = 'https://www.dictionary.com/browse/'

        
        html_content_1 = get_html_content(word, URL)
        try:
            soup_1 = bs(html_content_1, 'html.parser')
            info1 = soup_1.find(class_='one-click-content css-nnyc96 e1q3nk1v1').text
        except:
            info1 = "No Meaning for "+str(word)

        html_content_2 = get_html_content(word, URL_1)
        
        try:
            soup_2 = bs(html_content_2, 'html.parser')
            info = soup_2.find_all(class_='mw-list')
            Antonyms = ''.join(str(info[8].text).strip().split())
        except:
            Antonyms = "No Antonyms for " + str(word)


        result = dict()
        result['a'] = word
        result['meaning'] = info1
        result['Antonyms'] = Antonyms
    return render(request, 'home.html', {'result': result})