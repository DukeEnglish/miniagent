'''
Descripttion: 
Author: Duke 叶兀
E-mail: ljyduke@gmail.com
Date: 2024-01-06 12:55:46
LastEditors: Duke 叶兀
LastEditTime: 2024-01-18 02:13:18
'''
import logging
from zhipuai import ZhipuAI
from config import GLM_API_KEY


class GLMService():
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey

    def llm(self, user_input="推荐中国自驾游路线"):

        response = self.client.chat.completions.create(
            # model="glm-4",  # 填写需要调用的模型名称
            model="GLM-3-Turbo",
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=False,
        )
        res = response.choices[0].message.content
        logging.info(f"yi_single_service' resp is {res}")
        return res

    def llm_stream(self, user_input='推荐中国自驾游路线'):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if not content:
                continue

            yield content


glm_client = GLMService(GLM_API_KEY)

if __name__ == '__main__':
    glm = GLMService(GLM_API_KEY)
    res = glm.llm(user_input='你好，你是谁')
    print(res)
    res = glm.llm_stream(user_input='你好')
    for i in res:
        print(i)
        print()
