const https = require('http')
const DELAY = 2 * 1000

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
    const response = JSON.parse(data)
    console.log(response)
    const loop = setInterval(() => {
        console.log(response.modules[0])
    }, DELAY)
})