# keen-skills-cli

A CLI tool to download and manage keen skills from remote sources.

## 功能 Features

- 从远程源（GitHub、CDN 等）下载技能到桌面 - Download skills from remote sources (GitHub, CDN, etc.) to your desktop
- 列出可用技能 - List available skills
- 易于使用的命令行界面 - Easy-to-use command-line interface
- 发布技能到 npm 以便轻松分发 - Publish skills to npm for easy distribution

## 安装 Installation

### 从 npm

```bash
npm install -g keen-skills-cli
```

### 从源代码

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   cd keen-skills-cli
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 链接 CLI 工具：
   ```bash
   npm link
   ```

## 使用 Usage

### 下载技能

```bash
keen-skills download <skill-name>
```

**选项：**
- `-o, --output <path>`: 指定输出目录（默认：桌面）

**示例：**
```bash
keen-skills download conversation-manager
```

### 安装技能

```bash
keen-skills install <skill-name>
```

**选项：**
- `-o, --output <path>`: 指定输出目录（默认：桌面）

**示例：**
```bash
keen-skills install conversation-manager
```

### 列出可用技能

```bash
keen-skills list
```

### 显示帮助

```bash
keen-skills help
```

## 可用技能 Available Skills

- **conversation-manager**: 会话压缩、分主题记忆、混合检索
- **question-optimizer**: 问题优化

## 开发 Development

### 项目结构 Project Structure

```
keen-skills-cli/
├── bin/                # CLI 入口点
│   └── keen-skills.js  # 主 CLI 脚本
├── lib/                # 核心功能
│   └── download.js     # 下载逻辑
├── package.json        # 包配置
└── README.md           # 文档
```

### 发布到 npm

1. 更新 `package.json` 中的版本
2. 运行发布脚本：
   ```bash
   npm run publish
   ```

### 添加新技能

1. 在项目根目录的 `.keen/skills` 目录中添加技能
2. 更新 `lib/download.js` 中的 `listSkills` 函数以包含新技能
3. 将更新后的 CLI 工具发布到 npm

### 远程源配置

默认情况下，CLI 工具使用本地技能源。要使用真实的远程源：

1. 更新 `lib/download.js` 中的 `LOCAL_SKILLS_DIR` 以指向你的实际远程源
2. 在 `downloadSkill` 函数中实现远程下载逻辑

## 许可证 License

MIT