#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""占星骰子模块"""

import random

PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
HOUSES = ["1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H"]

RULERSHIPS = {
    "Sun": ["Leo"], "Moon": ["Cancer"], "Mercury": ["Gemini", "Virgo"],
    "Venus": ["Taurus", "Libra"], "Mars": ["Aries", "Scorpio"],
    "Jupiter": ["Sagittarius", "Pisces"], "Saturn": ["Capricorn", "Aquarius"],
    "Uranus": ["Aquarius"], "Neptune": ["Pisces"], "Pluto": ["Scorpio"]
}

DIGNITIES = {
    "Sun": {"dom": ["Leo"], "exa": ["Aries"], "det": ["Libra"], "fall": ["Aquarius"]},
    "Moon": {"dom": ["Cancer"], "exa": ["Taurus"], "det": ["Capricorn"], "fall": ["Scorpio"]},
    "Mercury": {"dom": ["Gemini", "Virgo"], "exa": ["Virgo"], "det": ["Sagittarius", "Pisces"], "fall": ["Pisces"]},
    "Venus": {"dom": ["Taurus", "Libra"], "exa": ["Pisces"], "det": ["Aries", "Scorpio"], "fall": ["Virgo"]},
    "Mars": {"dom": ["Aries", "Scorpio"], "exa": ["Capricorn"], "det": ["Taurus", "Libra"], "fall": ["Cancer"]},
    "Jupiter": {"dom": ["Sagittarius", "Pisces"], "exa": ["Cancer"], "det": ["Gemini", "Virgo"], "fall": ["Capricorn"]},
    "Saturn": {"dom": ["Capricorn", "Aquarius"], "exa": ["Libra"], "det": ["Cancer", "Leo"], "fall": ["Aries"]},
    "Uranus": {"dom": ["Aquarius"], "exa": ["Scorpio"], "det": ["Leo"], "fall": ["Taurus"]},
    "Neptune": {"dom": ["Pisces"], "exa": ["Cancer"], "det": ["Virgo"], "fall": ["Capricorn"]},
    "Pluto": {"dom": ["Scorpio"], "exa": ["Leo"], "det": ["Taurus"], "fall": ["Aquarius"]}
}

def draw():
    """抽取占星骰子"""
    planet = random.choice(PLANETS)
    sign = random.choice(SIGNS)
    house = random.choice(HOUSES)

    # 计算尊贵状态
    status = "neutral"
    if planet in DIGNITIES:
        d = DIGNITIES[planet]
        if sign in d["dom"]: status = "DOMICILE"
        elif sign in d["exa"]: status = "EXALTATION"
        elif sign in d["det"]: status = "DETRIMENT"
        elif sign in d["fall"]: status = "FALL"

    # 计算上升和飞星
    house_num = int(house[:-1])
    sign_idx = SIGNS.index(sign)
    asc_idx = (sign_idx - (house_num - 1)) % 12
    asc_sign = SIGNS[asc_idx]

    ruled_signs = RULERSHIPS.get(planet, [])
    fly_houses = []
    for ruled in ruled_signs:
        ruled_idx = SIGNS.index(ruled)
        fly_house = (ruled_idx - asc_idx + 12) % 12 + 1
        fly_houses.append(f"{fly_house}H")

    fly_str = " & ".join(fly_houses) + f" → {house}" if fly_houses else "N/A"

    return {
        "planet": planet, "sign": sign, "house": house,
        "status": status, "ascendant": asc_sign, "flying_star": fly_str
    }

def format_result(result):
    """格式化输出"""
    lines = ["=== ASTRO DICE ==="]
    lines.append(f"{result['planet']} in {result['sign']} {result['house']} ({result['status']})")
    lines.append(f"Ascendant: {result['ascendant']}")
    lines.append(f"Flying Star: {result['flying_star']}")
    return "\n".join(lines)
