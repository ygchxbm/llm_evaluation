import requests
import os
import time
import json
import hashlib


def completions_api(model, messages):
    uri = os.environ.get('LLM_EVALUATION_SERVER_CHATGPT_DOMAIN')
    secret = os.environ.get('LLM_EVALUATION_SERVER_CHATGPT_SECRET')
    app = os.environ.get('LLM_EVALUATION_SERVER_CHATGPT_APP')

    # Params is the same as openai
    params = {
        "model": model,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 1000,
        "n": 1,
        "presence_penalty": 1,
        "frequency_penalty": 1,
        # if stream is set to True, will receive streaming response
        # "stream": True,
        # model can be gpt-3.5-turbo (As default), gpt-4, gpt-4-32k, chat-bison-001 (Google Bard), ...
        # "model": "gpt-4"
    }

    timestamp = int(time.time())
    param_str = json.dumps({'params': params})
    src_str = f"{timestamp}{secret}{param_str}{timestamp}"
    signature_bytes = hashlib.sha256(src_str.encode('utf-8')).hexdigest().upper()

    headers = {"TIMESTAMP": str(timestamp), 'SIGNATURE': signature_bytes}
    # if you need to access api outside Tencent, you can change api-skynetyu.woa.com to momi.qq.com
    # when use api-skynetyu.woa.com, you can also choose http instead of https
    url = f'{uri}/api/pub_api.access?api=chatgpt.completions_api&app={app}'

    response = requests.post(url=url, data=param_str, headers=headers)
    if type(response) != requests.models.Response:
        return response.status_code, response.text, None
    if type(response) == str:
        return response.status_code, response.text, None
    if response.status_code != 200:
        return response.status_code, response.text, None

    result = response.json()
    if 'choices' in result:
        answer = result['choices'][0]['message']['content']
    elif 'result' in result:
        answer = result['result']
    else:
        print(response)
        return response.status_code, response.text, None

    return response.status_code, response.text, answer
