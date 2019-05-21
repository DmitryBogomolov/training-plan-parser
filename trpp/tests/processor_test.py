import unittest
from unittest import mock   # pylint: disable=no-name-in-module
from importlib import import_module, reload # pylint: disable=no-name-in-module, redefined-builtin
import sys
import os
import io

processor = import_module('trpp.processor') # pylint: disable=invalid-name

mock_text_parser = mock.Mock()      # pylint: disable=invalid-name
mock_plan_renderer = mock.Mock()    # pylint: disable=invalid-name
mock_text_parser.parse = mock.Mock()
mock_plan_renderer.render = mock.Mock()

class ProcessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.modules['trpp.text_parser'] = mock_text_parser
        sys.modules['trpp.plan_renderer'] = mock_plan_renderer
        reload(processor)

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop('trpp.text_parser')
        sys.modules.pop('trpp.plan_renderer')
        reload(processor)

    def setUp(self):
        mock_text_parser.parse.return_value = None
        mock_plan_renderer.render.return_value = None

    def tearDown(self):
        mock_text_parser.parse.reset_mock()
        mock_plan_renderer.render.reset_mock()

    def test_process(self):
        in_stream = io.StringIO('text-plan')
        out_stream = io.TextIOWrapper(io.BytesIO())
        mock_plan = object()
        mock_text_parser.parse.return_value = mock_plan
        mock_plan_renderer.render.return_value = 'html-plan'

        processor.process(in_stream, out_stream)

        out_stream.seek(0)
        self.assertEqual(out_stream.read(), 'html-plan')
        self.assertEqual(mock_text_parser.parse.call_args_list, [
            mock.call('text-plan'),
        ])
        self.assertEqual(mock_plan_renderer.render.call_args_list, [
            mock.call(mock_plan),
        ])

    def test_process_file(self):
        try:
            with open('test-file.txt', mode='w') as in_stream:
                in_stream.write('text-plan')
            mock_plan = object()
            mock_text_parser.parse.return_value = mock_plan
            mock_plan_renderer.render.return_value = 'html-plan'

            processor.process_file('test-file.txt')

            with open('test-file.html', mode='r') as out_stream:
                content = out_stream.read()
            self.assertEqual(content, 'html-plan')
            self.assertEqual(mock_text_parser.parse.call_args_list, [
                mock.call('text-plan'),
            ])
            self.assertEqual(mock_plan_renderer.render.call_args_list, [
                mock.call(mock_plan),
            ])

        finally:
            if os.path.exists('test-file.txt'):
                os.remove('test-file.txt')
            if os.path.exists('test-file.html'):
                os.remove('test-file.html')
