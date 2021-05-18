import global_vars
from json_serializer import JsonSerializer

global_a = 10

class SimpleClass:
    hello = 'Hi'
    goodbye = 'Bye'

    def __init__(self, arg_one, arg_two):
        print(f'In init. arg_one: {arg_one}, arg_two: {arg_two}')

    def class_func(self):
        print(f'class_func. global var: {global_a}')

def simple_i_o_func(arg):
    print('Perform input')
    inp = input()
    print(f'Input: {inp}, arg: {arg}')

def closure_func(something):
    print(f'In closure func. arg : {something}')
    def inner(another):
        print(f'In inner. arg: {something}')
    return inner

test_object = {
    # 'test': 0.32,
    # 12: 1,
    # False: ['hello', True, 156],
    # 13.37: {
    #     'this': 'is',
    #     'something': 'here',
    #     'this is': 'my sentence'
    # }
    'my_function': simple_i_o_func,
    'my_class': SimpleClass,
    'lambda': lambda b : b + 10
}

simple_obj = [
      23,
      42.4,
      True,
      'list_component',
    ]

test_simple_hash = {
    'testOne': 1,
    'testTwo': 2.1,
    'testThree': 3
}

def perform_test(obj):
    json_ser = JsonSerializer(True)
    print('Input obj:')
    print(obj)
    serialized = json_ser.dumps(obj)
    print('Serialized output:')
    print(serialized)
    decerialized = json_ser.loads(serialized)
    print('Deserialized output:')
    print(decerialized)

    return decerialized

test_object['my_class']('arg_one', 'arg_two').class_func()
decerialized = perform_test(test_object)
test_object['my_class']('arg_one', 'arg_two').class_func()
# decerialized['my_function']('argument')
# print(decerialized['lambda'](20))
# decerialized['my_class']('arg_one', 'arg_two').class_func()
# class_inst = decerialized['my_class']('argone', 'argtwo')
# print(class_inst.hello)
# print(class_inst.goodbye)
# class_inst.pisjun()
# print(decerialized['my_function'])
# decerialized['my_function']('argument')
# simple_i_o_func(56)