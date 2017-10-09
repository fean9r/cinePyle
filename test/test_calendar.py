'''
Created on Sep 26, 2017

@author: fean9r
'''
from .context import cinepyle

import unittest


class TestGoogleCalendar(unittest.TestCase):
    """Basic test cases."""

    def test_my_class(self):
        c = cinepyle.calendars.GoogleCalendar()
        self.assertEqual(c.test(), True)
        

if __name__ == '__main__':
    unittest.main()