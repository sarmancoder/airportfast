document.addEventListener('alpine:init', () => {
    const idPrefix = "id: "
    Alpine.data('responses', () => ({
        idThread: '',
        questionToSend: '',
        lines: [],
        isLoading: false,
        async sendQuestion() {
            const question = this.questionToSend.trim()
            if (this.isLoading || !question) {
                return
            }

            this.isLoading = true

            if (this.idThread.length > 0) {
                this.lines.push({ type: 'separator' })
            }

            this.lines.push({
                type: 'question',
                text: question
            })

            try {
                const response = await fetch('/question', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        question,
                        id: this.idThread
                    })
                })

                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`)
                }

                const reader = response.body.getReader()
                const td = new TextDecoder()
                let valueAcc = ""

                const res = {
                    type: 'response',
                    text: '<p>Preparando tu respuesta…</p>'
                }
                this.lines.push(res)
                const indres = this.lines.indexOf(res)

                while (true) {
                    const { done, value } = await reader.read()
                    if (done) break
                    const decoded = td.decode(value)
                    if (decoded.startsWith(idPrefix)) {
                        this.idThread = decoded.replace(idPrefix, '')
                        continue
                    }
                    valueAcc += decoded
                    this.lines[indres].text = DOMPurify.sanitize(marked.parse(valueAcc))
                }

                this.questionToSend = ''
            } catch (error) {
                console.error('No se pudo completar la consulta:', error)
                this.lines.push({
                    type: 'error',
                    text: 'Ha ocurrido un problema al consultar. Inténtalo de nuevo.'
                })
            } finally {
                this.isLoading = false
            }
        }
    }))
})