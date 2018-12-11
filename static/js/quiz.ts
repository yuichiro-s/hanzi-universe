console.log('hello');

(async function () {
    let res = await fetch('get_next_question');
    let {question, answer} = await res.json();
    console.log(question, answer);

    let obj = {
        'question': 'hello',
        'answer': [2, 3],
    };
    let result = await fetch('user_answer',
        {
            method: 'POST',
            body: JSON.stringify(obj),
            headers: {
                'Content-Type': 'application/json'
            },
        },
    );
})();
