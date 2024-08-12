from zhipuai import ZhipuAI
from API import API_KEY

def glm_chat(prompt,)


client = ZhipuAI(api_key="0ef06f9a519edbc03c207a4541d52cb6.MGeS4f3AKYiMQdQ7")  # 填写您自己的APIKey
response = client.chat.completions.create(
    model="charglm-3",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为智谱开放平台创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ],
)
print(response.choices[0].message)
