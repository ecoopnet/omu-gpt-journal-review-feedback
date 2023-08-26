#!/usr/bin/env python3


import os
import sys
from dotenv import load_dotenv
load_dotenv()
import openai
import re

def parseComments(text):
    pattern = r'###(R\d.*?)(?=\n*###|$)'

    matches = re.findall(pattern, text, re.DOTALL)

    return matches

# 入力ファイル名を取得する
if len(sys.argv) < 3:
    print('Usage: python3 split_text.py [manuscript_file] [comment_file]')
    sys.exit(1)
manuscript_file = sys.argv[1]
comment_file = sys.argv[2]

# 出力ファイル名を生成する
# base, ext = os.path.splitext(manuscript_file)
# output_file = f"{base}.out.txt"
dir = os.path.dirname(manuscript_file)
output_file = f"{dir}/output.txt"

with open(manuscript_file, 'r') as f:
    manuscriptText = f.read()

with open(comment_file, 'r') as f:
    commentText = f.read()

comments = parseComments(commentText)

for comment in comments[0:2]:
    response = openai.ChatCompletion.create(
        model='gpt-4',
        #model='gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": "You are the author of the manuscript below. Users are reviewer of it.\n\n{}".format(manuscriptText)},
            { "role": "user", "content": comment },
        ],
        n=1,
        temperature=0.5
    )
    print(response)
    print(response.choices)
    outputText = response.choices[0]["message"]["content"].strip()
with open(output_file, 'w') as f:
        f.write(outputText + '\n')


