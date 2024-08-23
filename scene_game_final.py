import streamlit as st
import json
import re
from zhipuai import ZhipuAI
from PIL import Image

st.set_page_config(
    page_title='ZhipuAI Streamlit App',
    page_icon=':smiley:',
    layout='wide',
    initial_sidebar_state='expanded'
)

prompt_start = """
你是关键词冒险，你是一个创造性的故事编织者，通过用户输入的关键词构建情景和角色，并提供两个选项引导故事发展。你的能力有:
- 分析关键词，构建情景和角色；
- 根据用户选择，推进故事情节；
- 在第三轮结束时，设置故事结局；
- 如涉及专业知识，上网搜集相关内容。

以下是关键词和输出形式

关键词：{key_words}

请生成大括号并严格以以下json格式输出：
    'scene':你创造的情景,
    'option_1':你给的选项1,
    'option_2':你给的选项2

"""

prompt_next = """
接着上面的剧情，玩家做出的选择是{option}，请根据选择和上面的情景接着
描述出故事下一步的发展，但是需要尽快完结，并继续重新生成两个选项，记录游戏轮数，
注意：
你的能力有:
- 分析关键词，构建情景和角色；
- 根据用户选择，推进故事情节；
- 在第三轮结束时，设置故事结局；
- 如涉及专业知识，上网搜集相关内容。

请生成大括号并严格的以以下的json格式输出：
    'scene':你创造的情景,
    'option_1':当前轮数+你给的选项1,
    'option_2':当前轮数+你给的选项2，
    'knowledge':你搜索到的知识,
    'end'：是否结束，只需输入False或True，但是请在第四轮选择后设置end=True，
"""

def call_glm(prompt, model,temperature=0.7,max_tokens=2048,top_p=0.75,**kwargs):
    client = ZhipuAI(api_key='a13a4b4673179c29ce2d0edff7e91e36.858H7Zd4dUF9Mdb9')
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
    #print(response_info)
    response_text = eval(response_info.strip())
    #response_text = json.loads(response_text)
    #print(response_text)
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
if 'last_button_clicked' not in st.session_state:
    st.session_state.last_button_clicked = False

def confirm():
    st.session_state.confirm = True

def choose_1():
    st.session_state.choose_1 = True
    st.session_state.option.append(st.session_state.option_1[-1])

def choose_2():
    st.session_state.choose_2 = True
    st.session_state.option.append(st.session_state.option_2[-1])

key_word = st.text_input("请输入关键词", key='key_words')
print("refresh:", st.session_state.option)
option_1 = {'选项1': []}
option_2 = {'选项2': []}
st.write(st.session_state.choose_1, st.session_state.choose_2)
if st.session_state.confirm == True or st.button("确定"):
    st.session_state.confirm = True
    if st.session_state.count == 0:
        input_text = get_dict(key_word)
        st.session_state.count=1
    else:
        input_text = get_dict('')
        st.session_state.count +=1
        print(st.session_state.count)
        st.session_state.last_button_clicked = input_text['end']
        print(st.session_state.last_button_clicked)

    st.session_state.scene.append(input_text["scene"])
    st.session_state.option_1.append(input_text["option_1"])
    st.session_state.option_2.append(input_text["option_2"])

    st.write(st.session_state.scene[-1])

    if  st.session_state.count==4:
        print(st.session_state.last_button_clicked)
        print("结束")
        st.markdown("# 结束 🎉")
        st.session_state['story'] = ''
        st.session_state['history'] = []
    else:
        print("继续")
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
# print(st.session_state.option_1)
# print(st.session_state.option_2)
print("option:", st.session_state.option)