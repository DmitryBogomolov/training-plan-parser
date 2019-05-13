import unittest
from ..plan_renderer import render
from ..objects import Plan, WeightInfo, Day, Exercise, RatioSetBlock, SimpleSetBlock

class PlanRendererTests(unittest.TestCase):
    def test_render_title(self):
        plan = Plan('Test Title', [], [])
        page = render(plan)

        self.assertIn('<td class="title" colspan="11">Test Title</td>', page)

    def test_render_weights(self):
        plan = Plan('Title', [
            WeightInfo('Ex 1', 10),
            WeightInfo('Ex 2', 20),
        ], [])
        page = render(plan)

        self.assertIn('<td class="set">Ex 1</td><td class="set">10</td>', page)
        self.assertIn('<td class="set">Ex 2</td><td class="set">20</td>', page)

    def test_render_day_title(self):
        plan = Plan('Title', [], [
            Day('Day 1', []),
            Day('Day 2', []),
        ])
        page = render(plan)

        self.assertEqual(page.count('<tr><td colspan="11">&nbsp;</td></tr>'), 2)
        self.assertIn('<tr><td class="day" colspan="11">Day 1</td></tr>', page)
        self.assertIn('<tr><td class="day" colspan="11">Day 2</td></tr>', page)

    def test_render_simple_exercises(self):
        plan = Plan('Title', [], [
            Day('Day', [
                Exercise('Ex 1', [
                    SimpleSetBlock(4, 3),
                    SimpleSetBlock(3, 2),
                ]),
            ])
        ])
        page = render(plan)

        rows = '<td class="set">4</td>' * 3 + '<td class="set">3</td>' * 2 + '<td></td>' * 5
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)

    def test_render_multiline_exercises(self):
        plan = Plan('Title', [], [
            Day('Day', [
                Exercise('Ex 1', [
                    SimpleSetBlock(5, 8),
                    SimpleSetBlock(4, 5),
                ]),
            ])
        ])
        page = render(plan)

        rows = '<td class="set">5</td>' * 8 + '<td class="set">4</td>' * 2
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)
        rows = '<td class="set">4</td>' * 3 + '<td></td>' * 7
        self.assertIn('<tr><td class="exercise"></td>' + rows + '</tr>', page)

    def test_render_ratio_exercises(self):
        plan = Plan('Title', [WeightInfo('Ex 1', 80)], [
            Day('Day', [
                Exercise('Ex 1', [
                    RatioSetBlock(0.4, 4, 3),
                    RatioSetBlock(0.5, 3, 2),
                ]),
            ])
        ])
        page = render(plan)

        rows = '<td class="set">40% 4 / 30</td>' * 3 + '<td class="set">50% 3 / 40</td>' * 2 + '<td></td>' * 5
        self.assertIn('<tr><td class="exercise">Ex 1</td>' + rows + '</tr>', page)
