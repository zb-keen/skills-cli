#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题检测脚本
使用TF-IDF和K-means聚类算法实现主题识别
"""

import os
import re
import math
import random
from collections import defaultdict


def preprocess_text(text):
    """
    预处理文本
    :param text: 原始文本
    :return: 预处理后的词列表
    """
    # 移除标点符号
    clean_text = re.sub(r'[.,?!;()\[\]{}]', '', text)
    # 转换为小写
    lower_text = clean_text.lower()
    # 分词
    words = lower_text.split()
    # 移除停用词
    stop_words = {
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'
    }
    return [word for word in words if len(word) > 1 and word not in stop_words]


def calculate_tfidf(documents):
    """
    计算TF-IDF
    :param documents: 文档列表
    :return: TF-IDF矩阵和词汇表
    """
    # 计算词频(TF)
    tf = []
    vocab = set()
    
    for doc in documents:
        words = preprocess_text(doc)
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
            vocab.add(word)
        tf.append(word_count)
    
    # 计算逆文档频率(IDF)
    idf = {}
    vocab_list = list(vocab)
    doc_count = len(documents)
    
    for word in vocab_list:
        count = 0
        for word_counts in tf:
            if word in word_counts:
                count += 1
        idf[word] = math.log(doc_count / (count + 1))
    
    # 计算TF-IDF
    tfidf = []
    for word_counts in tf:
        doc_tfidf = {}
        for word, count in word_counts.items():
            doc_tfidf[word] = count * idf[word]
        tfidf.append(doc_tfidf)
    
    return tfidf, vocab_list


def calculate_distance(vec1, vec2):
    """
    计算两个向量的欧几里得距离
    :param vec1: 第一个向量
    :param vec2: 第二个向量
    :return: 距离
    """
    all_keys = set(vec1.keys()) | set(vec2.keys())
    sum_sq = 0
    
    for key in all_keys:
        val1 = vec1.get(key, 0)
        val2 = vec2.get(key, 0)
        sum_sq += (val1 - val2) ** 2
    
    return math.sqrt(sum_sq)


def calculate_centroid(points):
    """
    计算聚类中心
    :param points: 数据点列表
    :return: 聚类中心
    """
    centroid = defaultdict(float)
    total_points = len(points)
    
    for point in points:
        for key, value in point.items():
            centroid[key] += value / total_points
    
    return dict(centroid)


def k_means(data, k, max_iterations=100):
    """
    K-means聚类
    :param data: 数据点列表
    :param k: 聚类数量
    :param max_iterations: 最大迭代次数
    :return: 聚类结果
    """
    # 初始化聚类中心
    centroids = random.sample(data, k) if len(data) >= k else data
    
    assignments = [0] * len(data)
    
    for _ in range(max_iterations):
        # 分配数据点到最近的聚类中心
        for i, point in enumerate(data):
            min_distance = float('inf')
            closest_centroid = 0
            
            for j, centroid in enumerate(centroids):
                distance = calculate_distance(point, centroid)
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid = j
            
            assignments[i] = closest_centroid
        
        # 更新聚类中心
        new_centroids = []
        for j in range(k):
            cluster_points = [data[i] for i, assignment in enumerate(assignments) if assignment == j]
            if cluster_points:
                new_centroids.append(calculate_centroid(cluster_points))
            else:
                # 如果聚类为空，重新随机初始化
                new_centroids.append(random.choice(data))
        
        # 检查收敛
        converged = all(calculate_distance(c1, c2) < 0.001 for c1, c2 in zip(centroids, new_centroids))
        if converged:
            break
        
        centroids = new_centroids
    
    return assignments, centroids


def extract_topic_keywords(centroid, top_n=5):
    """
    提取主题关键词
    :param centroid: 聚类中心
    :param top_n: 提取前N个关键词
    :return: 主题关键词
    """
    return [word for word, _ in sorted(centroid.items(), key=lambda x: x[1], reverse=True)[:top_n]]


def identify_topics(conversation, num_topics=3):
    """
    识别对话主题
    :param conversation: 对话内容
    :param num_topics: 主题数量
    :return: 主题列表
    """
    # 将对话分割为句子或段落
    sentences = [s.strip() for s in re.split(r'[。！？.!?]', conversation) if s.strip()]
    
    # 计算TF-IDF
    tfidf, _ = calculate_tfidf(sentences)
    
    # 使用K-means聚类
    if len(tfidf) < num_topics:
        num_topics = len(tfidf)
    
    assignments, centroids = k_means(tfidf, num_topics)
    
    # 提取每个主题的关键词
    topics = []
    for i, centroid in enumerate(centroids):
        keywords = extract_topic_keywords(centroid)
        # 为主题生成名称
        topic_name = f"主题_{'_'.join(keywords[:2])}" if len(keywords) >= 2 else f"主题_{i+1}"
        # 收集属于该主题的句子
        topic_sentences = [sentences[j] for j, assignment in enumerate(assignments) if assignment == i]
        
        topics.append({
            'id': i,
            'name': topic_name,
            'keywords': keywords,
            'content': '。'.join(topic_sentences) + '。'
        })
    
    return topics


if __name__ == "__main__":
    test_conversation = """
    用户要求修改 HotSaleCard.tsx 中的插码写法。
    我修改了文件中的插码逻辑，使其符合要求。
    用户要求修改 DicoverySearch.tsx 中的插码逻辑。
    我修改了文件中的 WT_envName 设置。
    用户要求创建 .trae/.ignore 文件。
    我创建了文件并添加了 node_modules/ 等忽略项。
    用户要求创建包含会话压缩、分主题记忆和混合检索功能的技能。
    我创建了 conversation-manager 技能。
    用户要求优化技能，添加文件存储和主题分类功能。
    我重新优化了技能文档。
    """
    
    print("测试主题识别...")
    topics = identify_topics(test_conversation, 3)
    print("识别到的主题：")
    for topic in topics:
        print(f"\n主题{topic['id'] + 1}: {topic['name']}")
        print(f"关键词: {', '.join(topic['keywords'])}")
        print(f"内容: {topic['content'][:100]}...")
