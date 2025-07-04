import json
import pandas as pd
import re
import argparse
import os
from typing import Tuple, List, Dict, Any, Optional

def build_pingze_dict(ciyun_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    将韵书数据预处理为字到平仄的映射字典。
    """
    pingze_dict = {}
    for item in ciyun_data:
        for key, value in item.items():
            for word in value.get('平', []):
                pingze_dict[word] = '平'
            for word in value.get('仄', []):
                pingze_dict[word] = '仄'
    return pingze_dict

def load_ciyun(ciyun_choice: str) -> Dict[str, str]:
    """
    加载韵书文件并返回平仄字典。
    """
    ciyun_map = {
        '1': '../data/词林正韵.json',
        '2': '../data/中华新韵.json'
    }
    ciyun_path = ciyun_map.get(ciyun_choice, '../data/词林正韵.json')
    if not os.path.exists(ciyun_path):
        raise FileNotFoundError(f"韵书文件未找到: {ciyun_path}")
    with open(ciyun_path, 'r', encoding='utf-8') as f:
        ciyun_data = json.load(f)
    return build_pingze_dict(ciyun_data)

def load_cipai(cipai_choice: str) -> pd.DataFrame:
    """
    加载词牌谱文件并返回DataFrame。
    """
    cipai_map = {
        '1': '../data/cipai_with_statistics_qdcp.csv',
        '2': '../data/cipai_with_statistics_tscgl.csv'
    }
    cipai_path = cipai_map.get(cipai_choice, '../data/cipai_with_statistics_tscgl.csv')
    if not os.path.exists(cipai_path):
        raise FileNotFoundError(f"词牌谱文件未找到: {cipai_path}")
    return pd.read_csv(cipai_path)

def preprocess_text(text: str) -> Tuple[str, int, List[int]]:
    """
    只保留汉字，统计总字数和分句字数。
    """
    text_drop = re.sub("[^\u4e00-\u9fa5]", "", text)
    length = len(text_drop)
    split_length = [len(i) for i in re.split('[，。、？！]', text) if i]
    return text_drop, length, split_length

def guess_cipai_name(
    length: int, split_length: List[int], cipai_data: pd.DataFrame
) -> Tuple[Optional[str], Optional[str]]:
    """
    根据总字数和分句字数猜测词牌名及其平仄规则。
    """
    for row in cipai_data.itertuples():
        try:
            if length == getattr(row, '总数') and str(split_length) == getattr(row, '分段字数'):
                return getattr(row, '词牌名'), getattr(row, '韵律')
        except Exception:
            continue
    return None, None

def mark_pingze(text: str, pingze_dict: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    标注文本每个字的平仄属性。
    """
    pingze_text = []
    for word in text:
        pz = pingze_dict.get(word, None)
        if pz:
            pingze_text.append((word, pz))
        else:
            pingze_text.append((word, '未知'))
    return pingze_text

def score_pingze(
    pingze_text: List[Tuple[str, str]], pingze_database: List[str]
) -> Tuple[float, List[Tuple[Tuple[str, str], str]]]:
    """
    计算平仄得分，并找出不合平仄的字。
    """
    score = 0
    issue_data = []
    for item1, item2 in zip(pingze_text, pingze_database):
        if item1[1] != item2 and item2 != '中':
            issue_data.append((item1, item2))
        elif item1[1] == item2 or item2 == '中':
            score += 1
    total = len(pingze_database)
    score_percent = (score / total * 100) if total else 0
    return score_percent, issue_data

def estimate_poetry(
    text: str, ciyun: str, cipai: str
) -> Tuple[Optional[str], float, List[Tuple[Tuple[str, str], str]]]:
    """
    综合分析诗词文本，返回词牌名、平仄得分、不合平仄字。
    """
    try:
        pingze_dict = load_ciyun(ciyun)
        cipai_data = load_cipai(cipai)
    except Exception as e:
        print(f"加载数据文件出错: {e}")
        return None, 0, []

    text_drop, length, split_length = preprocess_text(text)
    guess_cipai, pingze_database = guess_cipai_name(length, split_length, cipai_data)

    if not pingze_database:
        print("未能匹配到词牌名，请检查输入文本或词牌谱数据。")
        return None, 0, []

    # 只保留汉字的平仄规则
    pingze_database = re.sub("[^\u4e00-\u9fa5]", "", pingze_database)
    pingze_database = list(re.sub(r"增韵", "", pingze_database))
    pingze_text = mark_pingze(text_drop, pingze_dict)
    score, issue_data = score_pingze(pingze_text, pingze_database)
    return guess_cipai, score, issue_data

def main():
    parser = argparse.ArgumentParser(
        description="自动分析古诗词的词牌名和平仄合规性。",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-y", "--ciyun", type=str, required=False, help="1:词林正韵;2:中华新韵")
    parser.add_argument("-p", "--cipai", type=str, required=False, help="1:钦定词谱;2:唐宋词格律")
    parser.add_argument("-t", "--text", type=str, required=False, help="输入要分析的诗词文本")
    args = parser.parse_args()

    text = args.text or "仄平平仄仄，仄仄仄、平平平仄。仄平仄平，平平平仄仄。仄仄平仄。仄仄平平仄，仄平平仄，去仄平平仄。平平仄仄平平仄。仄仄平平，平平仄仄。平平仄平平仄。仄平平仄仄，平仄平仄。平平平仄。去平平仄仄。仄仄平平仄，平仄仄。平平仄仄平仄。仄平平仄仄，仄平平仄。平平仄、仄平平仄。平仄仄、仄仄平平仄仄，仄平平仄。平平仄、仄仄平仄。仄仄平、仄仄平平仄，平平仄仄。"
    guess_cipai, score, issues = estimate_poetry(text, args.ciyun or '1', args.cipai or '1')

    print(f"\n分析结果:")
    print(f"输入文本：{text}")
    if guess_cipai:
        print(f"词牌名为：{guess_cipai}")
        print(f"平仄打分：{score:.2f}")
        if issues:
            print("不合平仄的字及应为的平仄：")
            for (word, actual), expected in issues:
                print(f"  字：{word} 实际：{actual} 应为：{expected}")
        else:
            print("全部平仄合规！")
    else:
        print("未能识别词牌名，无法评分。")

if __name__ == "__main__":
    main()