# conversation-manager

## Description
会话压缩、分主题记忆、混合检索

## Features
- 会话压缩：自动压缩长对话，提取关键信息
- 分主题记忆：按主题分类存储对话内容
- 混合检索：结合关键词和语义检索对话历史

## Usage
```javascript
const conversationManager = require('./conversation-manager');

// 初始化会话管理器
const manager = new conversationManager();

// 添加对话
manager.addMessage('用户', '你好，我想了解如何使用这个技能');
manager.addMessage('系统', '你好！我是会话管理器，可以帮助你管理对话内容。');

// 压缩会话
const compressedConversation = manager.compressConversation();
console.log(compressedConversation);

// 按主题检索
const topicResults = manager.searchByTopic('使用方法');
console.log(topicResults);
```