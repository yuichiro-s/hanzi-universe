def get_next_question():
    print('Get next question.')

    return {
        'question': '你好',
        'answer': [3, 3],
        'pinyin': 'ni3hao3',
    }


def user_answer(question, answer, correct):
    print('User answer:', question, answer)
