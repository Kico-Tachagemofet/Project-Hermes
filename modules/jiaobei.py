#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""筊杯模块"""

import random

def draw():
    """掷筊"""
    cup1 = random.choice(['Yin', 'Yang'])
    cup2 = random.choice(['Yin', 'Yang'])

    if cup1 != cup2:
        result = "HOLY_CUP"
        result_cn = "圣杯（确认）"
    elif cup1 == 'Yang':
        result = "LAUGHING_CUP"
        result_cn = "笑杯（有保留）"
    else:
        result = "YIN_CUP"
        result_cn = "阴杯（否定）"

    return {
        "cup1": cup1, "cup2": cup2,
        "result": result, "result_cn": result_cn
    }

def format_result(result):
    """格式化输出"""
    return f"=== 筊杯 ===\n{result['cup1']}/{result['cup2']} -- {result['result_cn']}"
