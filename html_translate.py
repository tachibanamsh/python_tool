from bs4 import BeautifulSoup, NavigableString
from google.cloud import translate_v2 as translate

# Google Cloud Translation APIのクライアントを初期化
translate_client = translate.Client()

def translate_text(text, target_language='en'):
    # HTMLエンティティをデコードしてから翻訳
    response = translate_client.translate(text, target_language=target_language)
    return response['translatedText']

def translate_nested_tags(tag):
    # タグ内のNavigableStringオブジェクト（テキスト）を翻訳
    for content in tag.contents:
        if isinstance(content, NavigableString) and content.strip():
            translated_text = translate_text(content, target_language='en')
            content.replace_with(translated_text)
        elif content.name:  # 子タグがある場合、再帰的に処理
            translate_nested_tags(content)

# HTMLファイルを読み込む
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 翻訳するタグを指定
tags = ['p', 'th', 'td', 'h1', 'h2', 'h3', 'h4', 'li', 'a', 'span']
for tag in soup.find_all(tags):
    translate_nested_tags(tag)

# 翻訳後のHTMLをファイルに保存
with open('index_out4.html', 'w', encoding='utf-8') as file_out:
    file_out.write(str(soup))
