from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, CharacterCreateForm
from .models import UserProfile, Character

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # ひとまずトップに戻す（あとでログインページに飛ばしてもよい）
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_id = form.cleaned_data['login_id'].lower()
            password = form.cleaned_data['password']

            # 1. メールアドレスとして認証（username = email）
            user = authenticate(request, username=login_id, password=password)

            # 2. ダメなら account_id から User を引く
            if user is None:
                try:
                    profile = UserProfile.objects.get(account_id=login_id)
                    user = authenticate(
                        request,
                        username=profile.user.username,
                        password=password,
                    )
                except UserProfile.DoesNotExist:
                    user = None

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('main')  # ログインに成功したのでメイン画面へ
                else:
                    form.add_error(None, 'このアカウントは無効化されています。')
            else:
                form.add_error(None, 'ログインIDまたはパスワードが正しくありません。')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

#初回チュートリアル
@login_required
def onboarding(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = CharacterCreateForm(request.POST)
        if form.is_valid():
            char = form.save(commit=False)
            char.user = request.user
            char.save()

            profile.onboarding_completed = True
            profile.save()

            return redirect('main')
    else:
        form = CharacterCreateForm()

    return render(request, 'onboarding.html', {
        'form': form,
    })

#メイン画面遷移時チェック
@login_required
def main(request):
    profile = request.user.userprofile

    char_count = Character.objects.filter(user=request.user).count()
    if char_count == 0:
        return redirect('onboarding')

    # キャラ一覧や探索ボタンをここで描画
    return render(request, 'main.html', {
        # 'characters': Character.objects.filter(user=request.user),
    })

def logout_view(request):
    auth_logout(request)
    return redirect('home')
