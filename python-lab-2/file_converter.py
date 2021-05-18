import yaml_serializer
import json_serializer
import os

class FileConverter:

  def convert(self, input_filepath, output_filepath):
    _temp, input_extension = os.path.splitext(input_filepath)
    _temp, output_extension = os.path.splitext(output_filepath)
    input_serializer = self._create_serializer(input_extension.strip('.'), False)
    output_serializer = self._create_serializer(output_extension.strip('.'), False)
    deserialized = input_serializer.load(input_filepath)
    output_serializer.dump(deserialized, output_filepath)


  def _create_serializer(self, serializer_type, convert_complex):
    if serializer_type == 'json':
      return json_serializer.JsonSerializer(convert_complex)
    elif serializer_type == 'yaml':
      return yaml_serializer.YamlSerializer(convert_complex)
    else:
      raise Exception(f'Serializer type "{serializer_type}" is not supported')
  

