#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存储管理脚本
用于自动清理过时的压缩文件和主题文件，以及统计存储空间使用情况
"""

import os
import time


def get_file_size(file_path):
    """
    获取文件大小
    :param file_path: 文件路径
    :return: 文件大小（字节）
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"获取文件大小失败: {file_path}", e)
        return 0


def get_directory_size(directory):
    """
    计算目录大小
    :param directory: 目录路径
    :return: 目录大小（字节）
    """
    total_size = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += get_file_size(file_path)
    
    return total_size


def format_file_size(bytes_):
    """
    格式化文件大小
    :param bytes_: 字节数
    :return: 格式化后的文件大小
    """
    if bytes_ == 0:
        return '0 B'
    
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB']
    i = 0
    while bytes_ >= k and i < len(sizes) - 1:
        bytes_ /= k
        i += 1
    
    return f"{bytes_:.2f} {sizes[i]}"


def cleanup_old_files(directory, days=30):
    """
    清理过时文件
    :param directory: 目录路径
    :param days: 保留天数
    :return: 清理结果
    """
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    deleted_files = 0
    freed_space = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path):
                    mtime = os.path.getmtime(file_path)
                    if mtime < cutoff_time:
                        freed_space += get_file_size(file_path)
                        os.remove(file_path)
                        deleted_files += 1
            except Exception as e:
                print(f"清理文件失败: {file_path}", e)
    
    return {
        'deleted_files': deleted_files,
        'freed_space': freed_space
    }


def get_storage_stats(base_dir):
    """
    统计存储使用情况
    :param base_dir: 基础目录
    :return: 存储使用情况
    """
    compression_dir = os.path.join(base_dir, 'compression')
    topic_dir = os.path.join(base_dir, 'topic')
    scripts_dir = os.path.join(base_dir, 'scripts')
    
    compression_size = get_directory_size(compression_dir) if os.path.exists(compression_dir) else 0
    topic_size = get_directory_size(topic_dir) if os.path.exists(topic_dir) else 0
    scripts_size = get_directory_size(scripts_dir) if os.path.exists(scripts_dir) else 0
    total_size = compression_size + topic_size + scripts_size
    
    # 计算文件数量
    def count_files(dir_path):
        count = 0
        if os.path.exists(dir_path):
            for _, _, files in os.walk(dir_path):
                count += len(files)
        return count
    
    compression_files = count_files(compression_dir)
    topic_files = count_files(topic_dir)
    scripts_files = count_files(scripts_dir)
    
    return {
        'total_size': total_size,
        'formatted_total_size': format_file_size(total_size),
        'breakdown': {
            'compression': {
                'size': compression_size,
                'formatted_size': format_file_size(compression_size),
                'files': compression_files
            },
            'topic': {
                'size': topic_size,
                'formatted_size': format_file_size(topic_size),
                'files': topic_files
            },
            'scripts': {
                'size': scripts_size,
                'formatted_size': format_file_size(scripts_size),
                'files': scripts_files
            }
        }
    }


def main(base_dir, cleanup_days=30):
    """
    主函数
    :param base_dir: 基础目录
    :param cleanup_days: 清理天数
    """
    print('=== 存储管理 ===')
    
    # 统计存储使用情况
    print('\n1. 存储使用情况:')
    stats = get_storage_stats(base_dir)
    print(f'总存储使用: {stats["formatted_total_size"]}')
    print('\n详细 breakdown:')
    print(f'- 压缩文件: {stats["breakdown"]["compression"]["files"]} 个文件, {stats["breakdown"]["compression"]["formatted_size"]}')
    print(f'- 主题文件: {stats["breakdown"]["topic"]["files"]} 个文件, {stats["breakdown"]["topic"]["formatted_size"]}')
    print(f'- 脚本文件: {stats["breakdown"]["scripts"]["files"]} 个文件, {stats["breakdown"]["scripts"]["formatted_size"]}')
    
    # 清理过时文件
    print(f'\n2. 清理 {cleanup_days} 天前的文件:')
    cleanup_result = cleanup_old_files(base_dir, cleanup_days)
    print(f'- 删除文件数: {cleanup_result["deleted_files"]}')
    print(f'- 释放空间: {format_file_size(cleanup_result["freed_space"])}')
    
    # 再次统计存储使用情况
    print('\n3. 清理后存储使用情况:')
    after_stats = get_storage_stats(base_dir)
    print(f'总存储使用: {after_stats["formatted_total_size"]}')
    
    print('\n=== 存储管理完成 ===')


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    cleanup_days = 30
    if len(sys.argv) > 2:
        try:
            cleanup_days = int(sys.argv[2])
        except ValueError:
            pass
    
    main(base_dir, cleanup_days)
