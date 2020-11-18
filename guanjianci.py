import jieba
import traceback
import pandas as pd


def getmainword():
    with open(r"C:\Users\X250\Desktop\5g长尾词\关键词.txt", 'r') as f_word:
        return [word.strip("\n") for word in f_word.readlines()]


def qieci(kw_list):
    word_dict_list = []
    for item in kw_list:
        jieba.add_word("物联网")
        ci = jieba.lcut(item)
        ai = list(filter(lambda x: x != " ", ci))
        if len(ai) > 0:
            for lword in ai:
                if lword != "5g":
                    # word_dict ={}
                    # word_dict[lword] = item
                    # word_dict_list.append(word_dict)
                    word_dict_list.append(lword)
    return word_dict_list


def save_to_txt(my_list):
    try:
        with open(r"C:\Users\X250\Desktop\5g长尾词\结果.txt", "w") as f:
            f.write(str(my_list))
            print("结束")
    except:
        traceback.print_exc()


def find_and_opencsv(filename_list):
    keyword_list = []
    for filename in filename_list:
        word_dict = {}
        try:
            col = ["关键词", "搜索结果", "PC日检索量(VIP特权数据)", "移动日检索量(VIP特权数据)"]
            col_a = ["PC日检索量(VIP特权数据)", "移动日检索量(VIP特权数据)"]
            file = pd.read_csv(rf"C:\Users\X250\Desktop\5g长尾词\{filename}.csv",
                               sep=',',
                               encoding="gb2312",
                               na_values="-")

            file.fillna(0, inplace=False)
            result_a = file[col].sort_values(by="移动日检索量(VIP特权数据)",
                                             ascending=False).head(30)
            result_b = list(result_a["关键词"])
            word_dict[filename] = result_b
            keyword_list.append(word_dict)
        except:
            continue
    print(keyword_list)
    return keyword_list


if __name__ == "__main__":
    word_list = getmainword()
    file_list = qieci(word_list)
    m_list = find_and_opencsv(file_list)
    save_to_txt(m_list)