from zhipuai import ZhipuAI
import os
import sys
sys.path.append(os.path.abspath('.'))
from API import API_KEY

def call_glm(prompt, model,temperature=0.7,max_tokens=2048,top_p=0.75,**kwargs):
    client = ZhipuAI(api_key=API_KEY)
    response_text = ""
    try:
        response = client.chat.completions.create(
            model=model,
            messages = [{"role":"user","content":prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p)
        response_text = response.choices[0].message.content
    except Exception as e:
        print(e)
        response_text = 'Error'

    return response_text


