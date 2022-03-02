from django import forms
from django.core.validators import RegexValidator

#channel_id=RegexValidator(r'(\S{24})',message='please use the serach bar to find the reuqired channel ID.')
                           #please use the serach bar to find the reuqired channel ID')
#validators=[channel_id]
class Fooform(forms.Form):
    #username = forms.CharField(required=False)
    channelname=forms.CharField(        
        required=True,min_length=24,widget= forms.TextInput(attrs={'placeholder':'Please enter the 24 character Channel ID'}))
     
                           
    
# class PlayListForm(forms.Form):
#     pass
    
    
# class ChannelIdForm(forms.Form):
#     keyword=forms.CharField(required=True)
