# import global_vars
import re
import inspect
from dill.source import getsource
from types import FunctionType
import sys
import types
class JsonSerializer:
  _convert_complex = False
  _sended_globals = {}

  def __init__(self, conv_complex):
    # global_vars.init(sended_globals)
    self._convert_complex = conv_complex

  def dumps(self, obj) -> str:
    if self._convert_complex:
      obj = self._complex_to_simple(obj)
    result = ''
    if type(obj) is list:
      result += '[ '
      for i in range(len(obj)):
        if i != 0: result += ', ' 
        result += self.dumps(obj[i])
      result += ' ]'
    elif type(obj) is dict:
      result += '{ '
      for key in obj.keys():
        if list(obj.keys())[0] != key: result += ', ' 
        dumped_key = self.dumps(key)
        if dumped_key[0] != '"' and dumped_key[-1] != '"':
          dumped_key = '"' + dumped_key  + '"'
        result += dumped_key
        result += ': '
        result += self.dumps(obj[key])
      result += ' }'
    elif type(obj) is str:
      result += f"\"{obj}\""
    elif type(obj) is bool:
      result += 'true' if obj else 'false'
    elif (type(obj) is float) or (type(obj) is int):
      result += str(obj)
    else:
      result += str(obj)
    return result
  
  def loads(self, s):
    raw_data = self._splitted_str(s)
    # print(raw_data)
    # print(len(raw_data))
    obj = self._parse_string_to_obj(raw_data, 0)['result']
    return obj
  
  def dump(self, obj, fp):
    serialized = self.dumps(obj)
    output_file = open(fp, 'w')
    output_file.write(serialized)
    output_file.close()
  
  def load(self, fp):
    input_file = open(fp, 'r')
    input_s = input_file.read()
    input_file.close()
    return self.loads(input_s)


  def _complex_to_simple(self, obj):
    result = obj
    if inspect.isclass(obj):
      # result = { '__type__': 'class' }
      # print('Class')
      result = { '__type__': 'class'}
      result['name'] = obj.__name__
      allowed_keys = [ '__init__' ]
      result['members'] = dict(
        (key, value)
          for (key, value) in obj.__dict__.items()
            if not key.startswith('__') or key in allowed_keys
        )
      # print(result)
    elif callable(obj):
      # print('Function')
      result = { '__type__': 'function' }
      code = getsource(obj).strip()
      if 'lambda ' in code:
        code = code[code.find('lambda '):]
      result['code'] = code
      result['globals'] = {}
      excluded_keys = [ 'global_vars' ]
      for key, value in list(obj.__globals__.items()):
        if key.startswith('global') and not key in excluded_keys:
          result['globals'][key] = value
      # print(f'Globals for {obj.__name__} function: {result["globals"]}')
      # transformed_code = {}
      # print(obj.__code__.co_consts)
      # print(dir(obj.__code__))
      # for key in dir(obj.__code__):
      #   if key.startswith('co'):
      #     attr = getattr(obj.__code__, key)
      #     transformed_code[key] = attr() if callable(attr) else attr
      # print(transformed_code)
      # result['code'] = transformed_code
      result['name'] = obj.__name__
      result['args'] = inspect.getargspec(obj).args
      # result['globals'] = {}
      # excluded_keys = ['init']
      # for key, value in list(global_vars.init.__globals__.items()):
      #   if not key.startswith('__') and key not in excluded_keys:
      #     result['globals'][key] = value
    return result

  def _simple_to_complex(self, obj):
    if type(obj) is dict and '__type__' in obj.keys():
      if obj['__type__'] == 'function':
        # compiled_code = compile(obj['code'], 'string', 'exec')
        # print(obj['code'])
        # print(obj['code'])
        # compiled_code = types.CodeType(
        #   obj['code']['co_argcount'],
        #   obj['code']['co_kwonlyargcount'],
        #   obj['code']['co_nlocals'],
        #   obj['code']['co_stacksize'],
        #   obj['code']['co_flags'],
        #   obj['code']['co_code'],
        #   obj['code']['co_consts'],
        #   obj['code']['co_names'],
        #   obj['code']['co_varnames'],
        #   obj['code']['co_name'],
        #   obj['code']['co_firstlineno'],
        #   obj['code']['co_lnotab'],
        #   obj['code']['co_freevars'],
        #   obj['code']['co_cellvars']
        # )
        # new_func = FunctionType(compiled_code, obj['globals'], obj['name'])
        if 'lambda ' in obj['code']:
          obj['code'] = 'new_lambda = ' + obj['code']
        result = {}
        exec(obj['code'], obj['globals'], result)
        # print(result)
        func_name = 'new_lambda' if 'lambda ' in obj['code'] else obj['name']
        new_func = result[func_name]
        # print(func_name)
        # print(new_func)
        return new_func
        # exec(obj['code'], obj['globals'], result)
        # return result[obj['name']]
      elif obj['__type__'] == 'class':
        new_class = type(obj['name'], (object, ), obj['members'])
        return new_class
    return obj

  def _splitted_str(self, input):
    processed_data = []
    splitted_str = re.split(r"\"", input)
    for i in range(len(splitted_str)):
      if i % 2 == 1:
        processed_data.append('"' + splitted_str[i] + '"')
      else:
        escaped_from_funcs = re.split(r"[<>]", splitted_str[i])
        for j in range(len(escaped_from_funcs)):
          if j % 2 == 1:
            processed_data.append('<' + escaped_from_funcs[j] + '>')
          else:
            arr = re.split(r"[\s,]", escaped_from_funcs[j])
            for elem in arr:
              if elem:
                if elem[-1] == ':' and len(elem) > 1:
                  processed_data.append(elem[0:-1])
                  processed_data.append(elem[-1])
                else:
                  processed_data.append(elem)
    return processed_data

  def _parse_string_to_obj(self, raw_data, i):
    result = { 'result': None, 'i': i + 1 }
    if re.match(r'\d', raw_data[i].strip('"')[0]):
      result['result'] = int(raw_data[i].strip('"')) if raw_data[i].find('.') == -1 else float(raw_data[i].strip('"'))
      result['i'] = i + 1
    elif re.match(r'true|false', raw_data[i].strip('"')):
      raw_data[i].strip('"')
      result['result'] = raw_data[i] == 'true'
      result['i'] = i + 1
    elif raw_data[i][0] == '"':
      result['result'] = raw_data[i][1:(len(raw_data[i])-1)]
      result['i'] = i + 1
    elif raw_data[i][0] == '[':
      result_arr = []
      i += 1
      while i < len(raw_data):
        if raw_data[i] == ']':
          i += 1 
          break
        return_dict = self._parse_string_to_obj(raw_data, i)
        result_arr.append(return_dict['result'])
        i = return_dict['i']
      result['result'] = result_arr
      result['i'] = i
    elif raw_data[i][0] == '{':
      result_dict = {}
      i += 1
      while i < len(raw_data):
        if raw_data[i] == '}':
          i += 1
          break

        return_dict = self._parse_string_to_obj(raw_data, i)
        key = return_dict['result']
        i = return_dict['i']

        if raw_data[i] != ':': pass # raise exeption
        i += 1

        return_dict = self._parse_string_to_obj(raw_data, i)
        value = return_dict['result']
        i = return_dict['i']

        result_dict[key] = value
      if self._convert_complex:
        result_dict = self._simple_to_complex(result_dict)
      result['result'] = result_dict
      result['i'] = i
    
    return result

  # def _detect_funcs(self, obj)  
