from django import forms

class registration(forms.Form):
    user_name = forms.CharField(max_length=20)
    pass_word = formms.CharField(max_length=20)
    email_id = forms.EmailField()
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    

class information(forms.Form):
    message = forms.CharField(label='Message:')
    thumb = forms.ImageField()


