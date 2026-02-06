#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""塔罗牌抽取模块"""

import random

MAJOR = [
    "Fool", "Magician", "High Priestess", "Empress", "Emperor",
    "Hierophant", "Lovers", "Chariot", "Strength", "Hermit",
    "Wheel of Fortune", "Justice", "Hanged Man", "Death", "Temperance",
    "Devil", "Tower", "Star", "Moon", "Sun", "Judgement", "World"
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
NUMBERS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]

def get_deck():
    """获取完整牌组"""
    deck = MAJOR.copy()
    for suit in SUITS:
        for num in NUMBERS:
            deck.append(f"{num} of {suit}")
    return deck

def draw(n=3):
    """抽取n张塔罗牌"""
    deck = get_deck()
    drawn_indices = random.sample(range(len(deck)), n)
    results = []
    for idx in drawn_indices:
        card = deck[idx]
        orientation = random.choice(["Upright", "Reversed"])
        results.append({"card": card, "orientation": orientation})
    return results

def format_result(results):
    """格式化输出"""
    lines = ["=== TAROT ==="]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['card']} ({r['orientation']})")
    return "\n".join(lines)
