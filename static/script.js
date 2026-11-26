async function questionFormSubmit(e) {
    e.preventDefault()
    const responseHTMLContainer = document.getElementById('response')
    const threadStrong = document.getElementById('thread_id')
    responseHTMLContainer.insertAdjacentHTML('beforeend', '<p>Cargando</p>')

    await new Promise((r) => setTimeout(r, 500))

    const question = e.target['question'].value
    console.log(`Pregunta a resolver: ${question}`)

    const response = await fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': 'Bearer token'
        },
        body: JSON.stringify({ question, id: threadStrong.innerText })
    });

    if (!response.ok) {
        responseHTMLContainer.innerHTML = `# Hubo un error
> Revise la consola y contacte al administrador
`
        throw new Error(`Error HTTP: ${response.status}`);
    }

    // responseHTMLContainer.innerHTML = ""
    if (threadStrong.innerText.length > 0) {
        responseHTMLContainer.innerHTML += "<hr />"
    }

    const reader = await response.body.getReader()

    const td = new TextDecoder()

    let valueAcc = ""

    const idPrefix = "id: "


    while (true) {
        const { done, value } = await reader.read('utf-8')
        if (done) break
        const decoded = td.decode(value)
        console.log(decoded)
        if (decoded.startsWith(idPrefix) && threadStrong.innerText.length === 0) {
            threadStrong.innerText = decoded.replace(idPrefix, '')
            continue
        }
        valueAcc += decoded
        const valueutf = marked.parse(valueAcc)
        console.log(valueutf)
        responseHTMLContainer.innerHTML = DOMPurify.sanitize(valueutf);
    }

    e.target.reset()
}