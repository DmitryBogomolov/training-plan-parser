[![CircleCI](https://circleci.com/gh/DmitryBogomolov/training-plan-parser.svg?style=svg)](https://circleci.com/gh/DmitryBogomolov/training-plan-parser)

# Training Plan Parser

Parses training plan in text format (like in [sample](./sample.txt)) and outputs html page.

## In terminal

- Pass *path/to/plan.txt* as command line argument; *path/to/plan.html* is created.
  ```bash
  ./run path/to/plan.txt
  ```

- Pass plan as *stdin*.
  ```bash
  cat path/to/plan.txt | ./run - > path/to/plan.html
  ```
  or
  ```bash
  ./run - < path/to/plan.txt > path/to/plan.html
  ```

## In code

- Pass *path/to/plan.txt*.
  ```python
  from trpp import process_file
  
  process_file('path/to/plan.txt')
  ```

- Manage buffers manually.
  ```python
  from trpp import process

  with open('path/to/plan.txt', mode='rb') as input_buffer:
      with open('path/to/plan.html', mode='wb') as output_buffer:
          process(input_buffer, output_buffer)
  ```

## Format

See [sample](./sample.txt).
