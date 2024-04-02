import json
import pandas as pd
import re
import argparse

def estimate_poetry(text,ciyun,cipai):
    if ciyun=='1':
        ciyun = '../data/词林正韵.json'
    elif ciyun=='2':
        ciyun = '../data/中华新韵.json'
    else:
        ciyun = '../data/词林正韵.json'
    ciyun_json = open(ciyun, 'r', encoding='utf-8')
    ciyun_data = json.load(ciyun_json)

    if cipai =='1':
        cipai = '../data/cipai_with_statistics_qdcp.csv'
    elif cipai =='2':
        cipai = '../data/cipai_with_statistics_tscgl.csv'
    else:
        cipai = '../data/cipai_with_statistics_tscgl.csv'
    cipai_data = pd.read_csv(cipai)


    text_drop = re.sub("[^\u4e00-\u9fa5]", "", text)
    length = len(text_drop)
    split_length = [len(i) for i in re.split('，|。|、',text) if i]
    guess_cipai=''
    pingze_database = ''
    for index, cipai in cipai_data.iterrows():
        if length == cipai['总数'] and str(split_length) == cipai['分段字数']:
            guess_cipai = cipai['词牌名']
            pingze_database = cipai['韵律']
    
    pingze_database=  list(re.sub("[^\u4e00-\u9fa5]", "", pingze_database))

    pingze_text = []
    for word in text_drop:
        for item in ciyun_data:
            for key, value in item.items():
                if word in value['平']:
                    pingze_text.append((word,'平'))
                    break
                elif word in value['仄']:
                    pingze_text.append((word,'仄'))
                    break
            else:
                continue
            break

    score = 0
    issue_data = []
    if guess_cipai:
        for item1, item2 in zip(pingze_text,pingze_database):
            if item1[1]!=item2 and item2!='中':
                issue_data.append((item1, item2))
            elif item1[1]==item2 or item2=='中':
                score+=1
        score= score/length*100
    else:
        pass
    ciyun_json.close()
    return guess_cipai,score,issue_data


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-y", action="store", dest="ciyun", required=False,help="1:词林正韵;2:中华新韵")
    parser.add_argument("-p", action="store", dest="cipai",required=False,help="1:钦定词谱;2:唐宋词格律")
    args = parser.parse_args()

    text = "云气上林梢，毕竟非空非色。风景不随人去，到而今留得。老无情味到篇章，诗债怕人索。却笑近来林下，有许多词客。"
    guess_cipai = estimate_poetry(text,args.ciyun,args.cipai)
    print(f"词牌名为： {guess_cipai[0]}\n平仄打分： {guess_cipai[1]:.2f}")
    for i in guess_cipai[2]:
        print(f"不合平仄字： {i} ")

if __name__ == "__main__":
    main()