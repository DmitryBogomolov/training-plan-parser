#!/usr/bin/python3

import re
import json
from process import process

DAY_PATTERN = '\\d+ день'
RATIO_EXERCISE_PATTERN = re.compile('(\\d+)% (\\d+)х(\\d+)')
SIMPLE_EXERCISE_PATTERN = re.compile('(\\d+)х(\\d+)')

def parse(data):
    lines = re.split('\n+', data)

    lines = list(filter(None, map(str.strip, lines)))
    week = lines[0]

    positions = []
    for i, line in enumerate(lines):
        if re.search(DAY_PATTERN, line):
            positions.append(i)
    positions.append(len(lines))

    patterns = []
    weights = []
    for line in lines[1:positions[0]]:
        parts = line.split(' ')
        name = parts[0].strip()
        weight = int(parts[1].strip())
        pattern = re.compile(name.lower(), re.IGNORECASE)
        weights.append({ 'name': name, 'weight': weight })
        patterns.append({ 'pattern': pattern, 'weight': weight })

    days = []
    process_line = lambda line: extract_exercise(line, patterns)
    for i, pos in enumerate(positions[:-1]):
        items = lines[pos + 1:positions[i + 1]]
        days.append({
            'name': lines[pos],
            'exercises': list(map(process_line, items))
        })

    return json.dumps({
        'week': week,
        'weights': weights,
        'days': days
    }, ensure_ascii=False, indent=2) + '\n'

def extract_exercise(line, patterns):
    return extract_exercise_by_ratio_pattern(line, patterns) \
        or extract_exercise_by_simple_pattern(line)

def extract_exercise_by_ratio_pattern(line, patterns):
    name = check_pattern(line, RATIO_EXERCISE_PATTERN)
    if not name:
        return None
    weight = select_weight_by_name(name, patterns)
    sets = []
    for match in re.finditer(RATIO_EXERCISE_PATTERN, line):
        ratio, reps, count = match.groups()
        k = int(ratio) / 100
        obj = {
            'ratio': k,
            'weight': calculate_weight(k, weight),
            'count': int(reps)
        }
        for _ in range(int(count)):
            sets.append(obj)
    return {
        'name': name,
        'sets': sets
    }

def check_pattern(line, pattern):
    match = re.search(pattern, line)
    if match:
        return line[:match.start()].strip()
    return None

def select_weight_by_name(name, patterns):
    for obj in patterns:
        if obj['pattern'].search(name):
            return obj['weight']
    return None

def calculate_weight(ratio, weight):
    val = ratio * weight
    return round(val / 5) * 5

def extract_exercise_by_simple_pattern(line):
    name = check_pattern(line, SIMPLE_EXERCISE_PATTERN)
    if not name:
        return None
    count, reps = re.search(SIMPLE_EXERCISE_PATTERN, line).groups()
    sets = []
    obj = {
        'count': int(reps)
    }
    for _ in range(int(count)):
        sets.append(obj)
    return {
        'name': name,
        'sets': sets
    }

process(parse)
