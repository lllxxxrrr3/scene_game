import streamlit as st
from call_glm import call_glm
import pandas as pd
import re
st.set_page_config(layout="wide")
prompt_start = """
为我设计出一款冒险游戏。游戏玩法是你根据我给你的一些关键词，
请根据我关键词的类型，创造一个情景（情景中可以有一些虚拟的角色）,
同时给我两个选项，这两个选项会影响后续游戏的进程。以下是关键词和输出形式

关键词：{key_words}

请生成大括号并严格以以下json格式输出：
    'scene':你创造的情景,
    'option_1':你给的选项1,
    'option_2':你给的选项2
"""

prompt_next = """
接着上面的剧情，玩家做出的选择是{option}，请根据选择和上面的情景接着
描述出故事下一步的发展，并重新生成两个选项。
注意：
1，记住上面游戏的轮数，使游戏对话大约在10-15轮结束
2，在故事的生成中，如果有涉及一些物理学或者生物学等知识，可以上网搜集相关的知识内容，并告诉我,如果没有就不生成这些内容，以我要求的格式生成其他内容.
3,在结束时，给我一个完美的结局，并且告诉我是否结束。
请生成大括号并严格的以以下的json格式输出：
    'scene':你创造的情景,
    'option_1':你给的选项1,
    'option_2':你给的选项2，
    'knowledge':你搜索到的知识,
    'end'：是否结束，你只用输出True或False
"""


def get_dict(key_words):
    if len(st.session_state.option) == 0:
        response_text = call_glm(prompt=prompt_start.format(key_words=key_words), model='glm-4')
        st.session_state.option = []
    else:
        print(st.session_state.option)
        response_text = call_glm(prompt=prompt_next.format(option=st.session_state.option[-1]), model='glm-4')
    pattern = r'({[^}]*})'
    matches = re.findall(pattern, response_text)
    response_info = matches[0].replace('\n', '')
    print(response_info)
    response_text = eval(response_info.strip())
    print(response_text)
    return response_text

if 'confirm' not in st.session_state:
    st.session_state.confirm = False
if "scene" not in st.session_state:
    st.session_state.scene = []
if "option_1" not in st.session_state:
    st.session_state.option_1 = []
if "option_2" not in st.session_state:
    st.session_state.option_2 = []
if "option" not in st.session_state:
    st.session_state.option = []
if "choose_1" not in st.session_state:
    st.session_state.choose_1 = False
if "choose_2" not in st.session_state:
    st.session_state.choose_2 = False
if "count" not in st.session_state:
    st.session_state.count = 0

def confirm():
    st.session_state.confirm = True
def choose_1():
    st.session_state.choose_1 = True
    st.session_state.option.append(st.session_state.option_1[-1])
def choose_2():
    st.session_state.choose_2 = True
    st.session_state.option.append(st.session_state.option_2[-1])

key_word = st.text_input("请输入关键词", key='key_words')
print("refresh:",st.session_state.option)
option_1 = {'选项1': []}
option_2 = {'选项2': []}
st.write(st.session_state.choose_1, st.session_state.choose_2)
if st.session_state.confirm == True or st.button("确定"):
    st.session_state.confirm = True    
    if st.session_state.count == 0:
        input_text = get_dict(key_word)
    else:
        input_text = get_dict('')
    st.session_state.scene.append(input_text["scene"])
    st.session_state.option_1.append(input_text["option_1"])
    st.session_state.option_2.append(input_text["option_2"])
    st.write(st.session_state.scene[-1])
    col1, col2 = st.columns(2)
    with col1:
        st.button(st.session_state.option_1[-1], on_click=choose_1)
        if st.session_state.choose_1:
            st.session_state.choose_1 = False
            st.rerun()
    with col2:
        st.button(st.session_state.option_2[-1], on_click=choose_2)
        if st.session_state.choose_2:
            st.session_state.choose_2 = False
            st.rerun()


        
        

print(st.session_state.scene)
print(st.session_state.option_1)
print(st.session_state.option_2)
print("option:", st.session_state.option)



