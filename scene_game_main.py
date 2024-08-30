import streamlit as st
from call_glm import call_glm, call_cogview
import re
from prompt import prompt_image, prompt_section1, prompt_section2, prompt_start, prompt_end
import base64

st.set_page_config(page_title="迷旅小游戏",
                   page_icon=':smiley:',
                   layout='wide',
                   initial_sidebar_state='expanded')

if "ready" not in st.session_state:
    st.session_state.ready = 0  # 设置健康初始值

with st.sidebar:
    st.write("欢迎,请选择您想要的BGM")
    tab1, tab2, tab3 = st.tabs(["无", "轻快", "紧张"])
    with tab2:
        # 提供音频文件
        audio_file = open(r'D:\Download\llama3\peace.mp3', 'rb')
        audio_bytes = audio_file.read()
        audio_base_2 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio id="audio2" controls autoplay loop>
                <source src="data:audio/mp3;base64,{audio_base_2}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    with tab3:
        # 提供音频文件
        audio_file3 = open(r'D:\Download\llama3\tension.mp3', 'rb')
        audio_bytes3 = audio_file3.read()
        audio_base_3 = base64.b64encode(audio_bytes3).decode()
        audio_html3 = f"""
            <audio id="audio3" controls autoplay loop>
                <source src="data:audio/mp3;base64,{audio_base_3}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html3, unsafe_allow_html=True)

if st.session_state.ready == 0:
    st.markdown("""
    您好！感谢您访问我们设计的小游戏——迷旅。
    希望能您带来非凡的游戏体验！
    ---

    ### 🌟 游戏类型选择
    在开始冒险之前，请输入您希望体验的剧情类型关键词，如·：
    - 科幻 - 古代 - 现代 - 喜剧

    ### 初始属性点
    - 社会声望：？ - 智力：？ - 武力：？ - 健康值：？

    ### 游戏规则
    1. **游戏背景**：游戏设定在一个充满谜团的世界中，您将以第一人称视角体验一段非凡的冒险旅程。
    2. **故事叙述**：旁白将叙述故事背景和内容，包括丰富的环境、人物和细节描写。
    3. **玩家选择**：您将通过不同的选择控制剧情走向，每个选择都会影响您的属性点。
    4. **解密任务**：在游玩过程中，您需要解密回答问题，解开谜团。

    ### 知识与文化
    在您的冒险中，您将接触到各种专业知识，提高您的文化水平，包括但不限于：
    - 古代工具 - 历史遗迹  - 先进科技产品

    ### 🛠️ 开源项目

    -如果您对我们的开源项目感兴趣，请访问我们的GitHub仓库：[GitHub](https://github.com/lllxxxrrr3/scene_game/)
    ---

    ### 🚀 正式开始游戏
    你准备好开启你的冒险了吗？一旦确认，我们将正式开始游戏。
    请确认您已阅读并理解以上规则，然后点击下面的按钮开始游戏。

    """, unsafe_allow_html=True)


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


def choose_3():
    st.session_state.choose_3 = True
    st.session_state.option.append(st.session_state.option_3[-1])
    st.session_state.chosen_options.append(3)


def get_dict():
    # 根据游戏状态选择合适的prompt
    if int(st.session_state.game_state) == -1:
        prompt = prompt_start.format(key_words=st.session_state.key_words)
    elif int(st.session_state.game_state) % 3 == 0:
        prompt = prompt_section1.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )
    elif int(st.session_state.game_state) % 3 == 1:
        prompt = prompt_section1.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )  # Add last_words if applicable
    elif int(st.session_state.game_state) % 3 == 2:
        prompt = prompt_section2.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )
    else:
        prompt = prompt_start.format(key_words=st.session_state.key_words)

    # 调用API获取响应
    response_text = call_glm(prompt=prompt, model='glm-4')
    print(f'raw_text{response_text}')

    # 处理JSON
    pattern = r'({[^}]*})'
    matches = re.findall(pattern, response_text)
    response_info = matches[0].replace('\n', '').replace('，', ',')
    response_text = eval(response_info.strip())
    print(f'final_text{response_text}')
    if int(st.session_state.game_state) == -1:
        st.session_state.character = response_text["character"]
        st.session_state.count_end = response_text["count_end"]
    # 更新scene到st.session_state.plot
    new_scene = response_text.get("scene", "")
    if new_scene:
        # 更新剧情历史记录
        st.session_state.plot += f"\n{new_scene}"
        # 更新剧情
        st.session_state.scene.append(response_text["scene"])

        # 更新状态
        st.session_state.count += 1
        # 生成图片
        # image = call_cogview(prompt=prompt_image.format(plot = st.session_state.plot,
        #                                         scene = st.session_state.scene[-1],
        #                                         last_option = st.session_state.option[-1] if len(st.session_state.option)>0 else '',
        #                                         character = st.session_state.character))
        # st.session_state.image.append(image)
    # 更新人物属性
    st.session_state.social_reputation = response_text.get("reputation", 0)
    st.session_state.wisdom = response_text.get("wisdom", 0)
    st.session_state.strength = response_text.get("strength", 0)
    st.session_state.acuity = response_text.get("acuity", 0)
    st.session_state.health = response_text.get("health", 0)
    st.session_state.knowledge.append(response_text.get("knowledge", ""))

    # 更新game_state
    st.session_state.game_state += 1

    # 更新选项
    st.session_state.option_1.append(response_text["option_1"])
    st.session_state.option_2.append(response_text["option_2"])
    st.session_state.option_3.append(response_text["option_3"])
    return response_text


def display_scene_with_options():
    """
    用于在 Streamlit 应用中展示生成的游戏场景，并处理用户的选择。
    """
    for i in range(st.session_state.count):
        # 显示当前场景
        print(i)
        if int(i) % 3 == 1:
            st.write(f"【主线剧情】:{st.session_state.scene[i]}")
        elif int(i) % 3 == 2:
            st.write(f"【主线剧情】:{st.session_state.scene[i]}")
        elif int(i) % 3 == 0 and i != 0:
            st.write(f"【解谜剧情】:{st.session_state.scene[i]}")
        else:
            st.write(st.session_state.scene[i])
        # st.image(st.session_state.image[i])
        with st.container():
            if i < len(st.session_state.chosen_options):
                # 如果用户已经选择了某个选项，展示选择的结果
                if st.session_state.chosen_options[i] == 1:
                    with st.container():
                        st.success(f"你选择了: {st.session_state.option_1[i]}")
                elif st.session_state.chosen_options[i] == 2:
                    with st.container():
                        st.success(f"你选择了: {st.session_state.option_2[i]}")
                elif st.session_state.chosen_options[i] == 3:
                    with st.container():
                        st.success(f"你选择了: {st.session_state.option_3[i]}")

                # todo 如果有相关知识，显示在选择内容的下方
                if st.session_state.knowledge[i]:
                    with st.container():
                        st.info(f"相关知识: {st.session_state.knowledge[i]}")
            else:
                if st.session_state.count == st.session_state.count_end:
                    if_end()
                else:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.button(f'{st.session_state.option_1[i]}',
                                  on_click=choose_1, key=f'b1_{i}')
                    with col2:
                        st.button(st.session_state.option_2[i],
                                  on_click=choose_2, key=f'b2_{i}')
                    with col3:
                        st.button(st.session_state.option_3[i],
                                  on_click=choose_3, key=f'b3_{i}')


def display_sidebar():
    st.sidebar.markdown("<style>.SR, .W, .S, .A, .H{font-size:24px; font-weight: bold;}</style>",
                        unsafe_allow_html=True)
    st.sidebar.title("角色属性")
    st.sidebar.markdown(f"<p class='SR'>**社会声望**: {st.session_state.social_reputation}</P>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='W'>**智力**: {st.session_state.wisdom}</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='S'>**武力值**: {st.session_state.strength}</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='A'>**敏捷度**: {st.session_state.acuity}</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='H'>**健康**: {st.session_state.health}</p>", unsafe_allow_html=True)


def if_end():
    prompt = prompt_end.format(plot=st.session_state.plot, character=st.session_state.character)
    response_text = call_glm(prompt=prompt, model='glm-4')
    pattern = r'({[^}]*})'
    matches = re.findall(pattern, response_text)
    response_info = matches[0].replace('\n', '')
    response = eval(response_info.strip())

    st.session_state.scene.append(response["scene"])
    st.write(st.session_state.scene[-1])
    st.markdown("# 结束 🎉")
    st.balloons()


if "key_words" not in st.session_state:
    st.session_state.key_words = ""  # 默认初始状态

if "game_state" not in st.session_state:
    st.session_state.game_state = -1  # 默认初始状态
if 'confirm' not in st.session_state:
    st.session_state.confirm = False
if "scene" not in st.session_state:
    st.session_state.scene = []
if "option_1" not in st.session_state:
    st.session_state.option_1 = []
if "option_2" not in st.session_state:
    st.session_state.option_2 = []
if "option_3" not in st.session_state:
    st.session_state.option_3 = []
if "option" not in st.session_state:
    st.session_state.option = []
if "knowledge" not in st.session_state:
    st.session_state.knowledge = []
if "choose_1" not in st.session_state:
    st.session_state.choose_1 = False
if "choose_2" not in st.session_state:
    st.session_state.choose_2 = False
if "choose_3" not in st.session_state:
    st.session_state.choose_3 = False
if "chosen_options" not in st.session_state:
    st.session_state.chosen_options = []
if "count" not in st.session_state:
    st.session_state.count = 0
if "count_end" not in st.session_state:
    st.session_state.count_end = 0
if "plot" not in st.session_state:
    st.session_state.plot = ""
if "image" not in st.session_state:
    st.session_state.image = []
if "character" not in st.session_state:
    st.session_state.character = ''
if 'answer_type' not in st.session_state:
    st.session_state.answer_type = 0
if "social_reputation" not in st.session_state:
    st.session_state.social_reputation = 0  # 设置社会声望初始值

if "wisdom" not in st.session_state:
    st.session_state.wisdom = 0  # 设置智力初始值

if "strength" not in st.session_state:
    st.session_state.strength = 0  # 设置武力初始值

if "acuity" not in st.session_state:
    st.session_state.acuity = 0  # 设置敏捷度初始值

if "health" not in st.session_state:
    st.session_state.health = 0  # 设置健康初始值

if "cohesion" not in st.session_state:
    st.session_state.cohesion = {}  # 设置与各人物的亲密度初始值为字典

# main

if st.button("我准备好了，开始冒险！"):
    st.write("游戏正式开始，祝您好运！")
    st.session_state.ready = 1
if st.session_state.ready:
    key_word = st.text_input("请输入关键词", key='key_words')
    print(st.session_state.game_state)
    if st.session_state.confirm == True or st.button("确定"):
        st.session_state.confirm = True
        response_data = get_dict()
        display_sidebar()
        display_scene_with_options()
