import random

from hanzi_universe.hanzi import ranks, lookup
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


def get_next_question():
    print('Get next question.')

    hanzi, pron, word = random.choice(all_questions)
    word_chars, word_pron, word_defs = word
    answer = []
    pinyin = []
    pinyin_orig = []
    for p in word_pron:
        answer.append(p[-1])
        pinyin.append(decode_pinyin(p))
        pinyin_orig.append(p[:-1])
    question = word_chars

    return {
        'key': (hanzi, pron),
        'question': question,
        'answer': answer,
        'pinyin': pinyin,
        'pinyinOrig': pinyin_orig,
        'defs': word_defs,
    }


def user_answer(question, answer):
    print('User answer:', question, answer)

    for hanzi, t_user, t_correct in zip(question['question'], answer, question['answer']):
        if t_user == t_correct:
            # OK
            pass
        else:
            # NG
            pass


all_questions = prepare_questions()
