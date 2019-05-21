'''
Functions that combine parse and render stages.

- process
- process_file
'''

from os import path
from .text_parser import parse
from .plan_renderer import render

def process(in_stream, out_stream):
    '''Reads from *in_stream*, processes, writes to *out_stream*.'''
    content = in_stream.read()
    plan = parse(content)
    page = render(plan)
    out_stream.write(page)

def process_file(file_name):
    '''Read *file_name*, processes, writes to *basename(file_name).html*.'''
    name, _ = path.splitext(path.basename(file_name))
    output_name = path.join(path.dirname(file_name), name + '.html')
    with open(file_name, mode='r') as in_stream, open(output_name, mode='w') as out_stream:
        process(in_stream, out_stream)
