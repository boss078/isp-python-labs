import unittest
import sys
from pathlib import Path
import json_serializer as json_s

global_a = 15

class TestJsonSerializer(unittest.TestCase):

  SIMPLE_OBJECTS = [
    {
      23: True,
      'hello': 21,
      45.6: 'something',
      False: 23.1,
    },
    [
      23,
      42.4,
      True,
      'list_component',
    ]
  ]
  SIMPLE_JSONS = [
    '{ "23": true, "hello": 21, "45.6": "something", "false": 23.1 }',
    '[ 23, 42.4, true, "list_component" ]'
  ]

  COMPLEX_OBJECTS = [
    {
      'test': 0.32,
      12: 1,
      False: ['hello', True, 156],
      13.37: {
          'this': 'is',
          'something': 'here',
          'this is': 'my sentence'
      }
    }
  ]
  COMPLEX_JSONS = [
    '{ "test": 0.32, "12": 1, "false": [ "hello", true, 156 ], "13.37": { "this": "is", "something": "here", "this is": "my sentence" } }'
  ]

  class SimpleClass:
    hello = 'Hi'
    goodbye = 'Bye'
    local_b = 10

    def __init__(self, arg_one, arg_two):
      print(f'In init. arg_one: {arg_one}, arg_two: {arg_two}')

    def class_func(self):
      return { 'global_a': global_a, 'local_b': self.local_b }

  def simple_func(arg):
    return f'my arg is {arg}'

  SUPER_COMPLEX_OBJECTS = {
    'my_function': simple_func,
    'my_class': SimpleClass,
    'lambda': lambda b : b + 10
  }

  # SUPER_COMPLEX_JSON = '''{ "my_function": { "__type__": "function", "code": "def simple_i_o_func(arg):\n    print('Perform input')\n    inp = input()\n    print(f'Input: {inp}, arg: {arg}')", "name": "simple_i_o_func", "args": [ "arg" ], "globals": { "a": 5 } }, "my_class": { "__type__": "class", "name": "SimpleClass", "members": { "hello": "Hi", "goodbye": "Bye", "__init__": { "__type__": "function", "code": "def __init__(self, arg_one, arg_two):\n        print(f'In init. arg_one: {arg_one}, arg_two: {arg_two}')", "name": "__init__", "args": [ "self", "arg_one", "arg_two" ], "globals": { "a": 5 } }, "class_func": { "__type__": "function", "code": "def class_func(self):\n      print(f'class_func. global var: {a}')", "name": "class_func", "args": [ "self" ], "globals": { "a": 5 } } } }, "lambda": { "__type__": "function", "code": "lambda b : b + 10", "name": "<lambda>", "args": [ "b" ], "globals": { "a": 5 } } }'''



  def test_simple_objects(self):
    json_ser = json_s.JsonSerializer(True)
    for idx in range(len(self.SIMPLE_JSONS)):
      serialized = json_ser.dumps(self.SIMPLE_OBJECTS[idx])
      decerialized = json_ser.loads(self.SIMPLE_JSONS[idx])

      self.assertEqual(serialized, self.SIMPLE_JSONS[idx])
      self.assertEqual(decerialized, self.SIMPLE_OBJECTS[idx])
  
  def test_complex_objects(self):
    json_ser = json_s.JsonSerializer(True)
    for idx in range(len(self.COMPLEX_JSONS)):
      serialized = json_ser.dumps(self.COMPLEX_OBJECTS[idx])
      decerialized = json_ser.loads(self.COMPLEX_JSONS[idx])

      self.assertEqual(serialized, self.COMPLEX_JSONS[idx])
      self.assertEqual(decerialized, self.COMPLEX_OBJECTS[idx])

  def test_classes_funcs_lambdas(self):
    json_ser = json_s.JsonSerializer(True)
    serialized = json_ser.dumps(self.SUPER_COMPLEX_OBJECTS)
    decerialized = json_ser.loads(serialized)

    class_inst = decerialized['my_class']('arg_one', 'arg_two')
    self.assertEqual(class_inst.hello, 'Hi')
    self.assertEqual(class_inst.goodbye, 'Bye')
    self.assertEqual(class_inst.class_func(), { 'global_a': 15, 'local_b': 10 })
    self.assertEqual(decerialized['my_function']('the arg'), 'my arg is the arg')
    self.assertEqual(decerialized['lambda'](5), 15)


  # def test_super_complex(self):
  #   self.maxDiff = None
  #   json_ser = json_s.JsonSerializer(True)

  #   serialized = json_ser.dumps(self.SUPER_COMPLEX_OBJECTS)

  #   self.assertEqual(serialized, self.SUPER_COMPLEX_JSON)

if __name__ == '__main__':
  unittest.main()
