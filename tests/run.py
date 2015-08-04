import unittest

loader = unittest.TestLoader()
suite = loader.discover('./tests')
runner = unittest.TextTestRunner(descriptions=True, verbosity=2)

if __name__ == '__main__':
    result = runner.run(suite)
