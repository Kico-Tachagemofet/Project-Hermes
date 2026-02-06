#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""易经起卦模块"""

import random

TRIGRAMS = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
TRIGRAM_SYMBOLS = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳", "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

# 64卦对照表 (上卦, 下卦) -> (卦名, 卦序)
HEXAGRAMS = {
    ("乾", "乾"): ("乾为天", 1), ("乾", "兑"): ("天泽履", 10), ("乾", "离"): ("天火同人", 13),
    ("乾", "震"): ("天雷无妄", 25), ("乾", "巽"): ("天风姤", 44), ("乾", "坎"): ("天水讼", 6),
    ("乾", "艮"): ("天山遁", 33), ("乾", "坤"): ("天地否", 12),
    ("兑", "乾"): ("泽天夬", 43), ("兑", "兑"): ("兑为泽", 58), ("兑", "离"): ("泽火革", 49),
    ("兑", "震"): ("泽雷随", 17), ("兑", "巽"): ("泽风大过", 28), ("兑", "坎"): ("泽水困", 47),
    ("兑", "艮"): ("泽山咸", 31), ("兑", "坤"): ("泽地萃", 45),
    ("离", "乾"): ("火天大有", 14), ("离", "兑"): ("火泽睽", 38), ("离", "离"): ("离为火", 30),
    ("离", "震"): ("火雷噬嗑", 21), ("离", "巽"): ("火风鼎", 50), ("离", "坎"): ("火水未济", 64),
    ("离", "艮"): ("火山旅", 56), ("离", "坤"): ("火地晋", 35),
    ("震", "乾"): ("雷天大壮", 34), ("震", "兑"): ("雷泽归妹", 54), ("震", "离"): ("雷火丰", 55),
    ("震", "震"): ("震为雷", 51), ("震", "巽"): ("雷风恒", 32), ("震", "坎"): ("雷水解", 40),
    ("震", "艮"): ("雷山小过", 62), ("震", "坤"): ("雷地豫", 16),
    ("巽", "乾"): ("风天小畜", 9), ("巽", "兑"): ("风泽中孚", 61), ("巽", "离"): ("风火家人", 37),
    ("巽", "震"): ("风雷益", 42), ("巽", "巽"): ("巽为风", 57), ("巽", "坎"): ("风水涣", 59),
    ("巽", "艮"): ("风山渐", 53), ("巽", "坤"): ("风地观", 20),
    ("坎", "乾"): ("水天需", 5), ("坎", "兑"): ("水泽节", 60), ("坎", "离"): ("水火既济", 63),
    ("坎", "震"): ("水雷屯", 3), ("坎", "巽"): ("水风井", 48), ("坎", "坎"): ("坎为水", 29),
    ("坎", "艮"): ("水山蹇", 39), ("坎", "坤"): ("水地比", 8),
    ("艮", "乾"): ("山天大畜", 26), ("艮", "兑"): ("山泽损", 41), ("艮", "离"): ("山火贲", 22),
    ("艮", "震"): ("山雷颐", 27), ("艮", "巽"): ("山风蛊", 18), ("艮", "坎"): ("山水蒙", 4),
    ("艮", "艮"): ("艮为山", 52), ("艮", "坤"): ("山地剥", 23),
    ("坤", "乾"): ("地天泰", 11), ("坤", "兑"): ("地泽临", 19), ("坤", "离"): ("地火明夷", 36),
    ("坤", "震"): ("地雷复", 24), ("坤", "巽"): ("地风升", 46), ("坤", "坎"): ("地水师", 7),
    ("坤", "艮"): ("地山谦", 15), ("坤", "坤"): ("坤为地", 2),
}

TRIGRAM_BINARY = {
    1: [1, 1, 1], 2: [0, 1, 1], 3: [1, 0, 1], 4: [0, 0, 1],
    5: [1, 1, 0], 6: [0, 1, 0], 7: [1, 0, 0], 8: [0, 0, 0],
}

def get_trigram(num):
    """根据数字获取卦象"""
    remainder = num % 8
    return TRIGRAMS[remainder if remainder != 0 else 8]

def get_yao_position(num):
    """根据数字获取变爻位置"""
    remainder = num % 6
    return remainder if remainder != 0 else 6

def change_yao(upper, lower, yao_pos):
    """根据变爻位置改变卦象"""
    upper_num = [k for k, v in TRIGRAMS.items() if v == upper][0]
    lower_num = [k for k, v in TRIGRAMS.items() if v == lower][0]

    upper_bits = TRIGRAM_BINARY[upper_num].copy()
    lower_bits = TRIGRAM_BINARY[lower_num].copy()

    if yao_pos <= 3:
        lower_bits[3 - yao_pos] = 1 - lower_bits[3 - yao_pos]
    else:
        upper_bits[6 - yao_pos] = 1 - upper_bits[6 - yao_pos]

    def bits_to_trigram(bits):
        for num, b in TRIGRAM_BINARY.items():
            if b == bits:
                return TRIGRAMS[num]
        return None

    return bits_to_trigram(upper_bits), bits_to_trigram(lower_bits)

def draw():
    """起卦"""
    num1 = random.randint(1, 99)
    num2 = random.randint(1, 99)
    num3 = random.randint(1, 99)

    upper = get_trigram(num1)
    lower = get_trigram(num2)
    yao_pos = get_yao_position(num3)

    hex_info = HEXAGRAMS.get((upper, lower), ("未知卦", 0))
    new_upper, new_lower = change_yao(upper, lower, yao_pos)
    changed_info = HEXAGRAMS.get((new_upper, new_lower), ("未知卦", 0))

    return {
        "upper": upper, "lower": lower,
        "hex_name": hex_info[0], "hex_num": hex_info[1],
        "yao_pos": yao_pos, "yao_name": YAO_NAMES[yao_pos - 1],
        "changed_name": changed_info[0]
    }

def format_result(result):
    """格式化输出"""
    lines = ["=== 易经 ==="]
    lines.append(f"本卦：{result['hex_name']}")
    lines.append(f"变爻：{result['yao_name']}")
    lines.append(f"之卦：{result['changed_name']}")
    return "\n".join(lines)
