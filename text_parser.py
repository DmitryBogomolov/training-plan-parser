import os
import re

def make_view(items, start, end):
    def get_items():
        for i in range(start, end):
            yield items[i]
    return get_items

def split_to_parts(lines):
    anchors = []
    is_data = True
    for i in range(len(lines)):
        if bool(lines[i]) == is_data:
            anchors.append(i)
            is_data = not is_data
    if len(anchors) % 2 == 1:
        anchors.append(len(lines))
    parts = []
    for i in range(0, len(anchors), 2):
        start, end = anchors[i], anchors[i + 1]
        parts.append(make_view(lines, start, end))
    return parts

WEIGHT_PATTERN = re.compile(r'(\d+)$')
RATIO_EXERCISE_PATTERN = re.compile(r'(\d+)%\s(\d+)[x|\*](\d+)')
SIMPLE_EXERCISE_PATTERN = re.compile(r'(\d+)[x\*](\d+)')

def parse_weights(lines_source):
    weight_data = {}
    for line in lines_source():
        match = WEIGHT_PATTERN.search(line.strip())
        if not match:
            raise Exception('bad line: ' + line)
        name = line[:match.start()].strip()
        weight = int(match.group(0))
        weight_data[name] = weight
    return weight_data

def process_ratio_block(match):
    ratio, reps, count = map(int, match.groups())
    return [{'reps': reps, 'ratio': ratio / 100.0}] * count

def process_simple_block(match):
    reps, count = map(int, match.groups())
    return [{'reps': reps}] * count

def parse_exercise(text):
    pattern = None
    match = None
    process_block = None
    if not match:
        pattern = RATIO_EXERCISE_PATTERN
        process_block = process_ratio_block
        match = pattern.search(text)
    if not match:
        pattern = SIMPLE_EXERCISE_PATTERN
        process_block = process_simple_block
        match = pattern.search(text)
    if not match:
        raise Exception('bad line: ' + text)

    name = text[:match.start()].strip()
    sets = []
    while match:
        this_sets = process_block(match)
        sets.extend(this_sets)
        match = pattern.search(text, match.end())

    return {'name': name, 'sets': sets}

def parse_day(lines_source):
    lines = lines_source()
    name = next(lines)
    exercises = []
    for line in lines:
        exercises.append(parse_exercise(line.strip()))
    return {'title': name, 'exercises': exercises}


def parse(content):
    parts = split_to_parts(content.splitlines())
    if len(parts) < 3:
        raise Exception('not enough data')
    title = os.linesep.join(parts[0]())
    weight_data = parse_weights(parts[1])
    days = []
    for i in range(2, len(parts)):
        days.append(parse_day(parts[i]))
    return {
        'title': title,
        'weights': weight_data,
        'days': days,
    }
