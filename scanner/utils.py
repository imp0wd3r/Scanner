import re
import random


def std_url(url):
    """Standardize the URL."""

    if not re.search('^http[s]*://', url, re.I):
        if re.search(':443[/]*$', url, re.I):
            url = 'https://' + url
        else:
            url = 'http://' + url

    return url


def get_random_agent():
    """Return random User-Agent."""

    ua_list = [
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E),'
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50'
    ]

    return random.choice(ua_list)