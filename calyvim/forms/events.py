from django import forms


class EventCreateForm(forms.Form):
    name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    duration = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control", "value": "30"}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
    )
    schedule = forms.CharField(required=True)


class OneOnOneEventCreateForm(EventCreateForm):
    pass
