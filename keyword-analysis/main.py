from sqlalchemy import create_engine, text
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import jieba
from typing import List
import re
import json

# 替换成你的数据库连接
DB_URL = "mysql+pymysql://root:admin123@localhost:3306/dora?charset=utf8mb4"

# 连接数据库
engine = create_engine(DB_URL)

def get_stop_words() -> list[str]:
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
def is_valid_token(token: str) -> bool:
    # 过滤空白、纯符号、单字符、乱码等
    return (
        len(token) > 1 and
        not re.match(r'^[^\u4e00-\u9fa5a-zA-Z]+$', token) and  # 纯符号或乱码
        not re.match(r'^\d+$', token) and                      # 全是数字
        not re.search(r'[Ａ-Ｚａ-ｚ]', token)                  # 全角字符（乱码）
    )
    
def is_valid_token(token: str) -> bool:
    # 过滤空白、纯符号、单字符、乱码等
    return (
        len(token) > 1 and
        not re.match(r'^[^\u4e00-\u9fa5a-zA-Z]+$', token) and  # 纯符号或乱码
        not re.match(r'^\d+$', token) and                      # 全是数字
        not re.search(r'[Ａ-Ｚａ-ｚ]', token)                  # 全角字符（乱码）
    )

def fetch_latest_posts(limit=1000) -> list[str]:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT content FROM posts ORDER BY published_at DESC LIMIT :limit"),
            {"limit": limit}
        )
        return [row[0] for row in result if row[0]]  # 过滤空内容

# 定义自定义分词器，使用 jieba 进行分词
def chinese_tokenizer(text: str) -> List[str]:
  words = jieba.lcut(text)
  filter_words = []
  for word in words:
    word = word.strip()
    word = re.sub(r'[a-zA-Z0-9]', '', word)
    if len(word) <= 1:
      continue
    filter_words.append(word)
  return filter_words

# gram 数
GRAM = 1
contents = fetch_latest_posts()
corpus = []
for content in contents:
  content = str(content)
  if content.strip() and len(content) > 3:
    corpus.append(content)

vectorizer = TfidfVectorizer(
  stop_words=get_stop_words(), decode_error='ignore', ngram_range=(GRAM, GRAM),
  max_df=0.8, min_df=5, sublinear_tf=True, tokenizer=chinese_tokenizer
)
X = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()
feature_names = [name.replace(' ', '') for name in feature_names]
# 获取每个词语的平均 TF-IDF 值
tfidf_sum = X.sum(axis=0).A1  # 按列求和，得到每个词语的总 TF-IDF 值
tfidf_avg = tfidf_sum / X.shape[0]  # 计算每个词语的平均 TF-IDF 值

# 将 (词, 平均 TF-IDF值) 组成元组
tfidf_scores = list(zip(feature_names, tfidf_avg))
# 提取每个月份的前 N 个高 TF-IDF 关键词
N = 150  # 每个月份提取前 10 个关键词
top_n_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:N]
kws_map = { kw[0] :kw[-1] for kw in top_n_keywords }

with open(f'./word_freq_result.json', 'w', encoding='utf-8') as json_file:
  json.dump(kws_map, json_file, indent=4, ensure_ascii=False)