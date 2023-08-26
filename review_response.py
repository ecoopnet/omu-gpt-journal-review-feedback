#!/usr/bin/env python3


import os
import sys
from dotenv import load_dotenv
load_dotenv()
import openai
import re

def parseComments(text):
    pattern = r'###(R[^ ]+) +(.*?)(?=\n*###|$)'

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
output_file = f"{dir}/answers.txt"

with open(manuscript_file, 'r') as f:
    manuscriptText = f.read()

with open(comment_file, 'r') as f:
    commentText = f.read()

comments = parseComments(commentText)

outputText = ''

promptText = "Please assist me in writing my paper as a virtual co-author. Currently, we are in the revision stage. I will present both the comments from the reviewers and my manuscript below. Please answer every reviewers's question step-by-step in a scientific manner. During the response, indicate which parts of the manuscript were modified. \n"

for comment in comments:
    (commentId, commentText) = comment
    response = openai.ChatCompletion.create(
        model='gpt-4',
        #model='gpt-3.5-turbo',
        messages = [
            {"role": "system", "content": "{}\n{}".format(promptText, manuscriptText)},
            { "role": "user", "content": commentText },
        ],
        n=1,
        temperature=0.5
    )
    print(response)
    print(response.choices)
    answerText = response.choices[0]["message"]["content"].strip()
    outputText += f'###{commentId}\n{answerText}\n\n'

with open(output_file, 'w') as f:
        f.write(outputText + '\n')


