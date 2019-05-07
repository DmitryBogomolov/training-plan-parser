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
Ex: 3-1 5x5

'''

def rat(ratio, reps):
    return [{'ratio': ratio, 'reps': reps}]

def sim(reps):
    return [{'reps': reps}]

class TextParserTests(unittest.TestCase):
    def test_parse(self):
        data = text_parser.parse(SAMPLE)

        days = data['days']
        del data['days']
        self.assertEqual(data, {
            'title': 'Title\n(title notes)',
            'weights': {
                'Ex: 1-1': 10,
                'Ex: 2-1': 20,
                'Ex: 1-2': 30,
            },
        }, 'title and weights')
        self.assertEqual(len(days), 3, 'days')

        day = days[0]
        self.assertEqual(day['title'], ' * Day 1', 'day 1 title')
        exercises = day['exercises']
        self.assertEqual(len(exercises), 2, 'day 1 exercises')
        self.assertEqual(exercises[0], {
            'name': 'Ex: 1-1',
            'sets': rat(0.5, 5) + rat(0.6, 4) * 2 + rat(0.7, 3) * 2 + rat(0.75, 3) * 5,
        })
        self.assertEqual(exercises[1], {
            'name': 'Ex: 1-2',
            'sets': rat(0.5, 5) + rat(0.6, 5) * 2 + rat(0.7, 5) * 5,
        })

        day = days[1]
        self.assertEqual(day['title'], ' * Day 2', 'day 2 title')
        exercises = day['exercises']
        self.assertEqual(len(exercises), 2, 'day 2 exercises')
        self.assertEqual(exercises[0], {
            'name': 'Ex: 2-1',
            'sets': rat(0.5, 6) + rat(0.6, 6) * 2 + rat(0.65, 6) * 4,
        })
        self.assertEqual(exercises[1], {
            'name': 'Ex: 2-2',
            'sets': sim(10) * 5,
        })

        day = days[2]
        self.assertEqual(day['title'], ' * Day 3', 'day 3 title')
        exercises = day['exercises']
        self.assertEqual(len(exercises), 1, 'day 1 exercises')
        self.assertEqual(exercises[0], {
            'name': 'Ex: 3-1',
            'sets': sim(5) * 5,
        })
