import random
from typing import Tuple
from collections import OrderedDict
from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.fields import empty
import string

from file.models import File


"""
util functions
"""


def _read_file_content(instance: File) -> list[str]:
    content = []
    file_path = instance.content.path
    with open(file_path, 'r') as file:
        for line in file.readlines():
            clean_str = line.strip('\t\n').strip()
            content.append(clean_str) if clean_str else content.append("")
    return content


def _get_random_line_with_line_number(content: list[str]) -> Tuple[str, int]:
    # empty txt file case
    content_len = len(content)
    if content_len == 0:
        return "", 0

    rnd_idx = random.choice(range(content_len))
    return content[rnd_idx], rnd_idx + 1


"""
Serializers
"""


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["content"]


class OneRandomLineSerializer(serializers.Serializer):
    application_headers = ['application/json', 'application/xml']
    # Only required field
    line = serializers.CharField(required=True)
    # These fields are optional, depends on accept_headers
    line_number = serializers.IntegerField(required=False)
    file_name = serializers.CharField(required=False)
    most_frequent_letter = serializers.CharField(
        required=False, max_length=1)  # single character

    def __init__(self, instance=None, data=empty, accept_header='application/json', **kwargs):
        super().__init__(instance, data, **kwargs)
        self._accept_header = accept_header

    def to_representation(self, instance: File):
        ret = OrderedDict()
        content = _read_file_content(instance)
        random_line, line_number = _get_random_line_with_line_number(content)
        ret["line"] = random_line

        if self._accept_header in self.application_headers:
            ret["line_number"] = line_number
            ret["file_name"] = self._get_file_name(instance)
            ret["most_frequent_letter"] = self._get_most_frequent_letter(
                random_line)
        return ret

    def _get_file_name(self, instance: File) -> str:
        return instance.content.name

    def _get_most_frequent_letter(self, random_line: str) -> str:
        try:
            most_freq_letter = max(
                random_line, key=lambda x: random_line.count(x) if (x in string.ascii_letters) else 0)
            return most_freq_letter
        except ValueError as e:
            return ""


class OneRandomLineBackwardSerializer(serializers.Serializer):
    random_backward_line = serializers.SerializerMethodField(
        "get_random_backward_line")

    def get_random_backward_line(self, obj: File):
        # First read the content
        file_content = _read_file_content(instance=obj)
        # Then get your random line with line number(ignored for this case)
        random_line, _ = _get_random_line_with_line_number(file_content)
        # Return the random line backwards
        return random_line[::-1] if len(random_line) != 0 else ""


class LongestHundredLinesSerializer(serializers.Serializer):
    longest_hundred_lines = serializers.ListField(
        child=serializers.CharField(), max_length=100
    )

    # our custom ListSerializer class
    def to_representation(self, data):
        field_name = "longest_hundred_lines"
        max_length = self.fields[field_name].max_length
        ret_list = self._get_longest_hundred_lines(data
                                                   )
        # Now, sort `ret_list` according to the length of elements
        ret_list.sort(key=len, reverse=True)

        ret = OrderedDict()

        # return first `max_length` elements from the sorted list of strings (by length)
        ret[field_name] = ret_list[:max_length]
        return ret

    def _get_longest_hundred_lines(self, queryset) -> list[str]:
        ret_list: list[str] = []

        for file_obj in queryset:
            ret_list.extend(_read_file_content(instance=file_obj))

        return ret_list


class LongestTwentyLinesSerializer(serializers.Serializer):
    longest_twenty_lines = serializers.ListField(
        child=serializers.CharField(), max_length=20
    )

    def to_representation(self, data):
        field_name = "longest_twenty_lines"
        max_length = self.fields[field_name].max_length
        ret_list = self._get_longest_twenty_lines(data)

        # Now, sort `ret_list` according to the length of elements
        ret_list.sort(key=len, reverse=True)

        ret = OrderedDict()

        # return first `max_length` elements from the sorted list of strings (by length)
        ret[field_name] = ret_list[:max_length]
        return ret

    def _get_longest_twenty_lines(self, instance: File) -> list[str]:
        return _read_file_content(instance)
