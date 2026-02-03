#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字五行计算工具
根据出生时间计算婴儿的八字和五行属性
使用 lunar_python 库进行准确的八字计算
"""

from datetime import datetime
import json

try:
    from lunar_python import Solar
    LUNAR_AVAILABLE = True
except ImportError:
    LUNAR_AVAILABLE = False
    print("警告: lunar_python 库未安装，将使用简化算法")
    print("建议安装: pip install lunar-python")

# 天干五行
TIANGAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 地支五行
DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 地支藏干（简化版，只列主气）
DIZHI_CANGGAN = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'], '卯': ['乙'],
    '辰': ['戊', '乙', '癸'], '巳': ['丙', '戊', '庚'], '午': ['丁', '己'], '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'], '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

# 六十甲子纳音对照表
NAYIN_TABLE = {
    '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火',
    '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土',
    '壬申': '剑锋金', '癸酉': '剑锋金', '甲戌': '山头火', '乙亥': '山头火',
    '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土',
    '庚辰': '白蜡金', '辛巳': '白蜡金', '壬午': '杨柳木', '癸未': '杨柳木',
    '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
    '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木',
    '壬辰': '长流水', '癸巳': '长流水', '甲午': '沙中金', '乙未': '沙中金',
    '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
    '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
    '甲辰': '覆灯火', '乙巳': '覆灯火', '丙午': '天河水', '丁未': '天河水',
    '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金',
    '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水',
    '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火',
    '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
}

# 纳音五行对照表
NAYIN_WUXING = {
    '海中金': '金', '炉中火': '火', '大林木': '木', '路旁土': '土', '剑锋金': '金',
    '山头火': '火', '涧下水': '水', '城头土': '土', '白蜡金': '金', '杨柳木': '木',
    '泉中水': '水', '屋上土': '土', '霹雳火': '火', '松柏木': '木', '长流水': '水',
    '沙中金': '金', '山下火': '火', '平地木': '木', '壁上土': '土', '金箔金': '金',
    '覆灯火': '火', '天河水': '水', '大驿土': '土', '钗钏金': '金', '桑柘木': '木',
    '大溪水': '水', '沙中土': '土', '天上火': '火', '石榴木': '木', '大海水': '水'
}

def calculate_bazi(year, month, day, hour):
    """
    计算八字

    参数:
        year: 出生年份（公历）
        month: 出生月份（1-12）
        day: 出生日期（1-31）
        hour: 出生小时（0-23）

    返回:
        八字信息字典
    """
    if LUNAR_AVAILABLE:
        return calculate_bazi_with_lunar(year, month, day, hour)
    else:
        return calculate_bazi_fallback(year, month, day, hour)

def calculate_bazi_with_lunar(year, month, day, hour):
    """使用 lunar_python 库计算八字（推荐）"""
    try:
        # 创建日期时间对象
        birth_datetime = datetime(year, month, day, hour)

        # 使用 lunar_python 计算
        solar = Solar.fromDate(birth_datetime)
        lunar = solar.getLunar()

        # 获取四柱干支
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        hour_gz = lunar.getTimeInGanZhi()

        bazi = {
            'year': year_gz,
            'month': month_gz,
            'day': day_gz,
            'hour': hour_gz
        }

        return bazi
    except Exception as e:
        print(f"lunar_python 计算失败: {e}，使用备用方法")
        return calculate_bazi_fallback(year, month, day, hour)

def calculate_bazi_fallback(year, month, day, hour):
    """备用的简化八字计算方法"""
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

    date_obj = datetime(year, month, day, hour)

    # 计算年干支
    base_year = 1984  # 甲子年
    offset = (year - base_year) % 60
    year_gz = TIANGAN[offset % 10] + DIZHI[offset % 12]

    # 计算月干支（简化）
    year_tg_index = (year - 4) % 10
    month_tg_index = (year_tg_index * 2 + month) % 10
    month_dz_index = (month + 1) % 12
    month_gz = TIANGAN[month_tg_index] + DIZHI[month_dz_index]

    # 计算日干支
    base_date = datetime(2000, 1, 1)  # 庚辰日
    base_ganzhi = 16
    days_diff = (date_obj - base_date).days
    ganzhi_index = (base_ganzhi + days_diff) % 60
    day_gz = TIANGAN[ganzhi_index % 10] + DIZHI[ganzhi_index % 12]

    # 计算时干支
    day_tg_index = TIANGAN.index(day_gz[0])
    hour_dz_index = (hour + 1) // 2 % 12
    hour_tg_index = (day_tg_index * 2 + hour_dz_index) % 10
    hour_gz = TIANGAN[hour_tg_index] + DIZHI[hour_dz_index]

    bazi = {
        'year': year_gz,
        'month': month_gz,
        'day': day_gz,
        'hour': hour_gz
    }

    return bazi

def get_nayin(ganzhi):
    """
    根据干支获取纳音

    参数:
        ganzhi: 干支组合，如"甲子"

    返回:
        纳音名称，如"海中金"
    """
    return NAYIN_TABLE.get(ganzhi, '')

def get_nayin_wuxing(nayin):
    """
    根据纳音获取五行

    参数:
        nayin: 纳音名称，如"海中金"

    返回:
        五行属性，如"金"
    """
    return NAYIN_WUXING.get(nayin, '')

def analyze_wuxing(bazi):
    """
    分析八字的五行属性

    返回:
        五行统计信息
    """
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}

    # 统计天干五行
    for pillar in ['year', 'month', 'day', 'hour']:
        gz = bazi[pillar]
        tg = gz[0]
        dz = gz[1]

        # 天干
        wuxing_count[TIANGAN_WUXING[tg]] += 1

        # 地支
        wuxing_count[DIZHI_WUXING[dz]] += 1

        # 地支藏干（简化，只算主气）
        canggan = DIZHI_CANGGAN[dz]
        if canggan:
            wuxing_count[TIANGAN_WUXING[canggan[0]]] += 0.5

    # 找出缺失和偏弱的五行
    missing = [wx for wx, count in wuxing_count.items() if count == 0]
    weak = [wx for wx, count in wuxing_count.items() if 0 < count < 1.5]
    strong = [wx for wx, count in wuxing_count.items() if count >= 3]

    return {
        'count': wuxing_count,
        'missing': missing,
        'weak': weak,
        'strong': strong,
        'day_master': TIANGAN_WUXING[bazi['day'][0]]  # 日主五行
    }

def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='计算八字和五行属性')
    parser.add_argument('year', type=int, help='出生年份（公历）')
    parser.add_argument('month', type=int, help='出生月份（1-12）')
    parser.add_argument('day', type=int, help='出生日期（1-31）')
    parser.add_argument('hour', type=int, help='出生小时（0-23）')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')

    args = parser.parse_args()

    bazi = calculate_bazi(args.year, args.month, args.day, args.hour)
    wuxing = analyze_wuxing(bazi)

    # 计算纳音信息
    nayin_info = {
        'year_nayin': get_nayin(bazi['year']),
        'year_nayin_wuxing': get_nayin_wuxing(get_nayin(bazi['year'])),
        'month_nayin': get_nayin(bazi['month']),
        'day_nayin': get_nayin(bazi['day']),
        'hour_nayin': get_nayin(bazi['hour'])
    }

    result = {
        'bazi': bazi,
        'nayin': nayin_info,
        'wuxing': wuxing
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        year_nayin = nayin_info['year_nayin']
        year_nayin_wx = nayin_info['year_nayin_wuxing']
        print(f"\n八字: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}")
        print(f"年柱纳音: {year_nayin} ({year_nayin_wx})")
        print(f"日主: {wuxing['day_master']}")
        print(f"\n五行统计:")
        for wx, count in wuxing['count'].items():
            print(f"  {wx}: {count}")
        if wuxing['missing']:
            print(f"\n缺失五行: {', '.join(wuxing['missing'])}")
        if wuxing['weak']:
            print(f"偏弱五行: {', '.join(wuxing['weak'])}")
        if wuxing['strong']:
            print(f"偏强五行: {', '.join(wuxing['strong'])}")

if __name__ == '__main__':
    main()
