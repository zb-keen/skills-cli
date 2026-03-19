# keen-skills-cli

A CLI tool to download and manage keen skills from remote sources.

## 功能 Features

- 从远程源（GitHub、CDN 等）下载技能到桌面 - Download skills from remote sources (GitHub, CDN, etc.) to your desktop
- 列出可用技能 - List available skills
- 易于使用的命令行界面 - Easy-to-use command-line interface
- 发布技能到 npm 以便轻松分发 - Publish skills to npm for easy distribution

## 安装 Installation

### 从 npm From npm

```bash
npm install -g keen-skills-cli
```

### 从源代码 From source

1. 克隆仓库：Clone the repository:
   ```bash
   git clone <repository-url>
   cd keen-skills-cli
   ```

2. 安装依赖：Install dependencies:
   ```bash
   npm install
   ```

3. 链接 CLI 工具：Link the CLI tool:
   ```bash
   npm link
   ```

## 使用 Usage

### 下载技能 Download a skill

```bash
keen-skills download <skill-name>
```

**选项：**
- `-o, --output <path>`: 指定输出目录（默认：桌面）

**Options:**
- `-o, --output <path>`: Specify output directory (default: Desktop)

**示例：**
```bash
keen-skills download conversation-manager
```

**Example:**
```bash
keen-skills download conversation-manager
```

### 安装技能 Install a skill

```bash
keen-skills install <skill-name>
```

**选项：**
- `-o, --output <path>`: 指定输出目录（默认：桌面）

**Options:**
- `-o, --output <path>`: Specify output directory (default: Desktop)

**示例：**
```bash
keen-skills install conversation-manager
```

**Example:**
```bash
keen-skills install conversation-manager
```

### 列出可用技能 List available skills

```bash
keen-skills list
```

### 显示帮助 Show help

```bash
keen-skills help
```

## 可用技能 Available Skills

- **conversation-manager**: 会话压缩、分主题记忆、混合检索 - Conversation compression, topic-based memory, hybrid retrieval
- **question-optimizer**: 问题优化 - Question optimization

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

```
keen-skills-cli/
├── bin/                # CLI entry point
│   └── keen-skills.js  # Main CLI script
├── lib/                # Core functionality
│   └── download.js     # Download logic
├── package.json        # Package configuration
└── README.md           # Documentation
```

### 发布到 npm Publishing to npm

1. 更新 `package.json` 中的版本 - Update the version in `package.json`
2. 运行发布脚本： - Run the publish script:
   ```bash
   npm run publish
   ```

### 添加新技能 Adding new skills

1. 在项目根目录的 `.keen/skills` 目录中添加技能 - Add the skill to the `.keen/skills` directory in the project root
2. 更新 `lib/download.js` 中的 `listSkills` 函数以包含新技能 - Update the `listSkills` function in `lib/download.js` to include the new skill
3. 将更新后的 CLI 工具发布到 npm - Publish the updated CLI tool to npm

### 远程源配置 Remote source configuration

默认情况下，CLI 工具使用本地技能源。要使用真实的远程源：
By default, the CLI tool uses a local skills source. To use a real remote source:

1. 更新 `lib/download.js` 中的 `LOCAL_SKILLS_DIR` 以指向你的实际远程源 - Update the `LOCAL_SKILLS_DIR` in `lib/download.js` to point to your actual remote source
2. 在 `downloadSkill` 函数中实现远程下载逻辑 - Implement the remote download logic in the `downloadSkill` function

## 许可证 License

MIT