'''
Renders an instance of Plan class to a string in html format.

- render
'''

from functools import partial
from itertools import repeat, chain
from .objects import RatioSetBlock, SimpleSetBlock

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
    '''Renders *plan* to a string.'''
    weights = [WEIGHT_TEMPLATE.format(target=weight) for weight in plan.weights]
    days = [render_day(day, plan.weights) for day in plan.days]
    page = PAGE_TEMPLATE.format(
        title=plan.title,
        weights='\n'.join(weights),
        days='\n'.join(days),
    )
    return page
