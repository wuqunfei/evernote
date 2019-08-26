import threading
import os

from dehelperCrawler import DeHelperCrawler
from lingueeCrawler import LingueeCrawler


class DeWord(object):

    def __init__(self, word):
        self.word = word
        self.note = None
        self.phonetic_text = None
        self.phonetic_mp3 = None
        self.pos = None
        self.article = None
        self.chinese = None
        self.english = None
        self.examples = []
        self.photo = None
        self.link = None
        self.tag = None

    def with_word(self, word):
        self.word = word
        return self

    def with_note(self, note):
        self.note = note
        return self

    def with_phonetic_text(self, text):
        self.phonetic_text = text
        return self

    def with_phonetic_mp3(self, mp3):
        self.phonetic_mp3 = mp3
        return self

    def with_pos(self, pos):
        self.pos = pos
        return self

    def with_article(self, article):
        self.article = article
        return self

    def with_chinese(self, chinese):
        self.chinese = chinese
        return self

    def with_english(self, english):
        self.english = english
        return self

    def with_link(self, link):
        self.link = link
        return self

    def add_example(self, origin, translation):
        instance = {'origin': origin, 'translation': translation}
        self.examples.append(instance)
        return self

    def with_tag(self, tag):
        self.tag = tag
        return self


class CrawlerWorker(threading.Thread):

    def __init__(self, word_de, note, tag):
        threading.Thread.__init__(self)
        self.filter(word_de)
        self.bean.with_note(note)
        self.bean.with_tag(tag)

        self.dehelper = DeHelperCrawler()
        self.lingueer = LingueeCrawler()

    def filter(self, word):
        filtered_word = None
        self.bean = DeWord(None)
        if len(word) > 4:
            value = word[:4]
            if value == "die ":
                self.bean.with_article('die')
                filtered_word = word[4:]
            elif value == "das ":
                self.bean.with_article('das')
                filtered_word = word[4:]
            elif value == "der ":
                self.bean.with_article('der')
                filtered_word = word[4:]
            else:
                filtered_word = word
        else:
            filtered_word = word
        filtered_word = filtered_word.replace("(", "")
        filtered_word = filtered_word.replace(")", "")
        filtered_word = filtered_word.strip()
        self.bean.with_word(filtered_word)

    def run(self) -> None:
        print(self.dehelper.get_word(self.bean))
        print(self.lingueer.get_word(self.bean))


class ProcessWord(object):
    def __init__(self):
        self.path = "B1"

    def read_words(self):
        files = os.listdir(self.path)
        words = []
        for file in files:
            handler = open(os.path.join(self.path, file), mode='r')
            try:
                lines = handler.read().splitlines()
                index = 0
                for line in lines[::2]:
                    ww = lines[index: index + 2]
                    if file.find("-") != -1:
                        file_names = file.split("-")
                        ww.append(file_names[1])
                    else:
                        ww.append(file)
                    words.append(ww)
                    index += 2
            finally:
                handler.close()

        return words

    def filter_word(self, words):
        for word in words:
            try:
                crawler_worker = CrawlerWorker(word[0], word[1], word[2])
                crawler_worker.start()
            except Exception as ex:
                print(word)


def main():
    process = ProcessWord()
    words = process.read_words()
    filtered_words = process.filter_word(words)


if __name__ == '__main__':
    main()
