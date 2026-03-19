const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

// 本地技能目录
const LOCAL_SKILLS_DIR = path.join(__dirname, '..', '.keen', 'skills');

/**
 * 下载技能到指定目录
 * @param {string} skillName - 技能名称
 * @param {string} outputDir - 输出目录
 */
async function downloadSkill(skillName, outputDir) {
  try {
    console.log(chalk.grey(`Downloading skill ${skillName} from local source...`));

    // 创建输出目录
    const skillOutputPath = path.join(outputDir, `.keen`, `skills`, skillName);
    await fs.ensureDir(skillOutputPath);

    // 检查本地技能目录是否存在
    if (fs.existsSync(LOCAL_SKILLS_DIR)) {
      // 检查指定技能是否存在
      const localSkillPath = path.join(LOCAL_SKILLS_DIR, skillName);
      
      if (fs.existsSync(localSkillPath)) {
        // 从本地技能目录复制
        console.log(chalk.grey(`Copying skill files from local source...`));
        await fs.copy(localSkillPath, skillOutputPath, {
          overwrite: true,
          recursive: true
        });
      } else {
        throw new Error(`Skill ${skillName} not found in local skills directory`);
      }
    } else {
      throw new Error(`Local skills directory not found`);
    }

    // 验证复制是否成功
    if (!fs.existsSync(skillOutputPath)) {
      throw new Error(`Failed to create skill directory`);
    }

    console.log(chalk.grey(`Skill ${skillName} downloaded to ${skillOutputPath}`));
  } catch (error) {
    console.error(chalk.red(`Error downloading skill: ${error.message}`));
    throw error;
  }
}

/**
 * 列出可用技能
 * @returns {Promise<Array>} 可用技能列表
 */
async function listSkills() {
  try {
    // 检查本地技能目录是否存在
    if (fs.existsSync(LOCAL_SKILLS_DIR)) {
      // 从本地技能目录获取技能列表
      console.log(chalk.grey(`Getting skills from local source...`));
      const skillDirs = await fs.readdir(LOCAL_SKILLS_DIR);
      return skillDirs.map(dir => {
        // 读取 SKILL.md 文件获取描述
        const skillMdPath = path.join(LOCAL_SKILLS_DIR, dir, 'SKILL.md');
        let description = '未知技能';
        if (fs.existsSync(skillMdPath)) {
          const content = fs.readFileSync(skillMdPath, 'utf8');
          const match = content.match(/## Description[\s\S]*?(?=##|$)/i);
          if (match) {
            description = match[0].replace(/## Description\s*/i, '').trim();
          }
        }
        return { name: dir, description };
      });
    } else {
      console.error(chalk.red(`Local skills directory not found`));
      return [];
    }
  } catch (error) {
    console.error(chalk.red(`Error listing skills: ${error.message}`));
    return [];
  }
}

module.exports = {
  downloadSkill,
  listSkills
};
