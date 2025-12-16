import os

import markdown
import yaml
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, CharacterCreateForm
from .models import UserProfile, Character
from .utils import load_article_meta, CONTENT_DIR

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

# 初回チュートリアル
@login_required
def onboarding(request):
    profile = request.user.userprofile

    # 種族アイコン一覧を表示する
    icons_dir = os.path.join(settings.BASE_DIR, "game/static/game/icons/races")
    ricons = [f for f in os.listdir(icons_dir) if f.endswith(".png")]

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
        "icons": ricons,
    }, )

# メイン画面遷移時チェック
@login_required
def main(request):
    profile = request.user.userprofile

    char_count = Character.objects.filter(user=request.user).count()
    if char_count == 0:
        return redirect('onboarding')

    # ログインユーザのキャラ一覧
    characters = Character.objects.filter(user=request.user).order_by('id')

    # とりあえず先頭を「選択中キャラ」として扱う
    selected = characters.first()

    context = {
        'characters': characters,
        'selected': selected,
    }
    # キャラ一覧や探索ボタンをここで描画
    return render(request, 'main.html', {
        # 'characters': Character.objects.filter(user=request.user),
    })
    
def news_list(request):
    articles = []

    for filename in os.listdir(CONTENT_DIR):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(CONTENT_DIR, filename)
        meta = load_article_meta(path)
        if not meta:
            continue

        # slug はファイル名から拝借（.md を取るだけ）
        slug = os.path.splitext(filename)[0]

        articles.append({
            "slug": slug,
            "title": meta["title"],
            "summary": meta.get("summary", ""),
            "date": meta["date"],          # 表示用文字列
            "date_obj": meta["date_obj"],  # ソート用
        })

    # 日付降順でソート（新しい順）
    articles.sort(key=lambda x: x["date_obj"], reverse=True)

    return render(request, "news_list.html", {"articles": articles})

def news_detail(request, slug):
    # mdファイルのパスを組み立てる
    md_path = os.path.join(
        settings.BASE_DIR,
        "content",
        "news",
        f"{slug}.md"
    )

    # md読み込み
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    meta = {}
    body = text

    # 先頭が --- で始まる = フロントマター（メタデータ）とする
    if text.startswith("---"):
        # --- メタ --- 内容
        _, fm_text, body = text.split("---", 2)
        meta = yaml.safe_load(fm_text) or {}

    # 表示する内容だけをMarkdown → HTMLに変換する
    html = markdown.markdown(body, extensions=["fenced_code", "tables"])

    return render(request, "news_detail.html", {
        "content": html,
        "meta": meta,
        })

def logout_view(request):
    auth_logout(request)
    return redirect('home')
