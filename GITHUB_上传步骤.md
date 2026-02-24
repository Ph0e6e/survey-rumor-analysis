# 将项目上传到 GitHub 的步骤

## 前提条件
- 已安装 [Git](https://git-scm.com/downloads)
- 已注册 [GitHub](https://github.com) 账号

---

## 一、在本地初始化 Git 并提交

在项目根目录（即本文件夹）打开终端（PowerShell 或 CMD），依次执行：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件（.gitignore 中已排除的不会加入）
git add .

# 3. 第一次提交
git commit -m "Initial commit: 问卷与谣言分析项目"
```

---

## 二、在 GitHub 上创建新仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写：
   - **Repository name**：例如 `survey-rumor-analysis`（或你喜欢的英文名）
   - **Description**：可选，如「问卷与谣言数据分析」
   - 选择 **Public**
   - **不要**勾选 "Add a README file"（本地已有代码）
4. 点击 **Create repository**

---

## 三、关联远程仓库并推送

创建完成后，GitHub 会显示命令。在项目目录下执行（把 `你的用户名` 和 `仓库名` 换成实际值）：

```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 主分支命名为 main（若 GitHub 提示用 main）
git branch -M main

# 推送到 GitHub
git push -u origin main
```

首次推送时可能会要求登录 GitHub（浏览器或用户名+密码/Token）。

---

## 四、若使用 SSH（可选）

若已配置 SSH 密钥，可用 SSH 地址：

```bash
git remote add origin git@github.com:你的用户名/仓库名.git
git push -u origin main
```

---

## 注意事项

- 本项目的 **.gitignore** 已配置，会忽略 `__pycache__`、虚拟环境等，不会把这些提交到 GitHub。
- 若 **问卷数据** 或 **结果文件** 含敏感信息，可编辑 `.gitignore`，取消注释其中与数据/结果相关的几行，这样这些文件就不会被提交。
- 推送时若提示需要认证，请按 GitHub 文档使用 [Personal Access Token](https://github.com/settings/tokens) 或 SSH。
