import unittest

def run_the_suite():
    # Automatically locate and load all tests matching 'test_*.py' inside the 'tests' folder
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='UnitTests', pattern='test_*.py')
    
    # Run the compiled test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_the_suite()