import json
import pandas as pd
import re
import argparse
import os
from typing import Tuple, List, Dict, Any, Optional

def build_tone_dict(rhymebook_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    将韵书数据预处理为字到平仄的映射字典。
    """
    tone_dict = {}
    for item in rhymebook_data:
        for key, value in item.items():
            for word in value.get('平', []):
                tone_dict[word] = '平'
            for word in value.get('仄', []):
                tone_dict[word] = '仄'
    return tone_dict

def load_rhymebook(rhymebook_choice: str) -> Dict[str, str]:
    """
    加载韵书文件并返回平仄字典。
    """
    rhymebook_map = {
        '1': '../data/词林正韵.json',
        '2': '../data/中华新韵.json'
    }
    rhymebook_path = rhymebook_map.get(rhymebook_choice, '../data/词林正韵.json')
    if not os.path.exists(rhymebook_path):
        raise FileNotFoundError(f"韵书文件未找到: {rhymebook_path}")
    with open(rhymebook_path, 'r', encoding='utf-8') as f:
        rhymebook_data = json.load(f)
    return build_tone_dict(rhymebook_data)

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

def mark_tone(text: str, tone_dict: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    标注文本每个字的平仄属性。
    """
    tone_text = []
    for word in text:
        pz = tone_dict.get(word, None)
        if pz:
            tone_text.append((word, pz))
        else:
            tone_text.append((word, '未知'))
    return tone_text

def get_score_tone(
    tone_text: List[Tuple[str, str]], tone_database: List[str]
) -> Tuple[float, List[Tuple[Tuple[str, str], str]]]:
    """
    计算平仄得分，并找出不合平仄的字。
    """
    score = 0
    issue_data = []
    for item1, item2 in zip(tone_text, tone_database):
        if item1[1] != item2 and item2 != '中':
            issue_data.append((item1, item2))
        elif item1[1] == item2 or item2 == '中':
            score += 1
    total = len(tone_database)
    score_percent = (score / total * 100) if total else 0
    return score_percent, issue_data

def estimate_poetry(
    text: str, rhymebook: str, cipai: str
) -> Tuple[Optional[str], float, List[Tuple[Tuple[str, str], str]]]:
    """
    综合分析诗词文本，返回词牌名、平仄得分、不合平仄字。
    """
    try:
        tone_dict = load_rhymebook(rhymebook)
        cipai_data = load_cipai(cipai)
    except Exception as e:
        print(f"加载数据文件出错: {e}")
        return None, 0, []

    text_drop, length, split_length = preprocess_text(text)
    guess_cipai, tone_database = guess_cipai_name(length, split_length, cipai_data)

    if not tone_database:
        print("未能匹配到词牌名，请检查输入文本或词牌谱数据。")
        return None, 0, []

    # 只保留汉字的平仄规则
    tone_database = re.sub("[^\u4e00-\u9fa5]", "", tone_database)
    tone_database = list(re.sub(r"增韵", "", tone_database))
    tone_text = mark_tone(text_drop, tone_dict)
    score, issue_data = get_score_tone(tone_text, tone_database)
    return guess_cipai, score, issue_data

def main():
    parser = argparse.ArgumentParser(
        description="自动分析古诗词的词牌名和平仄合规性。",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-y", "--rhymebook", type=str, required=False, help="1:词林正韵;2:中华新韵")
    parser.add_argument("-p", "--cipai", type=str, required=False, help="1:钦定词谱;2:唐宋词格律")
    parser.add_argument("-t", "--text", type=str, required=False, help="输入要分析的诗词文本")
    args = parser.parse_args()

    text = args.text or "君王著意履声间。便令押、紫宸班。今代又尊韩。道吏部、文章泰山。一杯千岁，问公何事，早伴赤松闲。功业后来看。似江左、风流谢安。"
    guess_cipai, score, issues = estimate_poetry(text, args.rhymebook or '1', args.cipai or '1')

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