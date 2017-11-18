from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

URLS = {'callpage': 'https://www.callpage.io',
        'calendly': 'https://calendly.com',
        'JustWorks': 'https://justworks.com'}

VALID_TAGS = ['meta', 'a', 'title']

DEFINITIONS = ['features',
               'pricing',
               'integrations']

SYNONYMS = {'product': DEFINITIONS[0],
            'features': DEFINITIONS[0],
            'pricing': DEFINITIONS[1],
            'plans': DEFINITIONS[1],
            'integrations': DEFINITIONS[2]
            }

SOCIAL_MEDIA = ['facebook.com/',
                'twitter.com/',
                'linkedin.com/']


def main():

    return_dict = dict()

    for URL in URLS:
        result = urlopen(URLS[URL])
        html = result.read()
        contents = sanitize_html(html, URLS[URL])
        return_dict[URL] = contents

    print(json.dumps(return_dict))


def sanitize_html(html, url):

    soup = BeautifulSoup(html, 'html.parser')
    info = {'URL': url}

    for tag in soup.findAll(VALID_TAGS):

        if tag.name == 'meta':
            try:
                if tag['name'] == 'description':
                    info['description'] = tag['content']
            except Exception:
                pass

        elif tag.name == 'a':
            try:
                if tag.text.lower() in SYNONYMS:
                    if url in tag['href']:
                        info[SYNONYMS[tag.text.lower()]] = tag['href']
                    else:
                        info[SYNONYMS[tag.text.lower()]] = url + tag['href']
                else:
                    for i in SOCIAL_MEDIA:
                        if i in tag['href']:
                            info[i[:-5]] = tag['href']
                            break
            except Exception:
                pass

        elif tag.name == 'title':
            info['title'] = tag.text

    return info


if __name__ == "__main__":
    main()
