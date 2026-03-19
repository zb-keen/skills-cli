#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合检索脚本
结合关键词检索和语义检索，提供更准确的信息检索
"""

import os
import re
import math
from collections import defaultdict


def read_file(file_path):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {file_path}", e)
        return ''


def scan_directory(directory):
    """
    扫描目录中的所有文件
    :param directory: 目录路径
    :return: 文件路径列表
    """
    files = []
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(os.path.join(root, filename))
    
    return files


def keyword_search(files, query):
    """
    关键词检索
    :param files: 文件路径列表
    :param query: 搜索关键词
    :return: 检索结果
    """
    results = []
    query_words = query.lower().split()
    
    for file in files:
        content = read_file(file)
        lower_content = content.lower()
        
        # 计算匹配得分
        score = 0
        for word in query_words:
            if word in lower_content:
                # 计算出现次数
                matches = len(re.findall(re.escape(word), lower_content))
                score += matches
        
        if score > 0:
            results.append({
                'file': file,
                'score': score,
                'type': 'keyword'
            })
    
    # 按得分排序
    return sorted(results, key=lambda x: x['score'], reverse=True)


def calculate_semantic_similarity(text1, text2):
    """
    计算语义相似度（基于词袋模型）
    :param text1: 第一个文本
    :param text2: 第二个文本
    :return: 相似度得分
    """
    def preprocess(text):
        return re.sub(r'[.,?!;()\[\]{}]', '', text.lower()).split()
    
    words1 = preprocess(text1)
    words2 = preprocess(text2)
    
    # 创建词袋
    word_set = set(words1 + words2)
    
    # 计算词频向量
    vector1 = defaultdict(int)
    vector2 = defaultdict(int)
    
    for word in word_set:
        vector1[word] = 0
        vector2[word] = 0
    
    for word in words1:
        vector1[word] += 1
    
    for word in words2:
        vector2[word] += 1
    
    # 计算余弦相似度
    dot_product = 0
    norm1 = 0
    norm2 = 0
    
    for word in word_set:
        dot_product += vector1[word] * vector2[word]
        norm1 += vector1[word] ** 2
        norm2 += vector2[word] ** 2
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))


def semantic_search(files, query):
    """
    语义检索
    :param files: 文件路径列表
    :param query: 搜索查询
    :return: 检索结果
    """
    results = []
    
    for file in files:
        content = read_file(file)
        similarity = calculate_semantic_similarity(content, query)
        
        if similarity > 0.1:  # 设置阈值
            results.append({
                'file': file,
                'score': similarity,
                'type': 'semantic'
            })
    
    # 按得分排序
    return sorted(results, key=lambda x: x['score'], reverse=True)


def extract_relevant_snippet(content, query, max_length=100):
    """
    提取相关片段
    :param content: 文件内容
    :param query: 搜索查询
    :param max_length: 最大长度
    :return: 相关片段
    """
    sentences = [s.strip() for s in re.split(r'[。！？.!?]', content) if s.strip()]
    query_words = query.lower().split()
    
    # 找到包含查询词的句子
    relevant_sentences = []
    for sentence in sentences:
        lower_sentence = sentence.lower()
        if any(word in lower_sentence for word in query_words):
            relevant_sentences.append(sentence)
    
    if relevant_sentences:
        snippet = '。'.join(relevant_sentences[:3]) + '。'
        return snippet[:max_length] + '...' if len(snippet) > max_length else snippet
    
    # 如果没有找到相关句子，返回前100个字符
    return content[:max_length] + '...' if len(content) > max_length else content


def hybrid_search(directory, query, top_k=5):
    """
    混合检索
    :param directory: 搜索目录
    :param query: 搜索查询
    :param top_k: 返回前K个结果
    :return: 混合检索结果
    """
    # 扫描目录中的所有文件
    files = scan_directory(directory)
    
    # 执行关键词检索
    keyword_results = keyword_search(files, query)
    
    # 执行语义检索
    semantic_results = semantic_search(files, query)
    
    # 合并结果并去重
    combined_results = {}
    
    # 关键词结果权重更高
    for result in keyword_results:
        combined_results[result['file']] = {
            'file': result['file'],
            'score': result['score'] * 0.7,  # 关键词权重
            'type': 'keyword'
        }
    
    # 语义结果
    for result in semantic_results:
        if result['file'] in combined_results:
            # 如果文件已在关键词结果中，增加语义得分
            combined_results[result['file']]['score'] += result['score'] * 0.3  # 语义权重
            combined_results[result['file']]['type'] = 'hybrid'
        else:
            combined_results[result['file']] = {
                'file': result['file'],
                'score': result['score'] * 0.3,  # 语义权重
                'type': 'semantic'
            }
    
    # 转换为数组并排序
    sorted_results = sorted(combined_results.values(), key=lambda x: x['score'], reverse=True)[:top_k]
    
    # 获取结果内容
    final_results = []
    for result in sorted_results:
        content = read_file(result['file'])
        # 提取相关片段
        snippet = extract_relevant_snippet(content, query)
        
        final_results.append({
            **result,
            'snippet': snippet,
            'filename': os.path.basename(result['file'])
        })
    
    return final_results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        test_directory = sys.argv[1]
        test_query = sys.argv[2]
    elif len(sys.argv) > 1:
        test_directory = os.path.join(os.path.dirname(__file__), '..', 'compression')
        test_query = sys.argv[1]
    else:
        test_directory = os.path.join(os.path.dirname(__file__), '..', 'compression')
        test_query = '插码修改'
    
    print("测试混合检索...")
    print(f"搜索查询: {test_query}")
    
    results = hybrid_search(test_directory, test_query, 3)
    print("检索结果：")
    for i, result in enumerate(results, 1):
        print(f"\n结果{i}: {result['filename']}")
        print(f"得分: {result['score']:.4f}")
        print(f"类型: {result['type']}")
        print(f"相关片段: {result['snippet']}")
