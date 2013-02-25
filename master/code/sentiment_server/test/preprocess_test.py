import random
import unittest
import preprocess as p

class TestSequenceFunctions(unittest.TestCase):

    def test_negation_attachment(self):
        t1 = p.negation_attachment("This is not perfect at all!")
        t2 = p.negation_attachment("I am not!!")
        t3 = p.negation_attachment("I'm not!!")
        t4 = p.negation_attachment("I am not short")
        
        self.assertEqual(t1, "This is-not not-perfect at all!")
        self.assertEqual(t2, "I am-not!!")
        self.assertEqual(t3, "I'm-not!!")
        self.assertEqual(t4, "I am-not not-short")

    def test_remove_stopwords(self):
        t1 = "There is not way in hell I'm gonna wait till 1am for transfer news. :)"
        t2 = "I had a very vivid dream that I was pregnant last night, (like, scary real) and today I've felt off. And something still doesn't feel right."

        self.assertEqual(p.remove_stopwords("not", ["not"]), "not")

        # Add more tests.

if __name__ == '__main__':
    unittest.main()