#!/bin/bash
# 安装 IK 分词器
if [ ! -d "/usr/share/elasticsearch/plugins/analysis-ik" ]; then
  echo "Installing IK Analysis plugin..."
  /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch https://release.infinilabs.com/analysis-ik/stable/elasticsearch-analysis-ik-8.15.0.zip
else
  echo "IK Analysis plugin already installed."
fi

# 启动 Elasticsearch
exec /usr/local/bin/docker-entrypoint.sh