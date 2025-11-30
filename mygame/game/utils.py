import os
import yaml
from datetime import datetime

from django.conf import settings

CONTENT_DIR = os.path.join(settings.BASE_DIR, "content", "news")


def load_article_meta(path):
    # 1つのmdファイルから front matter（date/title/summary）だけ取る"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 先頭が --- で始まる前提
    if not text.startswith("---"):
        return None

    # front matter 部分を切り出す
    _, fm_text, _ = text.split("---", 2)  # 先頭から2回目の --- まで

    meta = yaml.safe_load(fm_text)

    # 必須項目がなければスキップ
    if not meta or "date" not in meta or "title" not in meta:
        return None

    # 日付はソート用に datetime に変換しておく
    meta["date_obj"] = datetime.strptime(meta["date"], "%Y-%m-%d")

    return meta