from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings

from .forms import SignUpForm, LoginForm
from .models import UserProfile
from .utils import load_article_meta, CONTENT_DIR
import os
import markdown
import yaml

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
                    return redirect('home')  # とりあえずトップへ
                else:
                    form.add_error(None, 'このアカウントは無効化されています。')
            else:
                form.add_error(None, 'ログインIDまたはパスワードが正しくありません。')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

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
