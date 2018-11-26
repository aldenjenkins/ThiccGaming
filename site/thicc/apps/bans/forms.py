from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db import IntegrityError
from .models import Ban, Comment, Group, Admin
#from social.apps.django_app.default.models import UserSocialAuth
from social_django.models import UserSocialAuth

def getSteam64FromString(steamid):
    steam64id = 76561197960265728  # I honestly don't know where
    # this came from, but it works...
    id_split = steamid.split(":")
    try:
        steam64id += int(id_split[2]) * 2  # again, not sure why multiplying by 2...
    except (IndexError, ValueError):
        return "Invalid Steam ID"
    if id_split[1] == "1":
        steam64id += 1
    return steam64id


class BanForm(forms.ModelForm):

    sid = forms.ChoiceField(choices=(
                (1, "Left 4 Dead 2"),
                (2, "Thicc Gaming | ZS"),
                # (3, "Thicc Scape"),
                # (4, "Thicc Gaming | JB"),
                # (5, "Thicc WoW")
            ))

    length = forms.ChoiceField(choices=(
                (0, "Permanent"),
                (1800, "30 Minutes"),
                (3600, "1 Hour"),
                (7200, "2 Hours"),
                (21600, "6 Hours"),
                (43200, "12 Hours"),
                (86400, "1 Day"),
                (172800, "2 Days"),
                (604800, "1 Week"),
                (1209600, "2 Weeks"),
                (2419200, "1 Month"),
            ), label='Ban Duration')

    authid= forms.CharField(required=True, label=_('STEAM ID'),widget = forms.TextInput(attrs={'placeholder': 'STEAM_0:1:1234567'}))

    ip = forms.CharField(required=False, label=_('User\'s IP. Not Required'), widget = forms.TextInput(attrs={'placeholder': 'x.x.x.x'}))

    def clean(self):
        cleaned_data = super(BanForm, self).clean()
        authid = cleaned_data.get('authid')
        if authid[:8] != "STEAM_0:" or len(authid) < 11:
            msg = "Invalid STEAM ID"
            self.add_error('authid', msg)
        else:
            cleaned_data['authid'] = getSteam64FromString(authid)
            return cleaned_data

    class Meta:
        model   = Ban
        fields = ('name','authid','ip','reason','length','sid',)
        labels = {
            'name': _('User\'s name'),
            'reason' : _('Reason'),

        }


class UnbanForm(forms.ModelForm):


    class Meta:
        model   = Ban
        fields  = ('ureason',)


class RebanForm(forms.ModelForm):

    length = forms.ChoiceField(choices=(
        (0, "Permanent"),
        (1800, "30 Minutes"),
        (3600, "1 Hour"),
        (7200, "2 Hours"),
        (21600, "6 Hours"),
        (43200, "12 Hours"),
        (86400, "1 Day"),
        (172800, "2 Days"),
        (604800, "1 Week"),
        (1209600, "2 Weeks"),
        (2419200, "1 Month"),
    ), label= _('Ban Duration'))

    class Meta:
        model = Ban
        fields = ('reason', 'length')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)



class GroupForm(forms.ModelForm):

    flags = forms.MultipleChoiceField(choices=Group.FLAG_CHOICES, label=_('Group\'s Flags. Select multiple with \"Shift\" or \"Control\"'))
    textual_name = forms.CharField(label=_('Group\'s textual name. ex. Admin'))
    name = forms.CharField(label=_('Group\'s numeral name. ex. 0 for Owners'))
    immunity = forms.IntegerField(max_value=100, label=_('Group\'s Immunity. Max 100'))

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        flags = cleaned_data.get('flags')
        newFlags = []
        [newFlags.append(flag) for flag in flags]
        cleaned_data['flags'] = ''.join(newFlags)

    class Meta:
        model = Group
        fields = ('textual_name', 'name',  'flags', 'immunity')


class AdminForm(forms.ModelForm):

    def clean(self):
        try:
            cleaned_data = super(AdminForm, self).clean()
        except IntegrityError as e:
            if 'unique constraint' in e.message:
                self.add_error('aid', _('This user already exists.'))
        else:
            # cleaned_data = super(AdminForm, self).clean()
            # data = self.cleaned_data
            # data['user'] = self.cleaned_data['aid'].username
            # data['srv_flags'] = self.cleaned_data.get('srv_group').flags
            try:
                test = str(UserSocialAuth.objects.get(provider='steam', user_id=cleaned_data.get('aid').id).uid)
            except UserSocialAuth.DoesNotExist:
                self.add_error('aid', _('This user does not have a STEAM account linked to their profile.'))


    def save(self, commit=True):
        instance = super(AdminForm, self).save(False)
        instance.user = instance.aid.username
        instance.srv_flags = instance.srv_group.flags
        instance.immunity = instance.srv_group.immunity
        instance.authid = str(UserSocialAuth.objects.get(provider='steam', user_id=instance.aid.id).uid)

        if commit:
            instance.save()
        return instance


    class Meta:
        model = Admin
        fields = ('aid','srv_group',)
