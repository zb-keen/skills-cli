#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主入口脚本
用于检测 Python 环境并执行相应的功能
"""

import os
import sys
import subprocess


def check_python_environment():
    """
    检测 Python 环境
    :return: True 如果 Python 环境可用，否则 False
    """
    try:
        # 尝试运行 Python 命令
        result = subprocess.run(
            [sys.executable, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def run_script(script_name, *args):
    """
    运行指定的脚本
    :param script_name: 脚本名称
    :param args: 脚本参数
    :return: 脚本执行结果
    """
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"错误: 脚本文件 {script_name} 不存在")
        return False
    
    try:
        cmd = [sys.executable, script_path] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"错误: 脚本执行失败")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"错误: 运行脚本时发生异常: {e}")
        return False


def main():
    """
    主函数
    """
    print("=== 对话管理器技能 ===")
    
    # 检测 Python 环境
    if not check_python_environment():
        print("错误: 未检测到 Python 环境")
        print("请安装 Python 3.6 或更高版本以使用此技能")
        return False
    
    # 显示可用命令
    print("\n可用命令:")
    print("1. 生成时间戳 - python scripts/main.py timestamp")
    print("2. 主题检测 - python scripts/main.py topic <对话内容文件>")
    print("3. 混合检索 - python scripts/main.py retrieve <搜索关键词>")
    print("4. 存储管理 - python scripts/main.py storage")
    print("5. 清理过时文件 - python scripts/main.py cleanup <天数>")
    
    # 处理命令行参数
    if len(sys.argv) < 2:
        print("\n请指定要执行的命令")
        return False
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'timestamp':
        return run_script('get_timestamp.py')
    elif command == 'topic':
        if len(args) < 1:
            print("错误: 请提供对话内容文件")
            return False
        return run_script('topic_detection.py', args[0])
    elif command == 'retrieve':
        if len(args) < 1:
            print("错误: 请提供搜索关键词")
            return False
        return run_script('hybrid_retrieval.py', args[0])
    elif command == 'storage':
        return run_script('storage_management.py')
    elif command == 'cleanup':
        days = args[0] if args else '30'
        return run_script('storage_management.py', days)
    else:
        print(f"错误: 未知命令 '{command}'")
        return False


if __name__ == "__main__":
    main()
