#!/usr/bin/env node

const { program } = require('commander');
const chalk = require('chalk');
const { downloadSkill, listSkills } = require('../lib/download');

// 获取默认输出目录
function getDefaultOutputDir() {
  // 确定默认输出目录为桌面
  if (process.platform === 'win32') {
    return process.env.USERPROFILE + '\\Desktop';
  } else {
    return process.env.HOME + '/Desktop';
  }
}

// 配置 CLI 命令
program
  .name('keen-skills')
  .description('A CLI tool to download and manage keen skills')
  .version('1.0.0');

// 下载技能命令
program
  .command('download <skill-name>')
  .description('Download a specific skill to your desktop')
  .option('-o, --output <path>', 'Specify output directory')
  .action(async (skillName, options) => {
    // 确保输出目录有默认值
    const outputDir = options.output || getDefaultOutputDir();
    console.log(chalk.blue(`Downloading skill: ${skillName}`));
    console.log(chalk.grey(`Output directory: ${outputDir}`));
    
    try {
      await downloadSkill(skillName, outputDir);
      console.log(chalk.green(`✓ Skill ${skillName} downloaded successfully!`));
    } catch (error) {
      console.error(chalk.red(`✗ Error downloading skill: ${error.message}`));
      process.exit(1);
    }
  });

// 列出可用技能命令
program
  .command('list')
  .description('List available skills')
  .action(async () => {
    console.log(chalk.blue('Available skills:'));
    try {
      const skills = await listSkills();
      if (skills.length === 0) {
        console.log(chalk.grey('  No skills available'));
      } else {
        skills.forEach(skill => {
          console.log(chalk.green(`  - ${skill.name}: ${skill.description}`));
        });
      }
    } catch (error) {
      console.error(chalk.red(`✗ Error listing skills: ${error.message}`));
    }
  });

// 安装技能命令
program
  .command('install <skill-name>')
  .description('Install a specific skill (alias for download)')
  .option('-o, --output <path>', 'Specify output directory')
  .action(async (skillName, options) => {
    // 确保输出目录有默认值
    const outputDir = options.output || getDefaultOutputDir();
    console.log(chalk.blue(`Installing skill: ${skillName}`));
    console.log(chalk.grey(`Output directory: ${outputDir}`));
    
    try {
      await downloadSkill(skillName, outputDir);
      console.log(chalk.green(`✓ Skill ${skillName} installed successfully!`));
    } catch (error) {
      console.error(chalk.red(`✗ Error installing skill: ${error.message}`));
      process.exit(1);
    }
  });

// 帮助信息
program
  .command('help')
  .description('Show help information')
  .action(() => {
    program.outputHelp();
  });

// 解析命令行参数
program.parse(process.argv);

// 如果没有提供命令，显示帮助信息
if (!program.args.length) {
  program.outputHelp();
}