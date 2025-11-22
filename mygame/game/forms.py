from django import forms
from django.contrib.auth.models import User
import re
from .models import UserProfile, Character

ACCOUNT_ID_REGEX = r'^[A-Za-z0-9_-]{5,20}$'
PASSWORD_REGEX_ALLOWED = r'^[A-Za-z0-9!$%&\'()*+,/;<=>?\[\]^{}~]{8,64}$'

class SignUpForm(forms.ModelForm):
    #アカウント名として一意に用いる
    account_id = forms.CharField(
        label='アカウントID',
        help_text='5〜16文字の半角英数字とアンダースコア(_), ハイフン(-)のみ利用できます。',
    )
    password = forms.CharField(
        label='パスワード',
        help_text='大文字,小文字,数字,記号の２種類が必要です。',
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='パスワード（確認）',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email',)
        labels = {
            'email': 'メールアドレス',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email

    def clean_account_id(self):
        raw = self.cleaned_data['account_id']
        account_id = raw.lower()

        # 文字種チェック
        if not re.match(ACCOUNT_ID_REGEX, account_id):
            raise forms.ValidationError(
                'アカウントIDは5〜16文字の半角英数字とアンダースコア(_)のみのひつようがあります。'
            )

        # 一意チェック
        if UserProfile.objects.filter(account_id=account_id).exists():
            raise forms.ValidationError('このアカウントIDは既に使われています。')

        return account_id

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', 'パスワードが一致しません。')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email'].lower()
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                account_id=self.cleaned_data['account_id']  # すでに小文字化済み
            )
        return user

def validate_password_strength(password):
    # 長さと許可文字チェック
    if not re.match(PASSWORD_REGEX_ALLOWED, password):
        raise forms.ValidationError(
            'パスワードは8〜64文字で、半角英数字および指定記号のみ使用できます。'
        )

    # 各種判定
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[!$%&\'()*+,/;<=>?\[\]^{}~]', password))

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    # 最低2種類を要求
    if score < 2:
        raise forms.ValidationError(
            '大文字・小文字・数字・記号のうち、少なくとも2種類を含めてください。'
        )

#キャラ作成
class CharacterCreateForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name',)
        labels = {
            'name': 'キャラ名',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) == 0:
            raise forms.ValidationError("名前を入力してください。")
        if len(name) > 15:
            raise forms.ValidationError("名前は15文字以内で入力してください。")
        return name

class LoginForm(forms.Form):
    login_id = forms.CharField(
        label='ログインID',
        help_text='登録メールアドレス または アカウントID でログインできます。',
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput
    )
