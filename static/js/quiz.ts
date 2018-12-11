let currentQuestion: {
    key: [string, string],
    question: string,
    answer: string[],
    pinyin: string[],
    pinyinNoTone: string[],
    defs: string[],
} = null;
let userInput = [];

const CLASS_OK = 'result-ok';
const CLASS_NG = 'result-ng';

async function checkAnswer() {
    document.getElementById('pinyin').hidden = false;
    document.getElementById('defs').hidden = false;
    if (JSON.stringify(userInput) === JSON.stringify(currentQuestion.answer)) {
        document.body.classList.add(CLASS_OK);
    } else {
        document.body.classList.add(CLASS_NG);
    }
    let obj = {
        'question': currentQuestion,
        'answer': userInput,
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
    return userInput.length >= currentQuestion.answer.length;
}

function keyPressed(keyName: string) {
    console.log('Pressed:', keyName);
    if (keyName === '1' ||
        keyName === '2' ||
        keyName === '3' ||
        keyName === '4' ||
        keyName === '5') {
        if (!isDone()) {
            userInput.push(keyName);
            if (isDone()) {
                checkAnswer();
            }
        }
    } else if (keyName === ' ') {
        if (isDone()) {
            nextQuestion();
        }
    }
}

async function nextQuestion() {
    let res = await fetch('get_next_question');
    currentQuestion = await res.json();
    console.log(currentQuestion);

    document.body.classList.remove(CLASS_OK, CLASS_NG);

    let eHanzi = document.getElementById('hanzi');
    eHanzi.innerHTML = '';
    for (let [c, rank, cat] of currentQuestion.question) {
        let e = document.createElement('a');
        e.setAttribute('href', 'hanzi/' + c);
        e.innerText = c;
        e.classList.add('hanzi');
        e.classList.add('category-' + cat);
        let eSub = document.createElement('sub');
        eSub.innerText = rank;
        e.appendChild(eSub);
        eHanzi.appendChild(e);
    }
    let ePinyin = document.getElementById('pinyin');
    ePinyin.innerHTML = '';
    for (let i = 0; i < currentQuestion.answer.length; i++) {
        let t = currentQuestion.answer[i];
        let p = currentQuestion.pinyin[i];
        let pNoTone = currentQuestion.pinyinNoTone[i];
        let e = document.createElement('a');
        e.setAttribute('href', 'pinyin/' + pNoTone);
        e.innerText = p;
        e.classList.add('tone' + t);
        ePinyin.appendChild(e);
    }
    ePinyin.hidden = true;

    let eDefs = document.getElementById('defs');
    eDefs.innerHTML = '';
    for (let def of currentQuestion.defs) {
        let c = document.createElement('span');
        c.innerText = def;
        c.classList.add('def-item');
        eDefs.appendChild(c);
    }
    eDefs.hidden = true;

    userInput = [];
}

async function init() {
    document.addEventListener('keydown', (event) => {
        const keyName = event.key;
        keyPressed(keyName);
    }, false);
    nextQuestion();
}

init();
