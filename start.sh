#!/bin/bash

# 显示启动信息
echo "🚀 Starting FastAPI app via Uvicorn..."

# 检查 PORT 是否设置
if [ -z "$PORT" ]; then
  echo "⚠️  PORT environment variable not set. Defaulting to 8000."
  PORT=8000
fi

echo "📡 Binding to 0.0.0.0:$PORT"

# 启动服务（生产环境不使用 --reload）
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port $PORT \
  --log-level info
