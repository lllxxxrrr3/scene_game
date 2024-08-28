import streamlit as st
from call_glm import call_glm, call_cogview
import re

st.set_page_config()

prompt_start = """
你是一个以解谜剧情为发展主线的互动游戏系统，让用户以第一人称视角体验。
主线任务会持续进行，是由不同的剧情结点接连构成的；支线任务是属性值点数的提高和获得相关道具，主线任务需要根据属性点值的大小对用户做出的选择进行分析，并作用于后续剧情的生成。
请注意:所有输出的内容要生成大括号并严格以json格式输出

现在是游戏开始阶段，以关键词：{key_words}剧情类型,生成游戏背景、主线任务,游戏背景要有大量的环境描写,人物描写,细节描写,并将故事完整叙述,文字要超过500字。
为除自玩家自己外的每一个故事中的人物编号，以及这个游戏系统的具体规则，和用户的初始属性点数值。
属性点包括：亲密值（对应不同人物），社会声望，智力，武力，敏捷度，健康值。
切记，设置合适的初始属性点！
然后向用户介绍游戏规则
“  1.你将担任旁白，叙述故事背景和内容
   2.玩家通过不同的选择控制剧情走向，不同的选择会有不同的属性点变化
   3.游玩过程中，玩家需进行解密回答问题，解开谜团
   4.玩家参加支线任务可以获得相关道具，辅助主线发展（但不是必须）
”

游戏由不同的每个剧情结点组成。每个剧情结点包括三类与用户的互动
你要给我生成一个固定的角色形象，
现在你已经生成了第一个剧情节点（就是你写的故事背景）,现在需要根据剧情推进主线任务,给出三个可供选择的选项,这三个选项要有较大的差异,以引起不同的后续
在必要时,剧情对一些特定环境或者工具进行专业解读,提高玩家的知识文化水平。例如古代的工具、历史遗迹、先进科技产品、著名的人物、著名的书籍、历史事件等
### 注意:在你的json中一定不要出现中文全角逗号,以中文输出。
请生成大括号并严格以以下json格式输出,不要生成注释:
    'scene':你创造的剧情背景,不要叙述人物的编号, 
    'character':角色形象,
    'rule':你给出的游戏规则,
    'knowledge':你搜索到的专业知识,
    'health':你为该人物设置的初始健康属性点,
    'reputation':你为该人物设置的初始社会声望属性点,
    'wisdom':你为人物设置的初始智力属性点,
    'strength':你为人物设置的初始武力值,
    'acuity':你为人物设置的初始敏捷度,
    'option_1':你给的选项1,
    'option_2':你给的选项2,
    'option_3':你给的选项3,
"""
prompt_section1 = """
你是一个以解谜剧情为发展主线的互动游戏系统，让用户以第一人称视角体验。
主线任务会持续进行，是由不同的剧情结点接连构成的；支线任务是属性值点数的提高和获得相关道具，主线任务需要根据属性点值的大小对用户做出的选择进行分析，并作用于后续剧情的生成。
请注意:所有输出的内容要生成大括号并严格以json格式输出

现有剧情为{plot},选择是{last_option},你需要接着这个剧情和选项往下推进。
现在的属性值为为：社会声望{attribute1}，智力{attribute2}，武力{attribute3}，敏捷度{attribute4}，健康值{attribute5},
现在需要推进主线剧情,主线任务要要有大量的环境描写,人物描写,细节描写,并将故事完整叙述,文字要超过500字。
### 注意:在你的json中一定不要出现中文全角逗号,以中文输出。
请生成大括号并严格以以下json格式输出:
    'scene':你创造的剧情背景,不要叙述人物的编号,
    'rule':你给出的游戏规则,
    'knowledge':你搜索到的专业知识,
    'health':该人物经历剧情之后的健康值,
    'reputation':该人物经历剧情之后的社会声望属性点,
    'wisdom':该人物经历剧情之后的智力属性点,
    'strength':该人物经历剧情之后的武力值,
    'acuity':该人物经历剧情之后的敏捷度,
    'option_1':你给的选项1,
    'option_2':你给的选项2,
    'option_3':你给的选项3,
"""
#生成支线任务
prompt_section2 = """
你是一个以解谜剧情为发展主线的互动游戏系统，让用户以第一人称视角体验。
主线任务会持续进行，是由不同的剧情结点接连构成的；支线任务是属性值点数的提高和获得相关道具，主线任务需要根据属性点值的大小对用户做出的选择进行分析，并作用于后续剧情的生成。

现有的剧情是:{plot},现在在主线任务中选择{last_option}
现在的属性值为为：社会声望{attribute1}，智力{attribute2}，武力{attribute3}，敏捷度{attribute4}，健康值{attribute5}。
你的任务是根据上述剧情的主线，设计与主线任务有关的支线任务,支线任务的完成方式是让玩家进行发言，对该任务进行初步处理，不要直接完成这个支线
注意：现在的属性值已经发生变化，请根据最新的属性点设计剧情
如果必要，剧情对一些特定环境或者工具进行专业解读，提高玩家的知识文化水平。例如古代的工具、历史遗迹、先进科技产品、著名的人物、著名的书籍、历史事件等，如果没有必要，则不生成,
以中文输出。

请生成大括号并严格的以以下的json格式输出:
    'scene':你设计的支线任务内容,
    'knowledge':你搜索到的专业解读,
    'option_1':你给的选项1,
    'option_2':你给的选项2,
    'option_3':你给的选项3,
    'health':该人物经历剧情之后的健康值,
    'reputation':该人物经历剧情之后的社会声望属性点,
    'wisdom':该人物经历剧情之后的智力属性点,
    'strength':该人物经历剧情之后的武力值,
    'acuity':该人物经历剧情之后的敏捷度,
"""
prompt_section3 = """
你是一个以解谜剧情为发展主线的互动游戏系统，让用户以第一人称视角体验。
主线任务会持续进行，是由不同的剧情结点接连构成的；支线任务是属性值点数的提高和获得相关道具，主线任务需要根据属性点值的大小对用户做出的选择进行分析，并作用于后续剧情的生成。

现有的剧情是:{plot},对于最新的支线任务，选择{last_option}，基于这个选择，对属性点进行修改，改变值为要合理，推进支线任务，设计一个小解密，以完成这个支线任务。
对于你给出的谜题,你要生成三个答案,一个正确的，两个迷惑的。
如果必要，剧情对一些特定环境或者工具进行专业解读，提高玩家的知识文化水平。例如古代的工具、历史遗迹、先进科技产品、著名的人物、著名的书籍、历史事件等，如果没有必要，则不生成,以中文输出。
请生成大括号并严格的以以下的json格式输出:
    'scene':你设计的解密内容,
    'knowledge':你搜索到的知识,
    'health':该人物经历剧情之后的健康值,
    'reputation':该人物经历剧情之后的社会声望属性点,
    'wisdom':该人物经历剧情之后的智力属性点,
    'strength':该人物经历剧情之后的武力值,
    'acuity':该人物经历剧情之后的敏捷度,
    'option_1':你为解密生成的答案,
    'option_2':你为解密生成的答案,
    'option_3':你为解密生成的答案,
"""
prompt_image = """
{scene}，用户选择的是{last_option}这是我给你的情景，主角的形象是{character}，请按照以上情景和角色形象生成一副动漫风格的图片。
注意：绘图时不要以人物为主，人物为辅助，主要是描述当前的环境！
"""

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
    st.write(1,st.session_state.game_state)
    if int(st.session_state.game_state) == -1:
        st.write(111111)
        prompt = prompt_start.format(key_words=st.session_state.key_words)
    elif int(st.session_state.game_state)%3 == 0:
        st.write(2222222)
        prompt = prompt_section1.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )
    elif int(st.session_state.game_state)%3 == 1:
        st.write(333333)
        prompt = prompt_section2.format(plot=st.session_state.plot,
                                        last_option=st.session_state.option[-1],
                                        attribute1=st.session_state.social_reputation,
                                        attribute2=st.session_state.wisdom,
                                        attribute3=st.session_state.strength,
                                        attribute4=st.session_state.acuity,
                                        attribute5=st.session_state.health,
                                        )  # Add last_words if applicable
    elif int(st.session_state.game_state)%3 == 2:
        st.write(44444)
        prompt = prompt_section3.format(plot=st.session_state.plot,last_option=st.session_state.option[-1],)  # If game_state 3, fallback to prompt_section1
    else:
        prompt = prompt_start.format(key_words=st.session_state.key_words)

    # 调用API获取响应
    response_text = call_glm(prompt=prompt, model='glm-4')
    print(f'raw_text{response_text}')

    # 处理JSON
    pattern = r'({[^}]*})'
    matches = re.findall(pattern, response_text)
    response_info = matches[0].replace('\n', '')
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
        #生成图片
        image = call_cogview(prompt=prompt_image.format(scene = st.session_state.scene[-1],
                                                last_option = st.session_state.option[-1] if len(st.session_state.option)>0 else '',
                                                character = st.session_state.character))
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
    st.write(2,st.session_state.game_state)
    st.write("count",st.session_state.count)
    for i in range(st.session_state.count):
        # 显示当前场景
        print(i)
        if int(i)%3 == 1:
            st.write(f"【主线剧情】:{st.session_state.scene[i]}")
        elif int(i)%3 == 2:
            st.write(f"【支线剧情】:{st.session_state.scene[i]}")
        elif int(i)%3 == 0 and i != 0:
            st.write(f"【解谜剧情】:{st.session_state.scene[i]}")
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
