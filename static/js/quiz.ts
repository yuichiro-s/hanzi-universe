async function init() {
    document.addEventListener('keydown', (event) => {
        const keyName = event.key;
        console.log(event);

    }, false);
}

init();
