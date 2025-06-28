from typing import Any, Tuple

import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 加载模型和分词器
MODEL_PATH = "/Users/zhulitao/Franctoryer/dora-campus-guard/sentimate-analysis/saved_model"
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# 推理函数
def predict_sentiment(text: str) -> Tuple[Any, str, float]:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1)
        predicted_class = probs.argmax(dim=-1).item()
        confidence = probs[0, predicted_class].item()  # 取出对应类别的概率作为置信度

    emotion_label_map = {
        0: "悲伤",
        1: "失望",
        2: "讨厌",
        3: "平和",
        4: "疑惑",
        5: "开心",
        6: "期待"
    }

    return predicted_class, emotion_label_map[predicted_class], confidence


if __name__ == '__main__':
    text = "终于考完了！"
    print(predict_sentiment(text))