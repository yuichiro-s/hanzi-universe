from flask import Flask, render_template, request, json

from hanzi_universe.hanzi import lookup, lookup_pinyin, get_category, ranks, INF
from hanzi_universe.pinyin import decode_pinyin
from hanzi_universe.quiz import get_next_question, user_answer

import random

app = Flask(__name__)


@app.route('/hanzi/<string:hanzi>')
def get_hanzi(hanzi):
    max_rank = request.args.get('max_rank', 3000)
    data = lookup(hanzi, max_rank)
    obj = prepare(data)
    return render_template('hanzi.html', obj=obj)


@app.route('/pinyin/<string:pinyin>')
def get_pinyin(pinyin):
    max_rank = request.args.get('max_rank', 3000)
    obj = lookup_pinyin(pinyin, max_rank)
    return render_template('pinyin.html', obj=obj)


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


def make_json_response(data):
    return app.response_class(
        response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/get_next_question')
def get_next_question_api():
    data = get_next_question()
    return make_json_response(data)


@app.route('/user_answer', methods=['POST'])
def user_answer_api():
    res = request.get_json()
    question = res.get('question')
    answer = res.get('answer')
    user_answer(question, answer)
    return make_json_response('ok')


@app.route('/frequency')
def show_frequency_list():
    lst = sorted(ranks.items(), key=lambda kv: kv[1] or INF)
    if not request.args.get('sort'):
        random.shuffle(lst)
    max_rank = request.args.get('max_rank', 3000)
    rows = []
    row = []
    for hanzi, rank in lst:
        if not rank or rank > max_rank:
            continue
        category = get_category(rank)
        row.append((hanzi, rank, category))
        if len(row) == 20:
            rows.append(row)
            row = []
    return render_template('frequency.html', rows=rows)


def create_word_list(words):
    res = []
    for w, rank in words:
        res.append({
            'hanzi': w,
            'rank': rank,
            'category': get_category(rank),
        })
    return res


def conv_pinyin(pron):
    return decode_pinyin(pron), pron[:-1], pron[-1]


def prepare(data):
    result = {
        'hanzi': data['hanzi'],
        'rank': data['rank'],
        'category': get_category(data['rank']),
        'entries': [],
        'traditional': data['traditional'],
    }
    for entry in data['entries']:
        words = []
        for chars, pron, defs in entry['words'][:5]:
            cs = []
            for c, rank in chars:
                match = (c == data['hanzi'])
                cs.append((match, c, get_category(rank)))
            words.append((cs, list(map(conv_pinyin, pron)), defs))
        entry = {
            'pinyin':
            conv_pinyin(entry['pron']),
            'defs':
            entry['defs'],
            'same':
            create_word_list(entry['same']),
            'related1':
            create_word_list(entry['related1']),
            'related2':
            list(
                map(lambda kv: {
                    'pinyin': conv_pinyin(kv[0]),
                    'list': create_word_list(kv[1]), }, entry['related2'])),
            'words':
            words,
        }
        result['entries'].append(entry)
    return result
