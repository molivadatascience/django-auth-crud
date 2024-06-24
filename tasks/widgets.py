from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import re

class MultiFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value:
            for file in value:
                html += format_html('<p>{}</p>', file.name)
        return html

    def value_from_datadict(self, data, files, name):
        if isinstance(files.get(name), list):
            return files.getlist(name)
        return files.get(name, None)

    def format_value(self, value):
        if isinstance(value, (list, tuple)):
            return [f.name for f in value]
        return value.name if value else ''