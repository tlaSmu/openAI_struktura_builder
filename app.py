import openai
import pandas as pd
import json
from slugify import slugify


def get_attractive_headline(cluster):
  '''запит для отримання заголовку h1/title'''

  order = f"\n\nWrite an attractive headline for the article about  \"{cluster}\"."
  prompt = keywords+order
  openai.api_key = "XXXXXXXXXXXXXXXXXXXXX" #openAI key

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response['choices'][0]['text'].split('\n')


def get_structure(cluster):
  '''запит для отримання структури'''

  order = f"\n\nMake a heading content structure for an article about \"{cluster}\", without Heading, only structure"
  prompt = keywords+order
  openai.api_key = "XXXXXXXXXXXXXXXXXXXXX" #openAI key

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response['choices'][0]['text'].split('\n')

def get_faqs(keywords):
  '''запит для отримання списку FAQs'''

  order = f"\n\nAdd 5 FAQs using the unique phrases above, no answers, only questions."
  prompt = keywords+order
  openai.api_key = "XXXXXXXXXXXXXXXXXXXXX" #openAI key

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response['choices'][0]['text'].split('\n')

data = {}
dataFrame = pd.read_csv("keywords.csv")
clusters = dataFrame['cluster'].unique() # унікалізовую кластери

for cluster in clusters:
  print(f'Start for {cluster}')

  rr = dataFrame[dataFrame['cluster'].str.contains(cluster)] # формую список ключових фраз по кластеру
  keywords = '\\n'.join(rr['keywords'])
  
  data['headline'] = get_attractive_headline(cluster)[2:]    # заголовок майбутньої статті
  data['structure'] = get_structure(cluster)[2:]             # структура статті
  data['faq'] = get_faqs(keywords)[2:]                       # список faqs   

  file_name = slugify(data['headline'][0])                   # назва json файлу

  json_object = json.dumps(data, indent=4)                   # формую файл
  with open(f"result/{file_name}.json", "w") as outfile:
      outfile.write(json_object)

