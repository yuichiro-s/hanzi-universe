import random

from hanzi_universe.hanzi import ranks, lookup, get_category
from hanzi_universe.pinyin import decode_pinyin


def prepare_questions():
    questions = []
    for hanzi, rank in list(ranks.items()):
        if rank and rank <= 3000:
            for entry in lookup(hanzi)['entries']:
                pron = entry['pron']
                words = entry['words'][:5]
                for word in words:
                    chars = word[0]
                    if len(chars) == 2:
                        questions.append((hanzi, pron, word))
    return questions


def scorer(hanzi_pron):
    return hanzi_pron.ng - hanzi_pron.ok


def get_next_question(hanzi_pron_list):
    print('Get next question.')

    if len(hanzi_pron_list) == 0 or random.randint(0, 1):
        print('Random question')
        hanzi, pron, word = random.choice(all_questions)
    else:
        print('Previous hanzi question')
        random.shuffle(hanzi_pron_list)
        hanzi_pron_list.sort(key=scorer, reverse=True)
        print('Chosen: ' + str(hanzi_pron_list[0]))
        hanzi_pron = hanzi_pron_list[0].hanzi_pron
        hanzi, pron = hanzi_pron.split('/')
        word = None
        for entry in lookup(hanzi)['entries']:
            if pron == entry['pron']:
                word = random.choice(entry['words'][:5])
        if word is None:
            hanzi, pron, word = random.choice(all_questions)

    word_chars, word_pron, word_defs = word
    answer = []
    pinyin = []
    pinyin_no_tone = []
    for p in word_pron:
        answer.append(p[-1])
        pinyin.append(decode_pinyin(p))
        pinyin_no_tone.append(p[:-1])
    question = []
    for c, rank in word_chars:
        question.append((c, rank, get_category(rank)))

    print(hanzi, pron, word)

    return {
        'key': (hanzi, pron),
        'question': question,
        'answer': answer,
        'pinyin': pinyin,
        'pinyinNoTone': pinyin_no_tone,
        'pinyinOrig': word_pron,
        'defs': word_defs,
    }


def user_answer(question, answer):
    print('User answer:', question, answer)

    res = []
    for hanzi, t_user, t_correct, p in zip(question['question'], answer,
                                           question['answer'],
                                           question['pinyinOrig']):
        ok = t_user == t_correct
        print(ok, hanzi, p)
        res.append((ok, hanzi[0], p))
    return res


all_questions = prepare_questions()
