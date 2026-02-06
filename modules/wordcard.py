#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""字卡抽取模块"""

import random
import json
import os

def load_cards(file_path):
    """加载字卡库"""
    cards = []
    ext = os.path.splitext(file_path)[1].lower()

    with open(file_path, 'r', encoding='utf-8') as f:
        if ext == '.json':
            cards = json.load(f)
        else:  # txt or md
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('---'):
                    if line.startswith('"') and line.endswith('"'):
                        line = line[1:-1]
                    if line and ':' not in line[:10]:
                        cards.append(line)
    return cards

def draw(cards, n=3):
    """抽取n张字卡"""
    if len(cards) < n:
        n = len(cards)
    return random.sample(cards, n)

def format_result(results, entity="Hermes"):
    """格式化输出"""
    lines = [f"=== WORD CARDS ({entity}) ==="]
    for i, card in enumerate(results, 1):
        lines.append(f"{i}. {card}")
    return "\n".join(lines)
