from transformers import (
    BertTokenizer, BertForSequenceClassification,
    Trainer, TrainingArguments
)
import torch
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score

# 使用 GPU（如果可用）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ------------ 1. 加载数据集 ----------------
dataset = load_dataset('csv', data_files={
    'train': './datasets/train.csv',
    'validation': './datasets/test.csv'
})
print(dataset)

# ------------ 2. 加载分词器和模型 ----------
MODEL_NAME = 'hfl/chinese-roberta-wwm-ext'
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=7).to(device)

# ------------ 3. 数据预处理 -----------------
def tokenize_function(examples):
    return tokenizer(
        examples['content'],
        padding="max_length",
        truncation=True,
        max_length=128
    )

encoded_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['content'])
encoded_dataset.set_format(type='torch', columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])

# ------------ 4. 训练参数配置 ----------------
training_args = TrainingArguments(
    output_dir="./model_output",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    load_best_model_at_end=True,
)

# ------------ 5. 评估函数定义 ----------------
def compute_metrics(eval_pred):
    preds = np.argmax(eval_pred.predictions, axis=1)
    labels = eval_pred.label_ids
    return {
        'accuracy': accuracy_score(labels, preds)
    }

# ------------ 6. 创建 Trainer 对象 ------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# ------------ 7. 模型训练 & 保存 ----------------
trainer.train()
trainer.save_model("./saved_model")
tokenizer.save_pretrained("./saved_model")

# ------------ 8. 模型评估 ----------------
results = trainer.evaluate()
print("Evaluation results:", results)
