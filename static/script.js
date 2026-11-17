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

    const data = await response.json();
    console.log('data:', data);

    e.target.reset()
}