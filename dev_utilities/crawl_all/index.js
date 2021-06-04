const https = require('http')
const DELAY = 500

function http_get(link, func_cb) {
    const req = https.request(link, res => {
        let html = ''
        res.on('data', (data) => { html += data })
        res.on('end', () => { func_cb(html) })
    })
    req.on('error', error => { console.error(error) })
    req.end()
}

http_get("http://127.0.0.1:3000/moses", (data) => {
    const modules = JSON.parse(data).modules
    let i = 0
    const loop = setInterval(() => {
        const current = i
        http_get(`http://127.0.0.1:3000/moses/${modules[current].number}`, (_module) => {
            const module = JSON.parse(_module)
            console.log(current + ": " + module.german.title)
        })
        i++
        if (i >= modules.length)
            clearInterval(loop)
    }, DELAY)
})