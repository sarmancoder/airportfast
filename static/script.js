function questionFormSubmit(e) {
    e.preventDefault()
    const question = e.target['question'].value
    console.log(`Pregunta a resolver: ${question}`)
    e.target.reset()
}