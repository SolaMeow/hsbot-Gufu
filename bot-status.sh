#!/bin/bash

# Python脚本的名称
script_name="hsbot-refac.py"

# 获取Python脚本的PID
pid=$(ps aux | grep $script_name | grep -v grep | awk '{print $2}')

# 如果没有找到PID，打印错误消息并退出
if [ -z "$pid" ]; then
    echo "No process found for script $script_name"
    exit 1
fi

# 打印PID
echo "PID for script $script_name: $pid"

# 使用lsof命令获取并打印使用的端口
echo "Ports used by script $script_name:"
sudo lsof -Pan -p $pid -i