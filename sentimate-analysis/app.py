from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sentiment import predict_sentiment

app = FastAPI()

# 输入结构
class Post(BaseModel):
    text: str


@app.post("/predict-emotion")
def predict_emotion(post: Post):
    """
    输入帖子文本，输出情感标签、置信度
    :param post:
    :return:
    """
    pred_id, pred_label, confidence = predict_sentiment(post.text)

    return {
        "emotion": pred_label,
        "label_id": pred_id,
        "confidence": confidence
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)