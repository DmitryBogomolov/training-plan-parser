const stdin = process.stdin;

module.exports = () => new Promise((resolve) => {
    stdin.setEncoding('utf8');
    let data = '';
    stdin.on('readable', () => {
        const item = stdin.read();
        if (item) {
            data += item;
        } else {
            resolve(data);
        }
    });
});
