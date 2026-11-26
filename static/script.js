document.addEventListener('alpine:init', () => {
    const idPrefix = "id: "
    Alpine.data('responses', () => ({
        idThread: '',
        questionToSend: '',
        lines: [],
        async sendQuestion() {
            if (this.idThread.length > 0) {
                this.lines.push({ type: 'separator' })
            }

            this.lines.push({
                type: 'question',
                text: this.questionToSend
            })

            const response = await fetch('/question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': 'Bearer token'
                },
                body: JSON.stringify({
                    question: this.questionToSend,
                    id: this.idThread
                })
            });

            if (!response.ok) {
                /*responseHTMLContainer.innerHTML = `# Hubo un error
> Revise la consola y contacte al administrador`*/
                throw new Error(`Error HTTP: ${response.status}`);
            }

            const reader = await response.body.getReader()

            const td = new TextDecoder()

            let valueAcc = ""

            const res = {
                type: 'response',
                text: 'Cargando...'
            }

            this.lines.push(res)
            const indres = this.lines.indexOf(res)

            while (true) {
                const { done, value } = await reader.read('utf-8')
                if (done) break
                const decoded = td.decode(value)
                if (decoded.startsWith(idPrefix)) {
                    this.idThread = decoded.replace(idPrefix, '')
                    continue
                }
                valueAcc += decoded
                this.lines[indres].text = marked.parse(valueAcc)
            }

            this.questionToSend = ''

            console.log(this.lines)
        }
    }))
})