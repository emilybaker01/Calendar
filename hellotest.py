import hello
import unittest

class HelloTest(unittest.TestCase):
    def test_read_record_for_day_ten_oclock(self):
        rows = hello.read_record_for_day('10.00')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], '08.07.25')
        self.assertEqual(rows[0][1], '10.00')

if __name__ == '__main__':
    unittest.main()

class HelloTest2(unittest.TestCase):
    def test_read_record_for_person_Mel(self):
        rows=hello.read_record_for_person('Mel Davis')
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0][0],'08.07.25')
        self.assertEqual(rows[0][1], '10.00')

class HelloTest3(unittest.TestCase):
    def test_read_record_for_date_wednesday(self):
        rows=hello.read_record_for_date(['09.07.25'])
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0][1],'10.00')
        self.assertEqual(rows[0][3], 'Adam Robertson')