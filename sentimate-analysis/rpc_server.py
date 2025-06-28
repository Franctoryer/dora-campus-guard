from xmlrpc.server import SimpleXMLRPCServer
from sentiment import predict_sentiment

# 定义包装函数（因为 XML-RPC 不能直接返回复杂对象）
def predict_emotion(text):
    """
    输入文本，返回情感分析结果
    """
    pred_id, pred_label, confidence = predict_sentiment(text)
    return {
        "label_id": pred_id,
        "emotion": pred_label,
        "confidence": confidence
    }

def main():
    # 启动 XML-RPC Server
    server = SimpleXMLRPCServer(("0.0.0.0", 8002), allow_none=True)
    print("🚀 XML-RPC 服务已启动，端口: 8002")

    # 注册函数
    server.register_function(predict_emotion, "predict_emotion")

    # 启动服务循环
    server.serve_forever()

if __name__ == "__main__":
    main()
