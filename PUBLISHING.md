# 发布指南

本文档说明如何将 `dynamic-graph-agent-framework` 发布到 PyPI。

## 前置准备

1. **注册 PyPI 账号**
   - 访问 https://pypi.org/account/register/
   - 注册并验证邮箱

2. **安装发布工具**
   ```bash
   pip install build twine
   ```

3. **配置 PyPI API Token**
   - 登录 PyPI，访问 https://pypi.org/manage/account/token/
   - 创建新的 API Token（建议命名为 "agent-graph-framework"）
   - 保存 Token，稍后使用

## 发布步骤

### 1. 更新版本号

在 `pyproject.toml` 和 `setup.py` 中更新版本号：

```toml
[project]
version = "0.1.0"  # 更新为新版本
```

```python
setup(
    version="0.1.0",  # 更新为新版本
    ...
)
```

### 2. 构建分发包

```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info

# 构建源码分发包和wheel包
python -m build
```

构建成功后，`dist/` 目录下会生成：
- `agent_graph_framework-0.1.0.tar.gz` (源码包)
- `agent_graph_framework-0.1.0-py3-none-any.whl` (wheel包)

### 3. 检查分发包

```bash
# 检查包的描述和元数据
twine check dist/*
```

确保没有错误或警告。

### 4. 上传到 PyPI

**首次上传（使用 TestPyPI 测试）：**

```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*
```

- TestPyPI 地址：https://test.pypi.org/project/agent-graph-framework/
- 测试安装：`pip install --index-url https://test.pypi.org/simple/ agent-graph-framework`

**上传到正式 PyPI：**

```bash
# 上传到 PyPI（会提示输入用户名和密码）
twine upload dist/*
```

或者使用 API Token：

```bash
# 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxx...  # 你的API Token

# 上传
twine upload dist/*
```

在 Windows PowerShell 中：

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxx..."
twine upload dist/*
```

### 5. 验证发布

发布成功后，访问：
- PyPI: https://pypi.org/project/agent-graph-framework/
- 安装测试：`pip install agent-graph-framework`

## 版本管理

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- `MAJOR.MINOR.PATCH` (主版本.次版本.修订号)
- `MAJOR`：不兼容的 API 变更
- `MINOR`：向后兼容的功能新增
- `PATCH`：向后兼容的问题修复

示例：
- `0.1.0` → `0.1.1` (修复bug)
- `0.1.1` → `0.2.0` (新增功能)
- `0.2.0` → `1.0.0` (重大变更，发布稳定版)

## 发布检查清单

发布前确认：

- [ ] 更新版本号
- [ ] 更新 `README.md` 中的文档
- [ ] 运行所有测试：`python -m pytest tests/`
- [ ] 更新 `CHANGELOG.md`（如果有）
- [ ] 检查 `LICENSE` 文件
- [ ] 确认依赖版本正确
- [ ] 构建并检查分发包
- [ ] 先在 TestPyPI 测试

## 常见问题

### 1. 包名已存在

如果包名已被占用，需要在 `setup.py` 和 `pyproject.toml` 中修改包名：

```python
setup(
    name="your-unique-package-name",  # 修改为唯一的包名
    ...
)
```

### 2. 上传失败

检查：
- 网络连接
- API Token 是否正确
- 版本号是否已存在（不能重复发布相同版本）

### 3. 构建警告

如果构建时出现警告，修复后再发布。常见警告：
- 缺少 `long_description`
- 缺少 `classifiers`
- 依赖版本范围不明确

## 自动化发布（可选）

使用 GitHub Actions 自动发布：

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

在 GitHub 仓库设置中添加 `PYPI_API_TOKEN` secret。

发布时创建 git tag：

```bash
git tag v0.1.0
git push origin v0.1.0
```

## 参考资源

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine 文档](https://twine.readthedocs.io/)
- [语义化版本](https://semver.org/)
