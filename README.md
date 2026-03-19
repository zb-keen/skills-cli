# keen-skills-cli

A CLI tool to download and manage keen skills from remote sources.

## Features

- Download skills from remote sources (GitHub, CDN, etc.) to your desktop
- List available skills
- Easy-to-use command-line interface
- Publish skills to npm for easy distribution

## Installation

### From npm

```bash
npm install -g keen-skills-cli
```

### From Source

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd keen-skills-cli
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Link the CLI tool:
   ```bash
   npm link
   ```

## Usage

### Download a skill

```bash
keen-skills download <skill-name>
```

**Options:**
- `-o, --output <path>`: Specify output directory (default: Desktop)

**Example:**
```bash
keen-skills download conversation-manager
```

### Install a skill

```bash
keen-skills install <skill-name>
```

**Options:**
- `-o, --output <path>`: Specify output directory (default: Desktop)

**Example:**
```bash
keen-skills install conversation-manager
```

### List available skills

```bash
keen-skills list
```

### Show help

```bash
keen-skills help
```

## Available Skills

- **conversation-manager**: 会话压缩、分主题记忆、混合检索
- **question-optimizer**: 问题优化

## Development

### Project Structure

```
keen-skills-cli/
├── bin/                # CLI entry point
│   └── keen-skills.js  # Main CLI script
├── lib/                # Core functionality
│   └── download.js     # Download logic
├── package.json        # Package configuration
└── README.md           # Documentation
```

### Publishing to npm

1. Update the version in `package.json`
2. Run the publish script:
   ```bash
   npm run publish
   ```

### Adding New Skills

1. Add the skill to the `.trae/skills` directory in the project root
2. Update the `listSkills` function in `lib/download.js` to include the new skill
3. Publish the updated CLI tool to npm

### Remote Source Configuration

By default, the CLI tool uses a simulated remote source. To use a real remote source:

1. Update the `SKILLS_REMOTE_URL` in `lib/download.js` to point to your actual remote source
2. Implement the remote download logic in the `downloadSkill` function

## License

MIT
