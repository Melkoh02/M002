import json
import re

from django.core.exceptions import ImproperlyConfigured
from rest_framework import parsers
from rest_framework.exceptions import ValidationError

from utils.misc import querydict_to_dict


def assign_on_path(obj, path, obj_to_assign, is_obj_or_dict=False):
    """
        assign something onto a nested object based on a path
        {house:
           [
             {name: room1},
             {name: None},
           ]
        }
        assigning with the following path: house.[1].name
        can assign what you want to the field that says None in the example
    """
    arr_regx = re.compile(r'^\[(\d+)]$')

    def assign_on_path_internal(obj2, path_arr, obj_to_assign2):
        if len(path_arr) == 1:
            if match := arr_regx.match(path_arr[0]):
                obj2[int(match.group(1))] = obj_to_assign2
            else:
                if is_obj_or_dict:
                    setattr(obj2, path_arr[0], obj_to_assign2)
                else:
                    obj2[path_arr[0]] = obj_to_assign2
        else:
            head, tail = path_arr[0], path_arr[1:]
            if match := arr_regx.match(head):
                assign_on_path_internal(obj2[int(match.group(1))], tail, obj_to_assign2)
            else:
                assign_on_path_internal(getattr(obj2, head) if is_obj_or_dict else obj2[head], tail, obj_to_assign2)

    assign_on_path_internal(obj, path.split('.'), obj_to_assign)


class MultipartCollectedJsonParserMediaUpload(parsers.MultiPartParser):
    """
      Accepts a multipart request, and recombines the files onto the nested json object expected in the 'data' field
      the files must come with the full path with the object to recombine.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )

        try:
            data = json.loads(result.data["data"])
            files = querydict_to_dict(result.files)
            for path, file in files.items():
                assign_on_path(data, path, file)
        except (ValueError, KeyError, AttributeError):
            raise ValidationError('Wrong multipart request format')

        return data


class CollectedMultipartJsonViewMixin:
    parser_classes = (MultipartCollectedJsonParserMediaUpload, parsers.JSONParser)


class SerializerClassByActionMixin:
    def get_serializer_class(self):
        default = getattr(self, 'serializer_class', None)
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
            else:
                for k, v in self.action_serializers.items():
                    if isinstance(k, tuple) and self.action in k:
                        return v
            return default

        raise ImproperlyConfigured(
            "SerializerByActionMixin requires a definition of 'action_serializers'"
        )
