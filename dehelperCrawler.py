import requests
import lxml.html


class DeHelperCrawler(object):

    def __init__(self):
        self.base_url = "https://www.godic.net/dicts/de/"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        self.accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        self.headers = {
            "user-agent": self.user_agent,
            "accept": self.accept
        }
        self.bean = None

    def get_word(self, bean):
        self.bean = bean
        url = self.base_url + self.bean.word
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == requests.codes.ok:
                return response.text
        except Exception as ex:
            print(ex)

    def grep(self, content):
        dom = None
        try:
            dom = lxml.html.fromstring(content)
        except Exception as ex:
            print(ex)
        if dom:
            word = dom.cssselect("#exp-head .word")[0].text
            phonitic = dom.cssselect("#exp-head .Phonitic")[0].text
            sentence = dom.cssselect("#ExpLJChild > .lj_item")[0].cssselect('p>.line').text
            sentences = dom.cssselect("#ExpLJChild > .lj_item")[0].cssselect('p>.exp').text
