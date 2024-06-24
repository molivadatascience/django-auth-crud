from django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is not None:
            attrs.update({'multiple': True})
        else:
            attrs = {'multiple': True}