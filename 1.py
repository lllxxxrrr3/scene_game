import streamlit as st
from zhipuai import ZhipuAI
import json
from PIL import Image  # PIL库用于图像处理

# 假设这是与智谱AI通信的客户端实例
client = ZhipuAI(api_key='a13a4b4673179c29ce2d0edff7e91e36.858H7Zd4dUF9Mdb9')

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
prompt_next = """
接着上面的剧情，玩家做出的选择是{choice}，请根据选择和上面的情景接着
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
    
    1，从1开始计数轮次，必须当游戏对话在第3轮时设置‘end’=True结束故事，
2，在故事的生成中，如果有涉及一些物理学或者生物学等知识，可以上网搜集相关的知识内容，并告诉我,如果没有就不生成这些内容，以我要求的格式生成其他内容.
3,在结束时，给我一个完美的结局，并且告诉我是否结束。
"""


# 获取AI响应的函数
def get_assistant_response(prompt):
    response = client.chat.completions.create(
        model="glm-4-0520",
        messages=[
            {"role": "user", "content": prompt}
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )
    answer = (dict(response.choices[0].message))["content"]
    return answer


def get_dict(words):
    if len(st.session_state['story']) == 0:
        response_text = get_assistant_response(prompt_start.format(key_words=words))
    else:
        print(words)
        response_text = get_assistant_response(prompt_next.format(choice=words))
    response_text = response_text.replace("`", "").replace("json", "")
    try:
        response_dict = json.loads(response_text)
    except json.JSONDecodeError:
        response_dict = {}  # 或者进行适当的错误处理
    return response_dict

def button_clicked(i):

    container.write(i)
    choice=st.session_state['options'][i]
    response_next = get_dict(choice)
    st.session_state['story'] = response_next['scene']
    st.session_state['options'] = [response_next['option_1'], response_next['option_2']]
    st.session_state['knowledge']=response_next['knowledge']
    st.session_state.last_button_clicked=response_next['end']

    if st.session_state['story']:
        st.write(st.session_state['story'])
    if st.session_state['knowledge']:
        st.write(st.session_state['knowledge'])
    print("来啦0")
    st.session_state['history'].append((st.session_state['story'], choice))

    if len(st.session_state['history']) == 0:
        print("来啦1")
        container.write("请开始你的选择...")
    else:
        print("来啦2")
        # 显示历史记录中的所有输入和 AI 响应
        for index, (choice, st.session_state['story']) in enumerate(st.session_state['history']):
            container.write(f"选择 {index + 1}: {choice}")
            container.write(f"AI 响应: {st.session_state['story']}")

    if st.session_state.last_button_clicked:
        image = draw_story_image(st.session_state['history'])
        st.image(image, caption='冒险故事的插图')
        st.session_state['story'] = ''
        st.session_state['history'] = []
    else:
        print("来啦3")
        st.session_state['story'] = choice

        st.button(st.session_state['options'][0],on_click=button_clicked,args=[0])
        st.button(st.session_state['options'][1],on_click=button_clicked,args=[1])

        # st.rerun()
        # st.empty()
        #container.empty()

def draw_story_image(history):
    # 这里应该根据故事历史生成图像
    # 示例返回一个本地图像文件
    return Image.open('path_to_your_image_file.jpg')

if __name__ == "__main__":
    container = st.container()
    global options
    if 'story' not in st.session_state:
        st.session_state['story'] = ''
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'knowledge' not in st.session_state:
        st.session_state['knowledge'] = ''
    if 'last_button_clicked' not in st.session_state:
        st.session_state.last_button_clicked = False
    if 'options' not in st.session_state:
        st.session_state['options'] = []

    #st.title('智谱AI助手')
    st.set_page_config(
        page_title="智谱AI助手",  # 页面标题
        page_icon=":rainbow:",  # icon
        layout="wide",  # 页面布局
    )

    user_input = st.text_input("请输入关键词以开始冒险：", key='key_words')

    response = get_dict(user_input)
    st.session_state['story'] = response['scene']
    st.session_state['options'] = [response['option_1'], response['option_2']]

    if st.session_state['story']:
        st.write(st.session_state['story'])
        print(st.session_state['story'])
    col1, col2 = st.columns(2)
    with col1:
        button1 = st.button(st.session_state['options'][0],on_click=button_clicked,args=[0])
    with col2:
        button2 = st.button(st.session_state['options'][1],on_click=button_clicked,args=[1])


