#from appengine_fixture_loader.loader import load_fixture

# TODO: We need a way to test it without relying on Google App Engine SDK being
# installed on this envidonment

import unittest

class SanityTest(unittest.TestCase):

    def testImportFailure(self):
        "This test will fail because Google's SDK is not present"

        def _dummy():
            from appengine_fixture_loader.loader import load_fixture

        self.assertRaises(ImportError, _dummy)

if __name__ == '__main__':
    unittest.main()
