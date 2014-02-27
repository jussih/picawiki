# encoding: utf-8

import sys
import wikipedia
import goslate

amount = int(sys.argv[1])
wikipedia.set_lang('fi')
gs = goslate.Goslate()

langs = ['en', 'de', 'se', 'cs', 'da', 'nl', 'et']
#full_langs = gs.get_languages()


def get_random_wikipedia_titles(amount, per_cycle=10):
    left = amount
    while left > 0:
        get = min(per_cycle, left)
        left -= get
        yield wikipedia.random(pages=get)


def process(bunch):
    for word in bunch:
        print word

for titles in get_random_wikipedia_titles(amount):
    bunch = []
    for title in titles:
        word = {}
        try:
            page = wikipedia.page(title=title)
        except wikipedia.exceptions.DisambiguationError:
            print "Disambiguation in title %s, skipping"%title
            continue
        word['word'] = title
        word['description'] = page.summary
        word['translations'] = {}
        try:
            word['imageurl'] = page.images()[0]
        except:
            word['imageurl'] = "http://www.catster.com/files/original.jpg"
        bunch.append(word)
    for lang in langs:
        translations = gs.translate([word['word'] for word in bunch], lang, 'fi')

        for translation, word in zip(translations, bunch):
            word['translations'][lang] = translation

    process(bunch)

