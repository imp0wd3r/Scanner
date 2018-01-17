import requests


def sens_scan(target, timeout):
    url = target['url']
    sens = target['sens']
    result = {}

    if url.endswith('/'):
        vuln_url = '{}{}'.format(url, sens)
    else:
        vuln_url = '{}/{}'.format(url, sens)
    
    rep = requests.get(vuln_url, timeout=int(timeout), allow_redirects=False)
    status = rep.status_code
    
    if status != 404:
        result = {
            'url': url,
            'sens': sens,
            'status': status,
            'len': len(rep.content)
        }

        if status in [301, 302]:
            result.update({
                'redirect': rep.headers['Location']
            })
    
    return result