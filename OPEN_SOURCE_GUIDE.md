# 开源项目完整流程指南

## 1. 项目准备阶段

### 1.1 项目规划
- **明确项目目标**：定义项目的核心功能和价值
- **技术栈选择**：选择合适的编程语言、框架和依赖
- **许可证选择**：
  - MIT：最宽松，适合大多数开源项目
  - Apache 2.0：适合企业级项目，包含专利保护
  - GPL：要求衍生作品也开源

### 1.2 项目结构设计
```
project-name/
├── project_name/       # 主包目录
├── tests/             # 测试代码
├── docs/              # 文档
├── examples/          # 示例代码
├── setup.py           # 安装配置
├── pyproject.toml     # 项目配置（PEP 621）
├── requirements.txt   # 依赖列表
├── README.md          # 项目说明
├── LICENSE            # 许可证
└── .gitignore         # Git忽略文件
```

### 1.3 基础文件编写

#### README.md
- 项目标题和简介
- 特性列表
- 安装和使用说明
- 贡献指南
- 许可证信息
- GitHub链接

#### LICENSE
- 从 [choosealicense.com](https://choosealicense.com/) 选择合适的许可证
- 确保包含版权信息和年份

#### .gitignore
- 使用 [gitignore.io](https://www.toptal.com/developers/gitignore) 生成适合项目的忽略规则
- 忽略 IDE 配置、虚拟环境、日志文件等

## 2. GitHub 仓库管理

### 2.1 创建仓库
1. 登录 GitHub，点击「New repository」
2. 填写仓库名称（建议与项目名称一致）
3. 选择许可证
4. 初始化 README 和 .gitignore
5. 点击「Create repository」

### 2.2 本地项目关联
```bash
# 初始化本地Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/username/repo-name.git

# 拉取远程仓库内容
git pull origin main

# 添加所有文件
git add .

# 第一次提交
git commit -m "Initial commit"

# 推送至GitHub
git push -u origin main
```

### 2.3 分支管理
- **main/master**：稳定版本分支
- **develop**：开发分支
- **feature/***：新功能分支
- **bugfix/***：bug修复分支
- **release/***：发布准备分支

### 2.4 代码规范
- 配置 linters（如 flake8、ruff）
- 配置类型检查（如 mypy）
- 配置格式化工具（如 black）
- 添加 pre-commit hooks

```bash
# 安装 pre-commit
pip install pre-commit

# 配置 pre-commit hooks
# 创建 .pre-commit-config.yaml 文件
pre-commit install
```

## 3. Python 包发布流程

### 3.1 包配置文件

#### pyproject.toml（推荐，PEP 621）
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "package-name"
version = "0.1.0"
description = "Package description"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [{name = "Your Name", email = "your.email@example.com"}]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "dependency1>=1.0.0",
    "dependency2>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]

[project.urls]
Homepage = "https://github.com/username/repo-name"
Documentation = "https://repo-name.readthedocs.io/"
Repository = "https://github.com/username/repo-name"
Issues = "https://github.com/username/repo-name/issues"

[tool.setuptools.packages.find]
where = ["."]
include = ["package_name*"]
```

#### setup.py（传统方式，可保留用于兼容性）
```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="package-name",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Package description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/repo-name",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dependency1>=1.0.0",
        "dependency2>=2.0.0",
    ],
)
```

#### MANIFEST.in
```
include README.md
include LICENSE
include pyproject.toml
recursive-include package_name *.py
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

### 3.2 版本管理

#### 语义化版本规范
```
MAJOR.MINOR.PATCH
```
- **MAJOR**：不兼容的API变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的bug修复

#### 版本号位置
- `pyproject.toml`：`version = "0.1.0"`
- `setup.py`：`version="0.1.0"`
- 考虑使用 `__version__` 变量在包中定义

### 3.3 构建和发布

#### 安装构建工具
```bash
pip install build twine
```

#### 构建包
```bash
# 清理旧构建
rm -rf dist/ build/ *.egg-info

# 构建源码包和wheel包
python -m build
```

#### 检查包
```bash
twine check dist/*
```

#### 上传到 PyPI

##### 1. 注册 PyPI 账号
- 访问 https://pypi.org/account/register/
- 验证邮箱

##### 2. 创建 API Token
- 登录 PyPI → 账户设置 → API Tokens
- 创建新Token，选择「Entire account」权限
- 保存Token，只显示一次

##### 3. 上传包
```bash
# 设置环境变量（推荐）
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxx

# 或直接使用命令
twine upload dist/*
```

##### 4. 上传到 TestPyPI（推荐测试）
```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ package-name
```

## 4. GitHub 最佳实践

### 4.1 Pull Request 流程
1. Fork 仓库
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request
5. 代码审查
6. 合并分支
7. 删除功能分支

### 4.2 Issue 管理
- 使用模板：bug报告、功能请求、文档改进
- 标签管理：bug、enhancement、documentation、help wanted
- 里程碑：用于版本规划

### 4.3 CI/CD 配置

#### GitHub Actions 示例
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    - name: Lint with flake8
      run: |
        flake8 .
    - name: Type check with mypy
      run: |
        mypy .
    - name: Test with pytest
      run: |
        pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## 5. 关键细节和注意事项

### 5.1 安全注意事项
- **不要提交敏感信息**：API密钥、密码、配置文件
- **定期更新依赖**：使用 `pip-audit` 检查安全漏洞
- **代码审查**：至少两名开发者审查代码
- **使用环境变量**：管理敏感配置

### 5.2 文档管理
- **README.md**：保持简洁明了，包含快速开始指南
- **API文档**：使用 Sphinx 或 MkDocs 生成
- **示例代码**：提供可运行的示例
- **贡献指南**：CONTRIBUTING.md 文件

### 5.3 测试策略
- **单元测试**：测试单个函数/类
- **集成测试**：测试模块间交互
- **端到端测试**：测试完整流程
- **覆盖率**：目标 >80%
- **CI集成**：自动运行测试

### 5.4 版本发布注意事项
- **创建标签**：`git tag v0.1.0 && git push --tags`
- **更新 CHANGELOG.md**：记录所有变更
- **发布说明**：在GitHub上创建发布版本
- **通知用户**：在相关社区宣传

### 5.5 社区管理
- **回应及时**：24-48小时内回复Issue
- **欢迎贡献**：鼓励社区参与
- **代码规范**：明确的贡献指南
- **行为准则**：CODE_OF_CONDUCT.md

## 6. 常见问题解决

### 6.1 包导入问题
- 确保 `__init__.py` 文件正确配置
- 检查 `PYTHONPATH` 环境变量
- 确保包名与目录名一致

### 6.2 依赖冲突
- 使用虚拟环境测试
- 明确依赖版本范围
- 使用 `pipdeptree` 查看依赖树

### 6.3 构建失败
- 检查 `pyproject.toml` 语法
- 确保所有文件路径正确
- 检查 Python 版本兼容性

### 6.4 上传失败
- 检查 API Token 权限
- 确保版本号未重复
- 检查包大小（PyPI限制：单个文件最大100MB）

## 7. 最佳实践

### 7.1 代码质量
- **遵循PEP 8**：Python代码规范
- **类型提示**：使用Python 3.6+的类型注解
- **文档字符串**：为所有公共API添加文档
- **模块化设计**：单一职责原则

### 7.2 性能优化
- **基准测试**：使用 `timeit` 或 `py-spy`
- **内存使用**：使用 `memory_profiler`
- **异步支持**：对I/O密集型操作使用asyncio

### 7.3 可维护性
- **清晰的命名**：变量、函数和类名要直观
- **注释**：解释复杂逻辑
- **减少耦合**：模块间低耦合，高内聚
- **重构**：定期优化代码结构

### 7.4 国际化
- **使用gettext**：支持多语言
- **避免硬编码文本**：使用配置文件
- **时区处理**：使用UTC时间

## 8. 持续维护

### 8.1 定期更新
- 依赖更新
- 安全补丁
- 文档更新

### 8.2 版本规划
- 短期计划：1-3个月
- 长期规划：6-12个月
- 公开 roadmap

### 8.3 社区建设
- 建立交流渠道：Discord、Slack、Gitter
- 维护贡献者列表
- 举办线上/线下活动

## 9. 示例项目结构

```
dynamic-graph-agent-framework/
├── dynamic_graph_agent_framework/  # 主包
│   ├── ai_tools/              # AI工具模块
│   ├── graph/                 # 图框架模块
│   └── __init__.py           # 公共API导出
├── tests/                     # 测试
│   ├── test_ai_tools.py
│   ├── test_graph.py
│   └── test_integration.py
├── examples/                  # 示例代码
│   └── demo.py
├── docs/                      # 文档
├── setup.py                   # 安装配置
├── pyproject.toml             # 项目配置
├── requirements.txt           # 依赖
├── README.md                  # 项目说明
├── LICENSE                    # 许可证
├── CHANGELOG.md               # 更新日志
├── .gitignore                 # Git忽略文件
└── .github/                   # GitHub配置
    ├── workflows/             # CI/CD
    └── ISSUE_TEMPLATE/        # Issue模板
```

## 10. 检查清单

### 项目初始化
- [ ] 明确项目目标和技术栈
- [ ] 选择合适的许可证
- [ ] 创建标准项目结构
- [ ] 编写README.md和LICENSE
- [ ] 配置.gitignore

### GitHub发布
- [ ] 创建GitHub仓库
- [ ] 推送初始代码
- [ ] 配置CI/CD
- [ ] 设置Issue模板和PR模板
- [ ] 配置分支保护

### Python包发布
- [ ] 编写setup.py和pyproject.toml
- [ ] 配置MANIFEST.in
- [ ] 测试构建过程
- [ ] 上传到TestPyPI并测试
- [ ] 上传到正式PyPI

### 维护阶段
- [ ] 定期更新依赖
- [ ] 响应Issue和PR
- [ ] 发布新版本
- [ ] 更新文档
- [ ] 社区建设

## 11. 资源链接

### 官方文档
- [PyPI Documentation](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [GitHub Docs](https://docs.github.com/)

### 工具和服务
- [PyPI](https://pypi.org/)
- [TestPyPI](https://test.pypi.org/)
- [Read the Docs](https://readthedocs.org/)
- [Codecov](https://codecov.io/)
- [Codacy](https://www.codacy.com/)

### 最佳实践参考
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Open Source Guides](https://opensource.guide/)

---

**最后更新时间**: 2025-12-28
**作者**: 智能体框架开发团队
