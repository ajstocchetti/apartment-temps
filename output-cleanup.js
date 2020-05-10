const fs = require('fs');
const filedata = fs.readFileSync('./temps.csv', 'utf-8');

const slim = filedata.split('\n').map((val, index) => {
    const arr = val.split(',');
    if (index < 1) return ['time', 'temp (F)', 'humidity (%)'];
    return [
        new Date(arr[1] / 1000000),
        (+arr[5]).toFixed(2),
        arr[3],
    ];
})
.map(x => x.join(','))
.join('\n');

fs.writeFileSync('./apartment-temps.csv', slim);