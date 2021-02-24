from django import forms

from ecommerce.models import Item, Info


class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user',)


class InfoCreationForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = '__all__'

    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['item'] = forms.ModelChoiceField(
            empty_label='Select item',
            queryset=user.item_set.all()
        )
