#streamlit_env\Scripts\activate.bat
#streamlit run streamlit_gx.py

import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key='a13a4b4673179c29ce2d0edff7e91e36.858H7Zd4dUF9Mdb9')

prompt_start = """
简介：一键生成关键词驱动的冒险故事，三轮选择决定结局，体验定制化冒险旅程！
你是关键词冒险，你是一个创造性的故事编织者，通过用户输入的关键词构建情景和角色，并提供两个选项引导故事发展。你的能力有:
- 分析关键词，构建情景和角色；
- 根据用户选择，推进故事情节；
- 在第三轮结束时，设置故事结局；
- 如涉及专业知识，上网搜集相关内容。
以下是关键词和输出形式
关键词：{key_words}
请生成大括号并严格以以下json格式输出：
    scene:你创造的情景,以及两个选择
"""

def get_assistant_response(prompt):
    # 使用zhipuai的API获取响应
    response = client.chat.completions.create(
        # assistant_id="66c6f56d337ddf725b9221e5",
        model="glm-4-0520",
        messages=[
            {"role": "user", "content": prompt}
        ],
        top_p= 0.7,
        temperature= 0.95,
        max_tokens=1024,
        # stream=False,  # 这里设置为False，因为Streamlit不支持流式传输
        # attachments=None,
        # metadata=None
        # 其他参数...
    )

    answer = (dict(response.choices[0].message)["content"])
    return answer

def get_dict(key_words):
    # st.text_input('请输入创建场景的关键词',key='key_words')
    response_text = get_assistant_response(prompt=prompt_start.format(key_words=key_words))
    print(response_text)
    response_text = response_text.replace("`","").replace("json","")
    response_text = eval(response_text)
    return response_text

# 初始化session_state
if 'history' not in st.session_state:
    st.session_state.history = []

# 主页面标题
st.title('智谱AI助手')

st.text_input("请输入关键词", key='key_words')

input_text = get_dict(st.session_state['key_words'])
st.write(input_text['scene'])

# 创建一个空的容器，用于放置文本输入框、AI 响应和继续按钮
container = st.container()

# 如果历史记录为空，显示一个初始的提示信息
if len(st.session_state.history) == 0:
    container.write("请开始你的选择...")
else:
    # 显示历史记录中的所有输入和 AI 响应
    for index, (user_input, ai_response) in enumerate(st.session_state.history):
        container.write(f"选择 {index + 1}: {user_input}")
        container.write(f"AI 响应: {ai_response}")

# 创建一个表单，用于接收用户的新输入
with st.form(key='input_form'):
    # 创建一个文本输入框
    input_text = st.text_input('输入文本', key=f'input_{len(st.session_state.history)}')

    # 创建一个提交按钮
    submit_button = st.form_submit_button('发送')

    # 当用户点击提交按钮时，获取 AI 助手的响应并将输入和响应添加到历史记录中
    if submit_button:
        if input_text:  # 确保输入不为空
            ai_response = get_assistant_response(input_text)
            st.session_state.history.append((input_text, ai_response))
            # 清除输入框中的内容
            st.rerun()
