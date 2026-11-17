async function questionFormSubmit(e) {
    e.preventDefault()
    const question = e.target['question'].value
    console.log(`Pregunta a resolver: ${question}`)

    const response = await fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': 'Bearer token'
        },
        body: JSON.stringify({ question })
    });

    if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
    }

    const reader = await response.body.getReader()

    const td = new TextDecoder()


    while (true) {
        const { done, value } = await reader.read('utf-8')
        if (done) break
        const valueutf = td.decode(value)
        console.log(valueutf)
    }

    e.target.reset()
}