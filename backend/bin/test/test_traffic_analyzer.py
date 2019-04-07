import unittest

from io import StringIO

from unittest.mock import patch

import main.traffic_analyzer as traffic_analyzer


class TestTrafficAnalyzerMethods(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", "test")
    def test_main_function(self, mock_stdout):
        error_text = "Please use (convert|enrich|run)\n"
        traffic_analyzer.main()
        self.assertEqual(mock_stdout.getvalue(), error_text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrafficAnalyzerMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
