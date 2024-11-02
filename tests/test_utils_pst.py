from py_string_tool.utils_pst import *
import pytest

def test_replace():
    # Test case 1: Basic replacement
    assert replace("Hello world", ["world"], "Python") == "Hello Python"
    
    # Test case 2: Multiple replacements
    assert replace("Hello world", ["Hello", "world"], "Python") == "Python Python"
    
    # Test case 3: No replacement needed
    assert replace("Hello world", ["Python"], "Java") == "Hello world"
    
    # Test case 4: Empty string replacement
    assert replace("Hello world", ["world"], "") == "Hello "
    
    # Test case 5: Replace with longer string
    assert replace("Hi", ["Hi"], "Hello") == "Hello"
    
    # Test case 6: Replace newline character
    assert replace("Hello\nworld", ["\n"], " ") == "Hello world"
    
    # Test case 7: Replace multiple newline characters
    assert replace("Hello\nworld\n!", ["\n"], " ") == "Hello world !"
    
    # Test case 8: Replace with newline character
    assert replace("Hello world", [" "], "\n") == "Hello\nworld"

# You can run this test function using pytest
if __name__ == "__main__":
    pytest.main([__file__])
