import random
import unittest
import filters as f

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.text = "Ooooh myyy gooooooood, @username!!!! :D :) This is #amazing: http://someurl.com/fdhsiufds?dsads=dsa"

    def test_no_emoticons(self):
        tmp = f.no_emoticons(self.text)
        self.assertEqual(tmp, 'Ooooh myyy gooooooood, @username!!!!   This is #amazing: http://someurl.com/fdhsiufds?dsads=dsa'.lower())

    def test_no_usernames(self):
        tmp = f.no_usernames(self.text)
        self.assertEqual(tmp, 'Ooooh myyy gooooooood, !!!! :D :) This is #amazing: http://someurl.com/fdhsiufds?dsads=dsa'.lower())

    def test_username_placeholder(self):
        tmp = f.username_placeholder(self.text)
        self.assertEqual(tmp, 'Ooooh myyy gooooooood, ||U||!!!! :D :) This is #amazing: http://someurl.com/fdhsiufds?dsads=dsa'.lower())

    def test_no_hash(self):
        tmp = f.no_hash(self.text)
        self.assertEqual(tmp, "Ooooh myyy gooooooood, @username!!!! :D :) This is : http://someurl.com/fdhsiufds?dsads=dsa".lower())

    def test_hash_placeholder(self):
        tmp = f.hash_placeholder(self.text)
        self.assertEqual(tmp, "Ooooh myyy gooooooood, @username!!!! :D :) This is ||H||: http://someurl.com/fdhsiufds?dsads=dsa".lower())

    def test_no_rt_tag(self):
        text = "RT " + self.text
        tmp = f.no_rt_tag(text)
        self.assertEqual(tmp, self.text.lower())

    def test_no_url(self):
        tmp = f.no_url(self.text)
        self.assertEqual(tmp, "Ooooh myyy gooooooood, @username!!!! :D :) This is #amazing:".lower())

    def test_url_placeholder(self):
        tmp = f.url_placeholder(self.text)
        self.assertEqual(tmp, "Ooooh myyy gooooooood, @username!!!! :D :) This is #amazing: ||URL||".lower())

    def test_reduce_letter_duplicates(self):
        tmp = f.reduce_letter_duplicates(self.text)
        self.assertEqual(tmp, "Oooh myyy goood, @username!!! :D :) This is #amazing: http://someurl.com/fdhsiufds?dsads=dsa".lower())

        t1 = f.reduce_letter_duplicates('My gooooooooooooooooooooood')
        self.assertEqual(t1, 'My goood'.lower())
if __name__ == '__main__':
    unittest.main()