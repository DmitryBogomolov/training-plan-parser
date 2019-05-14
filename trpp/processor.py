from io import TextIOWrapper
from os import path
from .text_parser import parse
from .plan_renderer import render

def process(input_buffer, output_buffer):
    input_wrapper = TextIOWrapper(input_buffer, encoding='UTF8')
    output_wrapper = TextIOWrapper(output_buffer, encoding='UTF8')
    content = input_wrapper.read()
    plan = parse(content)
    page = render(plan)
    output_wrapper.write(page)

def process_file(file_name):
    name, _ = path.splitext(path.basename(file_name))
    output_name = path.join(path.dirname(file_name), name + '.html')
    with open(file_name, mode='rb') as input_buffer:
        with open(output_name, mode='wb') as output_buffer:
            process(input_buffer, output_buffer)
