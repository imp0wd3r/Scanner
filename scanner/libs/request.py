import requests
from requests.hooks import default_hooks
from requests.models import DEFAULT_REDIRECT_LIMIT
from requests.cookies import cookiejar_from_dict
from requests.compat import OrderedDict
from requests.adapters import HTTPAdapter
from requests.utils import default_headers
from requests.packages.urllib3._collections import RecentlyUsedContainer

from scanner.utils import get_random_agent


def patch_requests(args):
    """Patch the requests module. Based on pocsuite."""

    if hasattr(requests.packages.urllib3.util, '_Default'):
        requests.packages.urllib3.util._Default = None
    else:
        requests.packages.urllib3.util.timeout._Default = None

    def set_verify_to_false():
        def cert_verify(self, conn, url, verify, cert):
            conn.cert_reqs = 'CERT_NONE'
            conn.ca_certs = None
        requests.adapters.HTTPAdapter.cert_verify = cert_verify

    def set_default_headers():
        def session_init(self):
            self.headers = default_headers()
            if args.random_agent:
                self.headers.update({'User-Agent': get_random_agent()})
            elif args.user_agent:
                self.headers.update({'User-Agent': args.user_agent})

            self.auth = None

            if args.proxy:
                # Currently only supports socks5
                self.proxies = {
                    'http': 'socks5://{}'.format(args.proxy),
                    'https': 'socks5://{}'.format(args.proxy)
                }
            else:
                self.proxies = {}

            self.hooks = default_hooks()
            self.params = {}
            self.stream = False
            self.verify = True
            self.cert = None
            self.max_redirects = DEFAULT_REDIRECT_LIMIT
            self.trust_env = True
            self.cookies = cookiejar_from_dict(args.cookies)
            self.adapters = OrderedDict()
            self.mount('https://', HTTPAdapter())
            self.mount('http://', HTTPAdapter())
            self.redirect_cache = RecentlyUsedContainer(1000)
        requests.sessions.Session.__init__ = session_init

    set_verify_to_false()
    set_default_headers()
    requests.packages.urllib3.disable_warnings()
