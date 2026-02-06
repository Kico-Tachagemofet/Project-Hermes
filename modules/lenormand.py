#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""雷诺曼牌抽取模块"""

import random

CARDS = [
    "1-Rider", "2-Clover", "3-Ship", "4-House", "5-Tree", "6-Clouds",
    "7-Snake", "8-Coffin", "9-Bouquet", "10-Scythe", "11-Whip", "12-Birds",
    "13-Child", "14-Fox", "15-Bear", "16-Stars", "17-Stork", "18-Dog",
    "19-Tower", "20-Garden", "21-Mountain", "22-Crossroads", "23-Mice",
    "24-Heart", "25-Ring", "26-Book", "27-Letter", "28-Gentleman", "29-Lady",
    "30-Lily", "31-Sun", "32-Moon", "33-Key", "34-Fish", "35-Anchor", "36-Cross"
]

def draw(n=3):
    """抽取n张雷诺曼牌"""
    if n > len(CARDS):
        n = len(CARDS)
    return random.sample(CARDS, n)

def format_result(results):
    """格式化输出"""
    lines = ["=== LENORMAND ==="]
    for i, card in enumerate(results, 1):
        lines.append(f"{i}. {card}")
    return "\n".join(lines)
