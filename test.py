# test.py
from bashplotlib.scatterplot import build_scatter
import difflib
import unittest
    
class SimpleTestCase(unittest.TestCase):
    # def setUp(self):
        # """Call before every test case."""
    # def tearDown(self):
        # """Call after every test case."""
    def testA(self):
        """Test case A. all test method names must begin with 'test.'"""
        expected_result = """+--------------------------+
|      My Test Graph       |
+--------------------------+
y: My Y Axis
+--------------------------+
|       |               x  |
|       |                  |
|       |                  |
|       |           x      |
|       |                  |
|       |                  |
|       |                  |
|       |                  |
| - - - o - - - - - x - - -|
|       |                  |
|       |                  |
| x     |                  |
+--------------------------+
                x: My X Axis
""" 
        x_coords = [-10,20,20,30]
        y_coords = [-10,0,20,30]
        width = 10
        char = 'x'
        color = 'default'
        title = 'My Test Graph'

        result = build_scatter(
            x_coords,
            y_coords,
            width,
            char,
            color,
            title, 
            None,
            xtitle="My X Axis",
            ytitle="My Y Axis")
        
        assert expected_result == result
        if expected_result != result:
            print("FAILURE!")
            print("Expected:")
            print(expected_result)
            print("Found:")
            print(result)
            for i,s in enumerate(difflib.ndiff(expected_result, result)):
                if s[0]==' ': continue
                elif s[0]=='-':
                    print(u'Delete "{}" from position {}'.format(s[-1],i))
                elif s[0]=='+':
                    print(u'Add "{}" to position {}'.format(s[-1],i))    
            print()
    
    def testB(self):
        """Test case B."""
        expected_result = """+--------------------------+
|      My Test Graph       |
+--------------------------+
y: My Y Axis
+--------------------------+
|       |               x  |
|       |                  |
|       |                  |
|       |           x      |
|       |                  |
|       |                  |
|       |                  |
|       |                  |
| - - - o - - - - - - - x -|
|       |                  |
|       |                  |
| x     |                  |
+--------------------------+
                x: My X Axis
""" 
        x_coords = [-10,30,20,30]
        y_coords = [-10,0,20,30]
        width = 10
        char = 'x'
        color = 'default'
        title = 'My Test Graph'

        result = build_scatter(
            x_coords,
            y_coords,
            width,
            char,
            color,
            title, 
            None,
            xtitle="My X Axis",
            ytitle="My Y Axis")
        
        assert expected_result == result
        if expected_result != result:
            print("FAILURE!")
            print("Expected:")
            print(expected_result)
            print("Found:")
            print(result)
            for i,s in enumerate(difflib.ndiff(expected_result, result)):
                if s[0]==' ': continue
                elif s[0]=='-':
                    print(u'Delete "{}" from position {}'.format(s[-1],i))
                elif s[0]=='+':
                    print(u'Add "{}" to position {}'.format(s[-1],i))    
            print()
    
    def testC(self):
        """Test case C."""
        expected_result = """+--------------------------+
|        The Title         |
+--------------------------+
y: Best Axis
+--------------------------+
|       |               x  |
|       |                  |
|       |                  |
|       |           x      |
|       |                  |
|       |                  |
|       |                  |
|       |                  |
| - - - o - - - - - - - x -|
|       |                  |
|       |                  |
| x     |                  |
+--------------------------+
               x: Worst Axis
""" 
        x_coords = [-10,30,20,30]
        y_coords = [-10,0,20,30]
        width = 10
        char = 'x'
        color = 'default'
        title = 'The Title'

        result = build_scatter(
            x_coords,
            y_coords,
            width,
            char,
            color,
            title, 
            None,
            xtitle="Worst Axis",
            ytitle="Best Axis")
        
        if expected_result != result:
            print("FAILURE!")
            print("Expected:")
            print(expected_result)
            print("Found:")
            print(result)
            for i,s in enumerate(difflib.ndiff(expected_result, result)):
                if s[0]==' ': continue
                elif s[0]=='-':
                    print(u'Delete "{}" from position {}'.format(s[-1],i))
                elif s[0]=='+':
                    print(u'Add "{}" to position {}'.format(s[-1],i))    
            print()
        assert expected_result == result
        

if __name__ == "__main__":
    unittest.main() # run all tests
