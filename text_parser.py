import os
import re
from collections import namedtuple
from itertools import repeat, chain
from functools import partial

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
        parts.append(lines[start:end])
    return parts

WEIGHT_PATTERN = re.compile(r'(\d+)$')
RATIO_EXERCISE_PATTERN = re.compile(r'(\d+)%\s(\d+)[x|\*](\d+)')
SIMPLE_EXERCISE_PATTERN = re.compile(r'(\d+)[x\*](\d+)')

WeightInfo = namedtuple('WeightInfo', ('name', 'weight'))

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

RatioSetBlock = namedtuple('RatioSetBlock', ('ratio', 'reps', 'count'))
SimpleSetBlock = namedtuple('SimpleSetBlock', ('reps', 'count'))

def process_ratio_block(match):
    ratio, reps, count = map(int, match.groups())
    return RatioSetBlock(ratio / 100.0, reps, count)

def process_simple_block(match):
    reps, count = map(int, match.groups())
    return SimpleSetBlock(reps, count)

Exercise = namedtuple('Exercise', ('name', 'blocks'))

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

Day = namedtuple('Day', ('title', 'exercises'))

def parse_day(lines):
    name = lines[0]
    exercises = [parse_exercise(line.strip()) for line in lines[1:]]
    return Day(name, exercises)

Plan = namedtuple('Plan', ('title', 'weights', 'days'))

def parse(content):
    parts = split_to_parts(content.splitlines())
    if len(parts) < 3:
        raise Exception('not enough data')
    title = os.linesep.join(parts[0])
    weights = parse_weights(parts[1])
    days = [parse_day(parts[i]) for i in range(2, len(parts))]
    return Plan(title, weights, days)

MAX_COLUMNS = 10
PAGE_TEMPLATE = '''<!doctype html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Training Plan</title>
        <style>
            table {{
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid black;
                font-size: 14px;
                text-align: left;
            }}
            .title {{
                height: 1.6em;
                font-weight: bold;
            }}
            .day {{
                height: 1.4em;
                font-weight: bolder;
            }}
            .set {{
                width: 2cm;
            }}
        </style>
    </head>
    <body>
        <div>
            <table>
                <tr>
                    <td class="title" colspan="''' + str(MAX_COLUMNS + 1) + '''">{title}</td>
                </tr>
                <tr>
                    <td></td>
                    {weights}
                </tr>
                {days}
            </table>
        <div>
    </body>
</html>
'''

WEIGHT_TEMPLATE = '<td class="set">{target.name}</td><td class="set">{target.weight}</td>'
DAY_TEMPLATE = '''
<tr><td colspan="''' + str(MAX_COLUMNS + 1) + '''">&nbsp;</td></tr>
<tr><td class="day" colspan="''' + str(MAX_COLUMNS + 1) + '''">{title}</td></tr>
{exercises}
'''
EXERCISE_TEMPLATE = '''<tr><td class="exercise">{name}</td>{sets}</tr>'''
RATIO_SET_TEMPLATE = '''<td class="set">{ratio}% {reps} / {weight}</td>'''
SIMPLE_SET_TEMPLATE = '''<td class="set">{reps}</td>'''
STUB_SET = '''<td></td>'''

def get_weight_by_name(name, weights):
    for item in weights:
        if name.startswith(item.name):
            return item.weight
    return 0

def select_set_renderer(exercise, weights):
    block = exercise.blocks[0]
    if isinstance(block, RatioSetBlock):
        weight = get_weight_by_name(exercise.name, weights)
        return partial(render_ratio_set, weight=weight)
    if isinstance(block, SimpleSetBlock):
        return render_simple_set
    raise Exception('unknown block')

def generate_sets(exercise):
    return list(chain(*[repeat(block, block.count) for block in exercise.blocks]))

def calculate_weight(ratio, weight):
    val = ratio * weight
    return round(val / 5) * 5

def render_ratio_set(item, weight):
    return RATIO_SET_TEMPLATE.format(
        ratio=round(item.ratio * 100),
        reps=item.reps,
        weight=calculate_weight(item.ratio, weight),
    )

def render_simple_set(item):
    return SIMPLE_SET_TEMPLATE.format(reps=item.reps)

def render_exercise(name, render_set, sets):
    items = map(render_set, sets[:MAX_COLUMNS])
    stub_items = [STUB_SET] * max(MAX_COLUMNS - len(sets), 0)
    return EXERCISE_TEMPLATE.format(name=name, sets=''.join(chain(items, stub_items)))

def render_day(day, weights):
    exercises = []
    for exercise in day.exercises:
        render_set = select_set_renderer(exercise, weights)
        sets = generate_sets(exercise)
        exercises.append(render_exercise(exercise.name, render_set, sets))
        if len(sets) > MAX_COLUMNS:
            exercises.append(render_exercise('', render_set, sets[MAX_COLUMNS:]))
    return DAY_TEMPLATE.format(title=day.title, exercises='\n'.join(exercises))

def render(plan):
    weights = [WEIGHT_TEMPLATE.format(target=weight) for weight in plan.weights]
    days = [render_day(day, plan.weights) for day in plan.days]
    page = PAGE_TEMPLATE.format(
        title=plan.title,
        weights='\n'.join(weights),
        days='\n'.join(days),
    )
    return page
