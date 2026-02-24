# 第一次上传项目到 GitHub — 完整操作指南

按下面顺序一步一步做即可。每完成一步再做下一步。

---

## 第 0 步：先确认两件事

1. **电脑已安装 Git**  
   - 打开 PowerShell 或 CMD，输入：`git --version`  
   - 若显示版本号（如 `git version 2.x.x`）说明已安装。  
   - 若提示“不是内部或外部命令”，请先安装：https://git-scm.com/downloads

2. **已有 GitHub 账号**  
   - 没有的话先注册：https://github.com

---

## 第 1 步：在项目文件夹里打开终端

1. 在资源管理器中打开你的项目文件夹：  
   `WPS云盘\cursor\Development`
2. 在文件夹空白处 **按住 Shift + 右键**，选择 **“在此处打开 PowerShell 窗口”**（或“在终端中打开”）。  
   这样终端一打开就已经在这个项目目录里了。

---

## 第 2 步：在终端里执行下面 3 条命令（一条一条复制执行）

**命令 1：初始化 Git 仓库**

```powershell
git init
```

执行后可能看到：`Initialized empty Git repository in ...`，说明成功。

---

**命令 2：把当前文件夹里的文件加入“待提交列表”**

```powershell
git add .
```

执行后一般没有输出，这是正常的。

---

**命令 3：做第一次“提交”（相当于给当前版本打个快照）**

```powershell
git commit -m "Initial commit: 问卷与谣言分析项目"
```

若第一次用 Git，可能会提示让你设置姓名和邮箱，按下面两条先设置再重新执行上面的 `git commit`：

```powershell
git config --global user.email "你的邮箱@example.com"
git config --global user.name "你的名字或GitHub用户名"
```

然后再执行一次：

```powershell
git commit -m "Initial commit: 问卷与谣言分析项目"
```

看到类似 `X files changed` 就表示第 1 步完成。

---

## 第 3 步：在 GitHub 网站上创建一个“空仓库”

1. 打开浏览器，登录 https://github.com  
2. 点击右上角 **“+”** → **“New repository”**  
3. 填写：
   - **Repository name**：起一个英文名，例如：`survey-rumor-analysis`（只能英文、数字、短横线）
   - **Description**：选填，如：问卷与谣言数据分析
   - 下面选择 **Public**
   - **不要勾选** “Add a README file”
4. 点击绿色按钮 **“Create repository”**

创建完成后，页面会显示一个地址，类似：  
`https://github.com/你的用户名/survey-rumor-analysis.git`  
先记住这个页面，下一步会用到。

---

## 第 4 步：把本地项目和 GitHub 仓库连起来并上传

回到刚才打开的项目文件夹的终端，**把下面命令里的“你的用户名”和“仓库名”换成你在第 3 步里填的**：

**命令 4：添加远程仓库地址（只改用户名和仓库名）**

```powershell
git remote add origin https://github.com/你的用户名/仓库名.git
```

例如你的 GitHub 用户名是 `zhangsan`，仓库名是 `survey-rumor-analysis`，就写：

```powershell
git remote add origin https://github.com/zhangsan/survey-rumor-analysis.git
```

---

**命令 5：把当前分支改名为 main（GitHub 默认主分支名）**

```powershell
git branch -M main
```

---

**命令 6：推送到 GitHub**

```powershell
git push -u origin main
```

- 第一次推送时，可能会弹出浏览器让你登录 GitHub，按提示登录即可。  
- 若提示输入用户名和密码：**密码处要填 GitHub 的 Personal Access Token**，不是登录密码。  
  - 生成 Token：GitHub 网页 → 右上角头像 → **Settings** → 左侧最下方 **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**，勾选 `repo`，生成后复制，在终端里当密码粘贴。

看到类似 `Branch 'main' set up to track...` 和 `Everything up-to-date` 或文件数量统计，就说明上传成功了。

---

## 第 5 步：在网页上确认

打开：  
`https://github.com/你的用户名/仓库名`  
（例如：`https://github.com/zhangsan/survey-rumor-analysis`）

能看到你的代码和文件列表，就表示整个流程都完成了。

---

## 常见问题

| 情况 | 处理方式 |
|------|----------|
| 提示 `git 不是内部或外部命令` | 先安装 Git：https://git-scm.com/downloads，安装后关掉终端再重新打开。 |
| 执行 `git commit` 时提示要设置 user.email / user.name | 按上面第 2 步里的 `git config --global` 两条命令设置后再执行一次 `git commit`。 |
| 提示 `remote origin already exists` | 说明已经添加过远程仓库，可跳过“命令 4”，直接执行命令 5 和 6。 |
| 推送时一直要密码 / 认证失败 | 使用 Personal Access Token 作为密码，或按提示用浏览器登录。 |

---

以后如果改了代码，想再次同步到 GitHub，只需在项目目录打开终端，执行：

```powershell
git add .
git commit -m "这里写你这次改了什么"
git push
```

按这份指南做完一遍，你就完成第一次上传了。遇到哪一步报错，把终端里的完整提示复制下来，我可以帮你逐句看。
