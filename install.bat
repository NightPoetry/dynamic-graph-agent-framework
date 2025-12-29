@echo off
setlocal enabledelayedexpansion

REM 动态图智能体框架一键安装脚本
REM Windows版本

echo ==============================================
echo       Dynamic Graph Agent Framework

echo ==============================================
echo 正在检查Python环境...

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)

python --version

echo 正在检查虚拟环境...

REM 检查是否已存在.venv目录
if not exist ".venv" (
    echo 未找到虚拟环境，正在创建.venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo 错误：创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
) else (
    echo 虚拟环境已存在，跳过创建
)

echo 正在激活虚拟环境...
.venv\Scripts\activate

if %errorlevel% neq 0 (
    echo 错误：激活虚拟环境失败
    pause
    exit /b 1
)

echo 正在升级pip...
python -m pip install --upgrade pip >nul 2>&1

if %errorlevel% neq 0 (
    echo 警告：升级pip失败，但将继续安装
)

echo 正在安装开发模式包...
pip install -e .[dev]

if %errorlevel% neq 0 (
    echo 错误：安装开发模式包失败
    pause
    exit /b 1
)

echo ==============================================
echo 安装成功！
echo ==============================================
echo 如何使用：
echo 1. 激活虚拟环境：
    echo    .venv\Scripts\activate
echo 2. 运行示例：
    echo    python examples/demo.py
echo 3. 运行测试：
    echo    python -m pytest tests/
echo ==============================================

pause
endlocal