from django import forms
from .models import LostItem, FoundItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ["name", "description", "location", "image"]

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ["location", "image"]

class MatchItemForm(forms.Form):
    lost_item_id = forms.IntegerField(label="Enter Lost Item ID", widget=forms.NumberInput(attrs={'class': 'form-control'}))
