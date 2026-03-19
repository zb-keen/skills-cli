# question-optimizer

## Description
问题优化

## Features
- 问题重述：优化用户问题的表述
- 问题扩展：为用户问题添加相关背景信息
- 问题分类：自动分类用户问题的类型

## Usage
```javascript
const questionOptimizer = require('./question-optimizer');

// 初始化问题优化器
const optimizer = new questionOptimizer();

// 优化问题
const originalQuestion = '如何使用这个功能？';
const optimizedQuestion = optimizer.optimize(originalQuestion);
console.log('优化后的问题:', optimizedQuestion);

// 扩展问题
const extendedQuestion = optimizer.extend(originalQuestion);
console.log('扩展后的问题:', extendedQuestion);

// 分类问题
const category = optimizer.classify(originalQuestion);
console.log('问题分类:', category);
```