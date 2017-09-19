const readStdin = require('./stdin');

const DAY_PATTERN = '\\d+ день';
const RATIO_EXERCISE_PATTERN = '(\\d+)% (\\d+)х(\\d+)';
const SIMPLE_EXERCISE_PATTERN = '(\\d+)х(\\d+)';

function extractExercise(line, patterns) {
    return extractExerciseByRatioPattern(line, patterns) || extractExerciseBySimplePattern(line);
}

function checkPattern(line, pattern) {
    const check = new RegExp(pattern).exec(line);
    return check ? line.substr(0, check.index).trim() : null;
}

function selectWeightByName(name, patterns) {
    const obj = patterns.find(item => item.pattern.test(name));
    return obj ? obj.weight : null;
}

function calculateWeight(ratio, weight) {
    const val = ratio * weight;
    return Math.round(val / 5) * 5;
}

function extractExerciseByRatioPattern(line, patterns) {
    const name = checkPattern(line, RATIO_EXERCISE_PATTERN);
    if (!name) {
        return null;
    }
    const regexp = new RegExp(RATIO_EXERCISE_PATTERN, 'g');
    const weight = selectWeightByName(name, patterns);
    let item;
    const sets = [];
    while (item = regexp.exec(line)) {
        const ratio = Number(item[1]) / 100;
        const obj = {
            ratio,
            weight: calculateWeight(ratio, weight),
            count: Number(item[2])
        };
        const ii = Number(item[3]);
        for (let i = 0; i < ii; ++i) {
            sets.push(obj);
        }
    }
    return {
        name,
        sets
    };
}

function extractExerciseBySimplePattern(line) {
    const name = checkPattern(line, SIMPLE_EXERCISE_PATTERN);
    if (!name) {
        return null;
    }
    const item = new RegExp(SIMPLE_EXERCISE_PATTERN).exec(line);
    const obj = {
        count: Number(item[1])
    };
    const ii = Number(item[2]);
    const sets = [];
    for (let i = 0; i < ii; ++i) {
        sets.push(obj);
    }
    return {
        name,
        sets
    };
}

function parse(data) {
    const lines = data.split('\n').map(x => x.trim()).filter(x => x);
    const week = lines[0];
    const list = [];
    const regexp = new RegExp(DAY_PATTERN);
    lines.forEach((line, i) => {
        if (regexp.test(line)) {
            list.push(i);
        }
    });
    const patterns = [];
    const weights = [];
    lines.slice(1, list[0]).forEach((value) => {
        const parts = value.trim().split(' ');
        const name = parts[0].trim();
        const weight = Number(parts[1].trim());
        weights.push({ name, weight });
        patterns.push({
            pattern: new RegExp(name.toLowerCase(), 'i'),
            weight
        });
    });
    const days = list.map((pos, i) => {
        const items = lines.slice(pos + 1, list[i + 1]);
        return {
            name: lines[pos],
            exercises: items.map(line => extractExercise(line.trim(), patterns))
        };
    });
    return {
        week,
        weights,
        days
    };
}

readStdin().then((data) => {
    process.stdout.write(JSON.stringify(parse(data), null, 2) + '\n');
});
