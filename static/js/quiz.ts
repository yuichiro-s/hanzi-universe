let question = '';
let userInput = [];
let correctAnswer = [];

const CLASS_OK = 'result-ok';
const CLASS_NG = 'result-ng';

function getElementPinyin() {
    return document.getElementById('pinyin');
}

function getElementHanzi() {
    return document.getElementById('hanzi');
}

async function checkAnswer() {
    getElementPinyin().hidden = false;
    if (JSON.stringify(userInput) === JSON.stringify(correctAnswer)) {
        document.body.classList.add(CLASS_OK);
    } else {
        document.body.classList.add(CLASS_NG);
    }
    let obj = {
        'question': question,
        'answer': userInput,
        'correct': correctAnswer,
    };
    return fetch('user_answer',
        {
            method: 'POST',
            body: JSON.stringify(obj),
            headers: {
                'Content-Type': 'application/json'
            },
        },
    );
}

function isDone() {
    return userInput.length >= correctAnswer.length;
}

function keyPressed(keyName: string) {
    console.log('Pressed:', keyName);
    if (keyName === '1' ||
        keyName === '2' ||
        keyName === '3' ||
        keyName === '4' ||
        keyName === '5') {
        let num = Number.parseInt(keyName);
        userInput.push(num);
        if (isDone()) {
            checkAnswer();
        }
    } else if (keyName === ' ') {
        if (isDone()) {
            nextQuestion();
        }
    }
}

async function nextQuestion() {
    let res = await fetch('get_next_question');
    let {question, answer, pinyin} = await res.json();

    getElementHanzi().textContent = question;
    let ePinyin = getElementPinyin();
    ePinyin.textContent = pinyin;
    ePinyin.hidden = true;
    document.body.classList.remove(CLASS_OK, CLASS_NG);

    console.log(question, answer, pinyin);

    userInput = [];
    correctAnswer = answer;
}

async function init() {
    document.addEventListener('keydown', (event) => {
        const keyName = event.key;
        keyPressed(keyName);
    }, false);
    nextQuestion();
}

init();
