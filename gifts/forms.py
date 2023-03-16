from django import forms
from .models import Mygifts, GiftRequest


class AddRequest(forms.ModelForm):
    class Meta:
        model = GiftRequest
        fields = ['user_name', 'user_city', 'user_message', 'user_email', 'user_phone']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_city': forms.Select(attrs={'class': 'form-control'}),
            'user_message': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'dir': 'auto'}),
            'user_email': forms.TextInput(attrs={'class': 'form-control'}),
            'user_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddGift(forms.ModelForm):
    class Meta:
        model = Mygifts
        fields = ['domaine', 'city', 'title', 'body', 'image']
        widgets = {
            'domaine': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'dir': 'auto'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'domaine': "Choisir un domaine",
            'city': "Choisir une ville",
            'title': "Titre de l'offre:",
            'body': "Description de l'offre:",
            'image': "Choisir image depuis vorte appareil:"
        }
