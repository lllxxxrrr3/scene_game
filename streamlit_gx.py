# #streamlit_env\Scripts\activate.bat
# #streamlit run streamlit_gx.py
#
# import streamlit as st
# from zhipuai import ZhipuAI  # 假设ZhipuAI已经正确导入
# #
# # 初始化ZhipuAI客户端，填写你的API密钥
# client = ZhipuAI(api_key='a13a4b4673179c29ce2d0edff7e91e36.858H7Zd4dUF9Mdb9')
#
# if 'stage' not in st.session_state:
#     st.session_state.stage = 0
#
# # 检查是否已经创建了session_state.history
# if 'history' not in st.session_state:
#     st.session_state.history = []
#
# def set_state(i):
#     st.session_state.stage = i
#     st.session_state.history = []
#
# def get_assistant_response(prompt):
#     # 使用zhipuai的API获取响应
#     response = client.chat.completions.create(
#         # assistant_id="659e54b1b8006379b4b2abd6",
#         model="glm-4-0520",
#         messages=[
#             {"role": "user", "content": "你好"},
#             {"role": "assistant", "content": "我是人工智能助手"},
#             {"role": "user", "content": "你叫什么名字"},
#             {"role": "assistant", "content": "我叫chatGLM"},
#             {"role": "user", "content": prompt}
#         ],
#         top_p= 0.7,
#         temperature= 0.95,
#         max_tokens=1024,
#         #stream=False,  # 这里设置为False，因为Streamlit不支持流式传输
#         # 其他参数...
#     )
#
#     answer = (dict(response.choices[0].message)["content"])
#     return answer
#
# st.title('智谱AI助手')
# if st.session_state.stage == 0:
#     st.button('开始', on_click=set_state, args=[1])
#
# if st.session_state.stage >= 1:
#     name = st.text_input('姓名', on_change=set_state, args=[2])
#     st.session_state.history.append(name)  # 添加姓名到历史记录
#
# if st.session_state.stage >= 2:
#     st.write(f'你好，{name}！')
#     st.button('输入查询', on_click=set_state, args=[3])
#
# while True:
#     if st.session_state.stage % 2 == 1 and st.session_state.stage > 2 :
#         # with st.form(key='my_form'):
#         prompt = st.text_input(label='请输入你的查询:', key='prompt')
#         st.session_state.history.append(prompt)  # 添加查询到历史记录
#         submitted = st.button('提交',on_click=set_state, args=st.session_state.stage+1 )
#
#     if st.session_state.stage % 2 == 0 and st.session_state.stage > 2 :
#         answer = get_assistant_response(prompt)
#         st.write('AI助手响应:', answer)
#         st.button('继续', on_click=set_state, args=st.session_state.stage+1)
#
#

import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key='a13a4b4673179c29ce2d0edff7e91e36.858H7Zd4dUF9Mdb9')

def get_assistant_response(prompt):
    # 使用zhipuai的API获取响应
    response = client.chat.completions.create(
        # assistant_id="659e54b1b8006379b4b2abd6",
        model="glm-4-0520",
        messages=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": prompt}
        ],
        top_p= 0.7,
        temperature= 0.95,
        max_tokens=1024,
        #stream=False,  # 这里设置为False，因为Streamlit不支持流式传输
        # 其他参数...
    )

    answer = (dict(response.choices[0].message)["content"])
    return answer

# 初始化session_state
if 'history' not in st.session_state:
    st.session_state.history = []

# 主页面标题
st.title('智谱AI助手')

# 创建一个空的容器，用于放置文本输入框、AI 响应和继续按钮
container = st.container()

# 如果历史记录为空，显示一个初始的提示信息
if len(st.session_state.history) == 0:
    container.write("请开始输入...")
else:
    # 显示历史记录中的所有输入和 AI 响应
    for index, (user_input, ai_response) in enumerate(st.session_state.history):
        container.write(f"输入 {index + 1}: {user_input}")
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
