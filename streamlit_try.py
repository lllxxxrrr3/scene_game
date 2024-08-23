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
接着上面的剧情，玩家做出的选择是{option}，请根据选择和上面的情景接着
描述出故事下一步的发展，并重新生成两个选项。
注意：
1，记住上面游戏的轮数，使游戏对话大约在10-15轮结束
2，在故事的生成中，如果有涉及一些物理学或者生物学等知识，可以上网搜集相关的知识内容，并告诉我.
3,在结束时，给我一个完美的结局，并且告诉我是否结束。
4，请生成大括号并严格的以以下的json格式输出：
    scene:你创造的情景,
    option_1:你给的选项1,
    option_2:你给的选项2，
    knowledge:你搜索到的知识,
    end：是否结束，你只用输出True或False
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

def get_dict(key_words):
    if len(st.session_state['story'])==0:
        response_text = get_assistant_response(prompt_start.format(key_words=key_words))
    else:
        print(key_words)
        response_text = get_assistant_response(prompt_next.format(choice=key_words))
    response_text = response_text.replace("`", "").replace("json", "")
    try:
        response_dict = json.loads(response_text)
    except json.JSONDecodeError:
        response_dict = {}  # 或者进行适当的错误处理
    return response_dict

def set_state(i):
    st.session_state.stage = i

# 更新故事的函数
def update_story(choice):

    response_next=get_dict(st.session_state['choice'])
    st.session_state['story'] = response_next['scene']
    if st.session_state['story']:
        st.write(st.session_state['story'])

    st.session_state['history'].append((st.session_state['story'], choice))

    if "结束" in choice:
        st.markdown("# 结束 🎉")
        print("结束")
        st.session_state['story'] = ''
        st.session_state['history'] = []
    else:
        st.session_state['story'] = choice
        #st.rerun()
        #st.empty()


def streamlit_main():

    if 'story' not in st.session_state:
        st.session_state['story'] = ''
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    st.title('智谱AI助手')

    user_input = st.text_input("请输入关键词以开始冒险：", key='key_words')

    if user_input and st.session_state.stage >= 1:
        with st.spinner('Generating response...'):
            response = get_dict(user_input)
            st.session_state['story'] = response['scene']
            options = [response['option_1'], response['option_2']]

            if st.session_state['story']:
                st.write(st.session_state['story'])
            col1, col2 = st.columns(2)
            with col1:
                button1 = st.button(options[0], key='button1')
            with col2:
                button2 = st.button(options[1], key='button2')

    if button1:
        choice = options[0]
        update_story(choice)

    if button2:
        choice = options[1]
        update_story(choice)

    if st.session_state['history']:
        # 在网页上显示对话历史和生成的响应
        for index, (choice, st.session_state['story']) in enumerate(st.session_state['history']):
            st.write(f"选择 {index + 1}: {choice}")
            st.write(f"AI 响应: {st.session_state['story']}")



# 运行Streamlit主函数
if __name__ == "__main__":

    streamlit_main()
