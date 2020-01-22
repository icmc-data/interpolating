from django  import forms

class PictureForm(forms.Form):
    auth_token = forms.CharField(label='auth_token', max_length=100)
    photo      = forms.FileField()

class PlayForm(forms.Form):
    id = forms.CharField(label="id", max_length=10)

class MoveForm(forms.Form):
    auth_token = forms.CharField(label='auth_token', max_length=100)
    btn_mover  = forms.CharField(label='btn_mover')

class ProccessForm(forms.Form):
    auth_token     = forms.CharField(label='auth_token', max_length=100)
    btn_processar  = forms.CharField(label='btn_processar')

class ID_ProccessForm(forms.Form):
    auth_token = forms.CharField(label='auth_token', max_length=100)
    imagem_id   = forms.CharField(label='imagem_id',   max_length=10)
    btn_processar_id  = forms.CharField(label='btn_processar_id')