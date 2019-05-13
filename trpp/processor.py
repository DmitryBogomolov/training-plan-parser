from io import TextIOWrapper
from .text_parser import parse
from .plan_renderer import render

def process(input_buffer, output_buffer):
    input_wrapper = TextIOWrapper(input_buffer, encoding='UTF8')
    output_wrapper = TextIOWrapper(output_buffer, encoding='UTF8')
    content = input_wrapper.read()
    plan = parse(content)
    page = render(plan)
    output_wrapper.write(page)
