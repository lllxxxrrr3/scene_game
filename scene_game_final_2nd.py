import streamlit as st
from call_glm import call_glm, call_cogview
import re

st.set_page_config(
    page_title='ZhipuAI Streamlit App',
    page_icon=':smiley:',
    layout='wide',
    initial_sidebar_state='expanded'
)

import streamlit as st

prompt_start = """
为我设计出一款冒险游戏。游戏玩法是你根据我给你的一些关键词，
请根据我关键词的类型，创造一个情景（情景中可以有一些虚拟的角色）,同时设计出自己的角色设定,
同时给我两个选项，这两个选项会影响后续游戏的进程。以下是关键词和输出形式

关键词：{key_words}

请生成大括号并严格以以下json格式输出：
    'scene':你创造的情景,
    'option_1':你给的选项1,
    'option_2':你给的选项2,
    'character':角色形象
"""

prompt_next = """
接着上面的剧情，玩家做出的选择是{option}，同时当前情景已进行{count}轮,
请根据选择和上面的情景，以及当前轮数与目标结束轮的关系，,接着描述出故事下一步的发展，并重新生成两个选项。
注意：
1,记住上面游戏的轮数,使游戏对话大约在10-15轮结束
2,在故事的生成中,如果有涉及一些物理学或者生物学等知识,可以上网搜集相关的知识内容,并告诉我,如果没有就不生成这些内容，以我要求的格式生成其他内容.
3,在结束时，给我一个完美的结局，并且告诉我是否结束。
请生成大括号并严格的以以下的json格式输出:
    'scene':你创造的情景,
    'option_1':你给的选项1,
    'option_2':你给的选项2,
    'character':{character}
    'knowledge':你搜索到的知识,
    'end':是否结束,你只用输出True或False
"""

prompt_end = """
接着上面的剧情，玩家做出的选择是{option}，主角的形象是{character},
请根据以上剧情{memory},对故事进行结尾，输出字数为500字左右。

请生成大括号并严格的以以下的json格式输出：
    'scene':你创造的情景
"""

prompt_image = """
{scene}这是我给你的情景，主角的形象是{character}，请按照以下情景生成一副动漫风格的图片
"""


def get_dict(key_words):
    if len(st.session_state.option) == 0:
        response_text = call_glm(prompt=prompt_start.format(key_words=key_words), model='glm-4')
    elif st.session_state.count == 7:
        response_text = call_glm( prompt=prompt_end.format(option=st.session_state.option[-1], memory=st.session_state.scene,
                                                           character = st.session_state.character),model='glm-4')
    else:
        response_text = call_glm(prompt=prompt_next.format(option=st.session_state.option[-1], character = st.session_state.character,
                                                           count=st.session_state.count), model='glm-4')

    # pattern = r'({[^}]*})'
    # matches = re.findall(pattern, response_text)
    # response_info = matches[0].replace('\n', '')
    # response_text = eval(response_info.strip())

    response_text = response_text.replace("`","").replace("json","")
    response_text = eval(response_text.strip())
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
if "knowledge" not in st.session_state:
    st.session_state.knowledge = []
if "choose_1" not in st.session_state:
    st.session_state.choose_1 = False
if "choose_2" not in st.session_state:
    st.session_state.choose_2 = False
if "chosen_options" not in st.session_state:
    st.session_state.chosen_options = []
if "count" not in st.session_state:
    st.session_state.count = 0
if "image" not in st.session_state:
    st.session_state.image = []
if "character" not in st.session_state:
    st.session_state.character = ''
if 'last_button_clicked' not in st.session_state:
    st.session_state.last_button_clicked = False


def confirm():
    st.session_state.confirm = True


def choose_1():
    st.session_state.choose_1 = True
    st.session_state.option.append(st.session_state.option_1[-1])
    st.session_state.chosen_options.append(1)


def choose_2():
    st.session_state.choose_2 = True
    st.session_state.option.append(st.session_state.option_2[-1])
    st.session_state.chosen_options.append(2)


key_word = st.text_input("请输入关键词", key='key_words')

if st.session_state.confirm == True or st.button("确定"):
    st.session_state.confirm = True
    if st.session_state.count == 0:
        input_text = get_dict(key_word)
    else:
        input_text = get_dict('')
        st.session_state.last_button_clicked = input_text['end']

    st.session_state.scene.append(input_text["scene"])
    st.session_state.option_1.append(input_text["option_1"])
    st.session_state.option_2.append(input_text["option_2"])
    st.session_state.knowledge.append(input_text.get("knowledge", ""))
    st.session_state.character = input_text["character"]
    image = call_cogview(prompt=prompt_image.format(scene = st.session_state.scene[-1],
                                                character = st.session_state.character))
    st.session_state.image.append(image)

    st.session_state.count += 1

    for i in range(st.session_state.count):
        st.write(st.session_state.scene[i])
        st.image(st.session_state.image[i])
        with st.container():
            if i < len(st.session_state.chosen_options):
                if st.session_state.chosen_options[i] == 1:
                    with st.container():
                        st.success(f"你选择了: {st.session_state.option_1[i]}")
                elif st.session_state.chosen_options[i] == 2:
                    with st.container():
                        st.success(f"你选择了: {st.session_state.option_2[i]}")

                # 如果有相关知识，显示在选择内容的下方
                if st.session_state.knowledge[i]:
                    with st.container():
                        st.info(f"相关知识: {st.session_state.knowledge[i]}")
            else:
                if st.session_state.count==7:
                    input_text = get_dict('')
                    st.session_state.scene.append(input_text["scene"])
                    st.write(st.session_state.scene[-1])
                    st.markdown("# 结束 🎉")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button(st.session_state.option_1[i], on_click=choose_1, key=f'b1_{i}')
                    with col2:
                        st.button(st.session_state.option_2[i], on_click=choose_2, key=f'b2_{i}')

print(st.session_state.scene)
print(st.session_state.option_1)
print(st.session_state.option_2)
print("option:", st.session_state.option)
print("chosen_options:", st.session_state.chosen_options)
print("knowledge:", st.session_state.knowledge)