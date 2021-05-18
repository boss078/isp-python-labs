import global_vars
import yaml
import inspect


class YamlSerializer:
  _convert_complex = False

  def __init__(self, conv_complex):
    self._convert_complex = conv_complex
  
  def dumps(self, obj):
    obj = self._iterate_obj(obj, self._deconstruct_complex)
    return yaml.dump(obj)

  def loads(self, serialized):
    deserialized = yaml.load(serialized)
    return self._iterate_obj(deserialized, self._recreate_complex)

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
    

  def _iterate_obj(self, obj, func):
    result = func(obj)
    if type(obj) is list:
      result = []
      for elem in obj:
        result.append(self._iterate_obj(elem, func))
    elif type(obj) is dict:
      result = {}
      for key, value in obj.items():
        result[key] = self._iterate_obj(value, func)
    return result

  def _deconstruct_complex(self, obj):
    result = obj
    if not self._convert_complex:
      return result
    if inspect.isclass(obj):
      result = { '__type__': 'class'}
      result['name'] = obj.__name__
      allowed_keys = [ '__init__' ]
      result['members'] = dict(
        (key, value)
          for (key, value) in obj.__dict__.items()
            if not key.startswith('__') or key in allowed_keys
        )
    elif callable(obj):
      result = { '__type__': 'function' }
      print(obj)
      # compiled_code = compile(obj['code'], 'string', 'exec')
      # result['code'] = compiled_code.co_consts[0]
      result['code'] = inspect.getsource(obj).strip()
      result['name'] = obj.__name__
      result['args'] = inspect.getargspec(obj).args
      result['globals'] = {}
      excluded_keys = ['init']
      for key, value in list(global_vars.init.__globals__.items()):
        if not key.startswith('__') and key not in excluded_keys:
          result['globals'][key] = value
    return result

  def _recreate_complex(self, obj):
    if not self._convert_complex:
      return result
    if type(obj) is dict and '__type__' in obj.keys():
      if obj['__type__'] == 'function':
        compiled_code = compile(obj['code'], 'string', 'exec')
        # new_func = FunctionType(compiled_code.co_consts[0], obj['globals'], obj['name'])
        # print(obj['code'])
        new_func = FunctionType(compiled_code, obj['globals'], obj['name'])
        return new_func
        # exec(obj['code'], obj['globals'], result)
        # return result[obj['name']]
      elif obj['__type__'] == 'class':
        new_class = type(obj['name'], (object, ), obj['members'])
        return new_class
    return obj