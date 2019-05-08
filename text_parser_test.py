import unittest
import text_parser

SAMPLE = '''
Title
(title notes)

Ex: 1-1 10
Ex: 2-1 20
Ex: 1-2 30


 * Day 1
Ex: 1-1 50% 5x1, 60% 4x2, 70% 3x2, 75% 3x5
Ex: 1-2 50% 5x1, 60% 5x2, 70% 5x5

 * Day 2
Ex: 2-1 50% 6x1, 60% 6x2, 65% 6x4
Ex: 2-2 10x5

 * Day 3
Ex: 3-1 5x5 3x2

'''

def rat(ratio, reps, count):
    return text_parser.RatioSetBlock(ratio, reps, count)

def sim(reps, count):
    return text_parser.SimpleSetBlock(reps, count)

class TextParserTests(unittest.TestCase):
    def test_parse(self):
        plan = text_parser.parse(SAMPLE)

        self.assertEqual(plan.title, 'Title\n(title notes)', 'title')
        self.assertEqual(plan.weights, [
            text_parser.WeightInfo('Ex: 1-1', 10),
            text_parser.WeightInfo('Ex: 2-1', 20),
            text_parser.WeightInfo('Ex: 1-2', 30),
        ])
        self.assertEqual(len(plan.days), 3, 'days')

        day = plan.days[0]
        self.assertEqual(day.title, ' * Day 1', 'day 1 title')
        exercises = day.exercises
        self.assertEqual(len(exercises), 2, 'day 1 exercises')
        self.assertEqual(exercises[0], text_parser.Exercise(
            'Ex: 1-1',
            [rat(0.5, 5, 1), rat(0.6, 4, 2), rat(0.7, 3, 2), rat(0.75, 3, 5)],
        ))
        self.assertEqual(exercises[1], text_parser.Exercise(
            'Ex: 1-2',
            [rat(0.5, 5, 1), rat(0.6, 5, 2), rat(0.7, 5, 5)],
        ))

        day = plan.days[1]
        self.assertEqual(day.title, ' * Day 2', 'day 2 title')
        exercises = day.exercises
        self.assertEqual(len(exercises), 2, 'day 2 exercises')
        self.assertEqual(exercises[0], text_parser.Exercise(
            'Ex: 2-1',
            [rat(0.5, 6, 1), rat(0.6, 6, 2), rat(0.65, 6, 4)],
        ))
        self.assertEqual(exercises[1], text_parser.Exercise(
            'Ex: 2-2',
            [sim(10, 5)],
        ))

        day = plan.days[2]
        self.assertEqual(day.title, ' * Day 3', 'day 3 title')
        exercises = day.exercises
        self.assertEqual(len(exercises), 1, 'day 1 exercises')
        self.assertEqual(exercises[0], text_parser.Exercise(
            'Ex: 3-1',
            [sim(5, 5), sim(3, 2)],
        ))
