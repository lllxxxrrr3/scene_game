import streamlit as st
from call_glm import call_glm, call_cogview
from prompt import prompt_start, prompt_section1, prompt_image, prompt_section2
import re

st.set_page_config()


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
    st.write(1, st.session_state.game_state)
    if int(st.session_state.game_state) == -1:
        st.write(111111)
        prompt = prompt_start.format(key_words=st.session_state.key_words)
    elif int(st.session_state.game_state) % 2 == 0:
        st.write(2222222)
        prompt = prompt_section1.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )
    elif int(st.session_state.game_state) % 2 == 1:
        st.write(333333)
        prompt = prompt_section2.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )  # Add last_words if applicable

    else:
        prompt = prompt_start.format(key_words=st.session_state.key_words)

    # 调用API获取响应
    response_text = call_glm(prompt=prompt, model='glm-4')
    print(f'raw_text{response_text}')

    # 处理JSON
    pattern = r'({[^}]*})'
    matches = re.findall(pattern, response_text)
    response_info = matches[0].replace('\n', '') \
        .replace('，', ',') \
        .replace('！', '!') \
        .replace('？', '?') \
        .replace('：', ':') \
        .replace('；', ';') \
        .replace('（', '(') \
        .replace('）', ')') \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('‘', "'") \
        .replace('’', "'") \
        .replace('——', '-') \
        .replace('…', '...')
    response_text = eval(response_info.strip())
    print(f'final_text{response_text}')
    if int(st.session_state.game_state) == -1:
        st.session_state.character = response_text["character"]
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
        image = call_cogview(prompt=prompt_image.format(scene=st.session_state.scene[-1],
                                                        last_option=st.session_state.option[-1] if len(
                                                            st.session_state.option) > 0 else '',
                                                        character=st.session_state.character))
        st.session_state.image.append(image)
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

    # 更新互动类型（问答为1/选择为0）
    if response_text.get("answer_type"):
        st.session_state.answer_type = response_text.get("answer_type")

    return response_text


def display_scene_with_options():
    """
    用于在 Streamlit 应用中展示生成的游戏场景，并处理用户的选择。
    """
    st.write(2, st.session_state.game_state)
    st.write("count", st.session_state.count)
    for i in range(st.session_state.count):
        # 显示当前场景
        print(i)
        if int(i) % 2 == 1:
            st.write(f"【主线剧情】:{st.session_state.scene[i]}")
        elif int(i) % 2 == 0 and i != 0:
            st.write(f"【支线剧情·解密】:{st.session_state.scene[i]}")

        else:
            st.write(st.session_state.scene[i])
        st.image(st.session_state.image[i])
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
                # 如果用户尚未做出选择，显示选项按钮或文本输入框
                if st.session_state.game_state == 3:
                    if st.session_state.answer_type == 0:  # 选择类型
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button(f'{st.session_state.option_1[i]}', on_click=choose_1, key=f'b1_{i}')
                        with col2:
                            st.button(f'{st.session_state.option_2[i]}', on_click=choose_2, key=f'b2_{i}')
                        with col3:
                            st.button(f'{st.session_state.option_3[i]}', on_click=choose_3, key=f'b3_{i}')
                    elif st.session_state.answer_type == 1:  # 问答类型
                        words = st.text_input("请输入你的回答", key=f'last_words_{i}')
                        if st.button("确认", key=f'confirm_{i}'):
                            st.session_state.option.append(words)
                            st.session_state.last_choice = words
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
    st.sidebar.title("Character Attributes")
    st.sidebar.markdown(f"**Social Reputation**: {st.session_state.social_reputation}")
    st.sidebar.markdown(f"**Wisdom**: {st.session_state.wisdom}")
    st.sidebar.markdown(f"**Strength**: {st.session_state.strength}")
    st.sidebar.markdown(f"**Acuity**: {st.session_state.acuity}")
    st.sidebar.markdown(f"**Health**: {st.session_state.health}")

    # 显示各人物之间的cohesion


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
key_word = st.text_input("请输入关键词", key='key_words')
print(st.session_state.game_state)
if st.session_state.confirm == True or st.button("确定"):
    st.session_state.confirm = True
    # if st.session_state.count == 0:
    #     response_data = get_dict()
    #     display_sidebar()
    #     display_scene_with_options()
    # elif st.session_state.game_state == 0:
    #     response_data = get_dict()
    #     display_sidebar()
    #     display_scene_with_options()
    # elif st.session_state.game_state == 1:
    response_data = get_dict()
    display_sidebar()
    display_scene_with_options()
