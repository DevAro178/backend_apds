import json
import requests
import urllib

class IPQS:
    key = 'ci1Hud3avMw8bXfIJ4azQ8dP032PvMb3'
    def malicious_url_scanner_api(self, url: str, vars: dict = {}) -> dict:
        url = 'https://www.ipqualityscore.com/api/json/url/%s/%s' % (self.key, urllib.parse.quote_plus(url))
        x = requests.get(url, params = vars)
        result=json.loads(x.text)
        if 'success' in result and result['success'] == True:
            return result['unsafe']
        else: return False