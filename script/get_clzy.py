import re
import json
with open('clzy.html','r',encoding='utf-8') as IN,open('词林新韵.json', 'w', encoding='utf-8') as json_file:
    data= IN.readlines()
    all_class = []
    all_word = []
    json_list  = []
    for i in data:
        class_ = re.findall(r"y=\"(.*)\">",i)
        word_= re.findall(r">([一-龥])<",i)
        if len(class_)>0:
            all_class.append(class_[0])
        if len(word_)>0:
            all_word.append(word_)

    poetry_dict = dict(zip(all_class,all_word))

    for key, value in poetry_dict.items():
        part, tone = key[:-2], key[-2:]
        if not json_list or json_list[-1].get(part) is None:
            json_list.append({part: {tone: value}})
        else:
            json_list[-1][part][tone] = value
    json.dump(json_list, json_file, ensure_ascii=False, indent=4)


