import streamlit as st
from call_glm1 import call_glm

prompt_start = """
为我设计出一款冒险游戏。游戏玩法是你根据我给你的一些关键词，
请根据我关键词的类型，创造一个情景（情景中可以有一些虚拟的角色）,
同时给我两个选项，这两个选项会影响后续游戏的进程。以下是关键词和输出形式

关键词：{key_words}

请生成大括号并严格以以下json格式输出：
    scene:你创造的情景,
    option_1:你给的选项1,
    option_2:你给的选项2
"""

prompt_image = """
我会给你一个情景和两个选项，为此给我生成一张相关的图片
情景:{scene},
选项1:{option_1},
选项2:{option_2},
"""

prompt_next = """
接着上面的剧情，玩家做出的选择是{option}，请根据选择和上面的情景接着
描述出故事下一步的发展，并重新生成两个选项。
注意：
1，记住上面游戏的轮数，使游戏对话大约在10-15轮结束
2，在故事的生成中，如果有涉及一些物理学或者生物学等知识，可以上网搜集相关的知识内容，并告诉我.
3,在结束时，给我一个完美的结局，并且告诉我是否结束。
3，请生成大括号并严格的以以下的json格式输出：
    scene:你创造的情景,
    option_1:你给的选项1,
    option_2:你给的选项2，
    knowledge:你搜索到的知识,
    end：是否结束，你只用输出True或False
"""


def get_dict(key_words):
    # st.text_input('请输入创建场景的关键词',key='key_words')
    response_text = call_glm(prompt=prompt_start.format(key_words=key_words), model='glm-4')
    print(response_text)
    response_text = response_text.replace("`","").replace("json","")
    response_text = eval(response_text)
    return response_text
# print(type(response_text))
# response_image = call_glm(prompt=prompt_image.format(scene=response_text['scene'],
#                                                     option_1=response_text['option_1'],
#                                                     option_2=response_text['option_2']),
#                           model='cogview-3')

# print(response_image)

if "session_count" not in st.session_state:
    st.session_state["session_count"] = None

def session(reponse):
    st.write(reponse['scence'])
    if reponse["end"]:
        col1, col2 = st.columns(2)
        with col1:
            st.button(reponse['option_1'])    
        with col2:
            st.button(reponse['option_2'])

def streamlit_main():
    st.text_input("请输入关键词",key='key_words')
    input_text = get_dict(st.session_state['key_words'])
    st.write(input_text['scene'])
    # col1, col2 = st.columns(2)
    # with col1: 
    opt1 = st.button(input_text['option_1'],key='b1')
    # with col2:
    opt2 = st.button(input_text['option_2'],key='b2')

            


streamlit_main()