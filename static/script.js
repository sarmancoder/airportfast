async function questionFormSubmit(e) {
    e.preventDefault()
    const responseHTMLContainer = document.getElementById('response')
    responseHTMLContainer.innerHTML = "Cargando..."

    await new Promise((r) => setTimeout(r, 500))

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
        responseHTMLContainer.innerHTML = `# Hubo un error
> Revise la consola y contacte al administrador
`
        throw new Error(`Error HTTP: ${response.status}`);
    }

    responseHTMLContainer.innerHTML = ""

    const reader = await response.body.getReader()

    const td = new TextDecoder()


    while (true) {
        const { done, value } = await reader.read('utf-8')
        if (done) break
        const valueutf = marked.parse(td.decode(value))
        responseHTMLContainer.innerHTML += DOMPurify.sanitize(valueutf);
    }

    e.target.reset()
}