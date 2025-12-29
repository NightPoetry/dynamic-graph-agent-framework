#!/bin/bash

# 动态图智能体框架一键安装脚本
# Linux/Mac版本

echo "==============================================="
echo "       Dynamic Graph Agent Framework"
echo "==============================================="
echo "正在检查Python环境..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python 3环境，请先安装Python 3.8+"
    exit 1
fi

python3 --version

# 检查是否已存在.venv目录
echo "正在检查虚拟环境..."
if [ ! -d ".venv" ]; then
    echo "未找到虚拟环境，正在创建.venv..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "错误：创建虚拟环境失败"
        exit 1
    fi
    echo "虚拟环境创建成功"
else
    echo "虚拟环境已存在，跳过创建"
fi

echo "正在激活虚拟环境..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "错误：激活虚拟环境失败"
    exit 1
fi

echo "正在升级pip..."
python3 -m pip install --upgrade pip > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "警告：升级pip失败，但将继续安装"
fi

echo "正在安装开发模式包..."
pip install -e .[dev]

if [ $? -ne 0 ]; then
    echo "错误：安装开发模式包失败"
    exit 1
fi

echo "==============================================="
echo "安装成功！"
echo "==============================================="
echo "如何使用："
echo "1. 激活虚拟环境："
echo "   source .venv/bin/activate"
echo "2. 运行示例："
echo "   python examples/demo.py"
echo "3. 运行测试："
echo "   python -m pytest tests/"
echo "==============================================="

echo "按任意键继续..."
read -n 1 -s
