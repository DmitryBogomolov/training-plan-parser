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
Ex: 3-1 5x5 3x2 2x4

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
            [sim(5, 5), sim(3, 2), sim(2, 4)],
        ))

    def test_render_title(self):
        plan = text_parser.Plan('Test Title', [], [])
        page = text_parser.render(plan)

        self.assertIn('<td class="title" colspan="11">Test Title</td>', page)

    def test_render_weights(self):
        plan = text_parser.Plan('Title', [
            text_parser.WeightInfo('Ex 1', 10),
            text_parser.WeightInfo('Ex 2', 20),
        ], [])
        page = text_parser.render(plan)

        self.assertIn('<td class="set">Ex 1</td><td class="set">10</td>', page)
        self.assertIn('<td class="set">Ex 2</td><td class="set">20</td>', page)

    def test_render_day_title(self):
        plan = text_parser.Plan('Title', [], [
            text_parser.Day('Day 1', []),
            text_parser.Day('Day 2', []),
        ])
        page = text_parser.render(plan)

        self.assertEqual(page.count('<tr><td colspan="11">&nbsp;</td></tr>'), 2)
        self.assertIn('<tr><td class="day" colspan="11">Day 1</td></tr>', page)
        self.assertIn('<tr><td class="day" colspan="11">Day 2</td></tr>', page)

    def test_render_simple_exercises(self):
        plan = text_parser.Plan('Title', [], [
            text_parser.Day('Day', [
                text_parser.Exercise('Ex 1', [
                    text_parser.SimpleSetBlock(4, 3),
                    text_parser.SimpleSetBlock(3, 2),
                ]),
            ])
        ])
        page = text_parser.render(plan)

        rows = '<td class="set">4</td>' * 3 + '<td class="set">3</td>' * 2 + '<td></td>' * 5
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)

    def test_render_multiline_exercises(self):
        plan = text_parser.Plan('Title', [], [
            text_parser.Day('Day', [
                text_parser.Exercise('Ex 1', [
                    text_parser.SimpleSetBlock(5, 8),
                    text_parser.SimpleSetBlock(4, 5),
                ]),
            ])
        ])
        page = text_parser.render(plan)

        rows = '<td class="set">5</td>' * 8 + '<td class="set">4</td>' * 2
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)
        rows = '<td class="set">4</td>' * 3 + '<td></td>' * 7
        self.assertIn('<tr><td class="exercise"></td>' + rows + '</tr>', page)

    def test_render_ratio_exercises(self):
        plan = text_parser.Plan('Title', [text_parser.WeightInfo('Ex 1', 80)], [
            text_parser.Day('Day', [
                text_parser.Exercise('Ex 1', [
                    text_parser.RatioSetBlock(0.4, 4, 3),
                    text_parser.RatioSetBlock(0.5, 3, 2),
                ]),
            ])
        ])
        page = text_parser.render(plan)

        rows = '<td class="set">40% 4 / 30</td>' * 3 + '<td class="set">50% 3 / 40</td>' * 2 + '<td></td>' * 5
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)
