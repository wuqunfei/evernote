import requests


class LingueeCrawler(object):
    def __init__(self):
        self.address = "https://lingapi.herokuapp.com/api"
        self.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        self.bean = None

    def get_word(self, bean):
        values = None
        self.bean = bean
        params = {"src": "de", "dst": "en", "q": bean.word}
        response = requests.get(self.address, params=params, headers=self.headers)
        if response.status_code == requests.codes.ok:
            values = response.json()
        return values

    def grep(self, matches):
        for match in matches:
            word_type = match['word_type']
            if word_type != None:
                for k, v in word_type.items():
                    pass
