#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""妈祖灵签模块"""

import random
import json
import os

def load_signs(file_path):
    """加载签文数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("signs", [])

def draw(signs):
    """抽签"""
    if not signs:
        return None
    sign = random.choice(signs)
    return sign

def format_result(result):
    """格式化输出"""
    if not result:
        return "=== 妈祖灵签 ===\n无签文数据"
    lines = ["=== 妈祖灵签 ==="]
    lines.append(f"第{result['number']}签")
    lines.append("")
    for line in result.get("poem", []):
        lines.append(line)
    return "\n".join(lines)
