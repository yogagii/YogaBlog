Title: GPT
Date: 2023-02-20
Category: Analytics
Tags: ML
Author: Yoga


版本 | 发布时间 | 训练方案 | 参数量 | 模型
| - | - | - | - | - |
GPT(GPT-1) | 2018 年 6 月 | 无监督学习 | 1.17 亿 |
GPT-2 | 2019 年 2 月 | 多任务学习 | 15 亿 |
GPT-3 | 2020 年 5 月 | 海量参数 | 1,750 亿 | text-curie-001, text-babbage-001, text-ada-001, davinci
ChatGPT(GPT-3.5) | 2022 年 12 月 | 针对对话场景优化 | 1,750 亿 | text-davinci-003, text-davinci-002, gpt-3.5-turbo
GPT-4 | 未发布 | 万亿参数 | 100万亿 |

https://blog.csdn.net/hekaiyou/article/details/128303729

### 模型使用

https://platform.openai.com/docs/api-reference/models

基础模型 | Desc | Use cases
| - | - | -
davinci 达芬奇 | Most capable GPT-3 model. Most powerful | 文本摘要
curie 居里 | Very capable, but faster and lower cost than Davinci. | 翻译，分类，文本情感分类
babbage 巴贝奇 | Capable of straightforward tasks, very fast, and lower cost. | 语义搜索semantic search
ada | The fastest model in the GPT-3 series, and lowest cost. | 分类，地址提取，关键词

从上往下：模型越小，能力越差，价钱越低，响应速度越快

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
* max_tokens: （16）生成结果时的最大 tokens 数，不能超过模型的上下文长度
* temperature: （1）控制结果的随机性，0.0为固定结果
* suffix: （null）completion后缀
* top_p：（1）和temperature二选一，具有top_p概率质量的标记的结果
* n：（1）每个prompt生成的completion数量
* stream：（false）是否回流部分进度
* logprobs：（null）api返回最可能token数量
* echo：（false）返回completion + prompt
* stop：（null）遇到停止生成token
* presence_penalty：（0）根据现有出现惩罚来降低重复
* frequency_penalty：（0）根据现有频率惩罚来降低重复
* best_of：（1）产生最佳completion个数
* logic_bias：（null）指定token在completion中出现的概率
* user：终端用户唯一标识符

### 模型训练

数据集准备：原文 – 摘要 （几百个）

基础模型：4选1，可不断迭代

* training_file：上传的训练数据文件ID。
* validation_file：验证数据的上传文件的ID。
* model：（curie）基础模型
* n_epochs：（4）训练模型的epoch数
* batch_size：（null）批大小是用于训练单个向前和向后传递的训练示例的数量，默认训练集 0.2%
* learning_rate_multiplier：（null）用于训练的学习率乘数。
* prompt_loss_weight：（0.01）The weight to use for loss on the prompt tokens. 
* compute_classification_metrics：（false）If set, we calculate classification-specific metrics such as accuracy and F-1 score using the validation set at the end of every epoch.  
* classification_n_classes：（null）分类任务的类数量
* classification_positive_class：（null）二元分类中的正类
* classification_betas：（null）F-beta scores
* suffix：（null）模型名后缀

可训练判别器模型，当提问范围超出数据集，回答"No sufficient context for answering the question"

When the question was not generated on the context, the model will be prompted to answer "No sufficient context for answering the question". We will also train a discriminator model, which predicts whether the question can be answered based on the context or not.

### 计价

1000 tokens(750 words) $0.02 (prompt+completion 提问+回答总字数)

模型 | 基础模型 使用 |训练模型 | 训练后使用
| - | - | - | -
text-davinci-003 | $0.02 | $0.03 | $0.12
text-curie-001 | $0.002 | $0.003 | $0.012
text-babbage-001 | $0.0005 | $0.0006 | $0.012
text-ada-001 | $0.0004 | $0.0004 | $0.0016

视频时长 | 原文字数 | 耗时 | 基本模型费用 | 训练模型费用
| - | - | - | - | -
1小时 | 20000 中文字符 | 5-10min | (20000+10000)x2 / 1000x0.02 =$1.2 | 20000*2/1000*0.12 =$4.8 (不包括训练产生费用)

_基本模型费用 =(prompt+completition) *$0.02_

_训练模型费用 =训练数据量*$0.03 + prompt*$0.12_

### Speech to text

Whisper is a general-purpose speech recognition model. The Whisper v2-large model is currently available through API with the whisper-1 model name.

* Transcription
```python
import openai
audio_file= open("/path/to/file/audio.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
```
限制： 25 MB，mp3, mp4, mpeg, mpga, m4a, wav, and webm.

* Translation
```python
transcript = openai.Audio.translate("whisper-1", audio_file)
```
只支持翻译成英语

https://platform.openai.com/docs/guides/speech-to-text

```bash
pip install -U openai-whisper

whisper japanese.wav --language Japanese
```

https://github.com/openai/whisper#available-models-and-languages

---

## Azure OpenAI

### 使用场景
* Content Generation
    * Automatically generate responses to customer inquries
    * Generate personalised UI for your website
* Sumarization
    * Summary of customer support conversation logs
    * Subject Matter Exper Document Summarization (financial reporting / analyst articles)
    * Social Media trends summarization
* Code generation
    * Convert natural language to SQL for telemetry data
    * Convert natural languate to Query proprietary data models
    * code documentation
* Semantic Search
    * Search reviews for a specific product / service
    * information discovery and knowledge mining

\ | OpenAI | Azure OpenAI
| - | - | -
版本 | GPT3.5 | GPT3.0 (DALL·E preview / ChatGPT comming soon)
Rate limit | TPM (tokens per minute) API调用限制，对企业级大用户量，一分钟头几秒用完TPM，后面几秒无TPM可用 | 
Data safety | customer-to-OpenAI requests and responses are encrypted | 符合企业安全性 合规性

### Document Process Automation:

Documents (PDF) -> Azure Form Recognizer -> Azure Cognitive Search -> Azure OpenAI Service -> Cosmos DB -> Web Application / PowerBI

### Contact Center Analytics

Telephony Server -> Azure Storage (Audio Files) -> Speech-to-Text -> Azure OpenAI Service -> PowerBI Insights (conversion trends& insights) / CRM (detailed call history incl. summaries, call reasons)

### OpenAI Fine-tuning

Azure OpenAI Studio -> Create customized model -> Upload training data -> Import validation data

不是数据集越多越好，训练越多反而影响了原本模型效果

对于企业内部应用：
通过 Hyperparams: Top base prompt 最高指示：拒绝回答无关问题

---

## DALL·E 2 图像生成

* Generate an infinite number of images with simple text prompts
* Accelerate designs or inspire creative decision
* Build capability into enterprise applications through APls and SDKs

Microsoft Designer: https://designer.microsoft.com
