import unittest
from hw3 import *
class TestParser(unittest.TestCase):
    
    def test_parse_array(self):
        line = "myArray = (1, 2, 3)"
        expected = "myArray = [1, 2, 3]"
        result = parse_array(line)
        self.assertEqual(result, expected)

    def test_parse_dictionary(self):
        line = 'myDict = {Key: "value1", Keyy: "value2"}'
        expected = 'myDict = { Key = "value1", Keyy = "value2" }'
        result = parse_dictionary(line)
        self.assertEqual(result, expected)

    def test_parse_constant_declaration(self):
        line = "MY_CONSTANT -> 42"
        expected_name = "MY_CONSTANT"
        expected_value = "42"
        result_name, result_value = parse_constant_declaration(line)
        self.assertEqual(result_name, expected_name)
        self.assertEqual(result_value, expected_value)

    def test_parse_constant_evaluation(self):
        constants = {"MY_CONSTANT": "42"}
        line = "result = $MY_CONSTANT$"
        expected = "result = 42"
        result = parse_constant_evaluation(line, constants)
        self.assertEqual(result, expected)

    def test_convert_to_toml(self):
        input_data = """\
<#
This is a comment
#>
myArray = (1, 2, 3, 4)
myDict = {key1: "value1", key2: "value2"}
MY_CONSTANT -> 42
result = $MY_CONSTANT$
"""
        # Создаем временный файл для тестирования
        with open('test_input.txt', 'w', encoding='utf-8') as f:
            f.write(input_data)

        expected_output = """\
myArray = [1, 2, 3, 4]
myDict = { key1 = "value1", key2 = "value2" }
MY_CONSTANT = 42
result = 42
"""
        
        result_output = convert_to_toml('test_input.txt')
        
        self.assertEqual(result_output.strip(), expected_output.strip())



if __name__ == '__main__':
    unittest.main()
