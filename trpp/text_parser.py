import os
import re
from .objects import Plan, WeightInfo, Day, Exercise, SimpleSetBlock, RatioSetBlock

def split_to_parts(lines):
    anchors = []
    is_data = True
    for i, line in enumerate(lines):
        if bool(line) == is_data:
            anchors.append(i)
            is_data = not is_data
    if len(anchors) % 2 == 1:
        anchors.append(len(lines))
    parts = []
    for i in range(0, len(anchors), 2):
        start, end = anchors[i], anchors[i + 1]
        parts.append(lines[start:end])
    return parts

WEIGHT_PATTERN = re.compile(r'(\d+)$')
RATIO_EXERCISE_PATTERN = re.compile(r'(\d+)%\s(\d+)[x|\*](\d+)')
SIMPLE_EXERCISE_PATTERN = re.compile(r'(\d+)[x\*](\d+)')

def parse_weights(lines):
    weights = []
    for line in lines:
        match = WEIGHT_PATTERN.search(line.strip())
        if not match:
            raise Exception('bad line: ' + line)
        name = line[:match.start()].strip()
        weight = int(match.group(0))
        weights.append(WeightInfo(name, weight))
    return weights

def process_ratio_block(match):
    ratio, reps, count = map(int, match.groups())
    return RatioSetBlock(ratio / 100.0, reps, count)

def process_simple_block(match):
    reps, count = map(int, match.groups())
    return SimpleSetBlock(reps, count)

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
    blocks = []
    while match:
        blocks.append(process_block(match))
        match = pattern.search(text, match.end())

    return Exercise(name, blocks)

def parse_day(lines):
    name = lines[0]
    exercises = [parse_exercise(line.strip()) for line in lines[1:]]
    return Day(name, exercises)

def parse(content):
    parts = split_to_parts(content.splitlines())
    if len(parts) < 3:
        raise Exception('not enough data')
    title = os.linesep.join(parts[0])
    weights = parse_weights(parts[1])
    days = [parse_day(parts[i]) for i in range(2, len(parts))]
    return Plan(title, weights, days)
