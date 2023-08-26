#!/usr/bin/env python3

import os
import sys
import openai

# 入力ファイル名を取得する
if len(sys.argv) < 2:
    print('Usage: python3 split_text.py [input_file]')
    sys.exit(1)
input_file = sys.argv[1]

# 出力ファイル名を生成する
base, ext = os.path.splitext(input_file)
output_file = f"{base}.out.txt"


# 会話ログを読み込む
with open(input_file, 'r') as f:
    logs = f.read().split()

maxInputTextLength = 1500

# 会話ログ文字列を空白で分割する
texts = []
for log in logs:
    if len(log) > 0:
        texts.extend(log.split())

# 最大 maxInputTextLength 文字になるように、ただし会話が途中で途切れないように切り分ける
inputTexts = []
inputText = ''
for text in texts:
    if len(inputText + text) > maxInputTextLength:
        inputTexts.append(inputText.strip())
        inputText = text + ' '
    else:
        inputText += text + ' '
if len(inputText) > 0:
    inputTexts.append(inputText.strip())

# inputTexts の要素が maxInputTextLength 文字になっているかチェックする
# inputTexts の各要素をOpenAI APIのGPT3.5-turboモデルのcompletionタスクに投げる
prefix = '以下の入力文章を変換して出力してください。\n入力は空白区切りの会話文章群です。\n誤字の修正は行ってもいいですが、決して要約しないでください。\n出力は空白を句読点に変換し、「。」のあとは改行し、空行を挟んで出力してください。'
# prefix = '以下のメッセージ群を整形してください。入力は空白区切りです。出力は空白をなくして句読点と改行を足し読みやすくして下さい。会話の区切りは"\n\n"で区切ってください。誤字の修正は行ってもいいですが、決して要約しないでください。'
with open(output_file, 'w') as f:
    for i, inputText in enumerate(inputTexts):
        prompt = prefix + inputText
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            #model='gpt-3.5-turbo-0301',
            messages = [
                { "role": "user", "content": prefix },
                { "role": "user", "content": "入力: \n"+inputText + "\n\n----\n出力:\n" }
            ],
            # max_tokens=4096 - 60 - maxInputTextLength, # 入力文字列を引いたトークン数にする
            n=1,
            temperature=0.1
        )
        print(response)
        print(response.choices)
        outputText = response.choices[0]["message"]["content"].strip()
        print(outputText + "\n")
        f.write(outputText + '\n')
        # exit()


