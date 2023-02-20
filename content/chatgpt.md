Title: GPT
Date: 2023-02-20
Category: Analytics
Tags: ML
Author: Yoga


版本 | 发布时间 | 训练方案 | 参数量 | 是否开放接口
| - | - | - | - | - |
GPT(GPT-1) | 2018 年 6 月 | 无监督学习 | 1.17 亿 | 是
GPT-2 | 2019 年 2 月 | 多任务学习 | 15 亿 | 是
GPT-3 | 2020 年 5 月 | 海量参数 | 1,750 亿 | 是
ChatGPT(GPT-3.5) | 2022 年 12 月 | 针对对话场景优化 | 1,750 亿 | 否
GPT-4 | 未发布 | 万亿参数 | 100万亿 | 否

https://blog.csdn.net/hekaiyou/article/details/128303729


```python
def chat(prompt):
  try:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt= prompt,
      temperature=0.9,
      max_tokens=2500,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
      stop=[" Human:", " AI:"]
    )

    answer = response["choices"][0]["text"].strip()
    return answer
  except Exception as exc:
    return "broken"
```

* model: 要使用的模型的 ID，Ada / Babbage / Curie / Davinci
* prompt: 生成结果的提示文本，即你想要得到的内容描述
* max_tokens: 生成结果时的最大 tokens 数，不能超过模型的上下文长度
* temperature: 控制结果的随机性，0.0为固定结果

计价：
1000 tokens(750 words) $0.02 (prompt+completion 提问+回答总字数)
