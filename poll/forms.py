from django import forms


class ChoiseManyForm(forms.Form):
    form = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=[])

    def __init__(self, choices_options=None, *args, **kwargs):
        super(ChoiseManyForm, self).__init__(*args, **kwargs)
        if choices_options:
            self.fields['form'].choices = [
                (str(k), v) for k, v in zip(choices_options,choices_options)]


class ChooseOneForm(forms.Form):
    form = forms.ChoiceField(widget=forms.RadioSelect, choices=[])

    def __init__(self, choices_options=None, *args, **kwargs):
        super(ChooseOneForm, self).__init__(*args, **kwargs)
        if choices_options:
            self.fields['form'].choices = [(str(k), v) for k, v in
                                           zip(choices_options,choices_options)]


class TextInputForm(forms.Form):
    form = forms.CharField(widget=forms.TextInput)


"""class ChoiseForm(forms.Form):

    options = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )
    form = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                     choices=options)"""
