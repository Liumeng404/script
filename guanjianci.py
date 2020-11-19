import jieba
import traceback
import pandas as pd
from aip import AipNlp
import ast
import time
import csv

# def baidu_nlp():
#     api_key = "SZGMoWG2MKNgW3GClgqWPKlw"
#     secret_key = "voAjVVKlHijMtX5lVKb8jxzYhNyQGQol"
#     host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'

#     response = requests.get(host)
#     if response:
#         result = response.json()
#         access_token = result["access_token"]

#     return access_token


def get_baidu_result(text_1, text_2):
    """ 你的 APPID AK SK """
    APP_ID = '23006256'
    API_KEY = 'SZGMoWG2MKNgW3GClgqWPKlw'
    SECRET_KEY = 'voAjVVKlHijMtX5lVKb8jxzYhNyQGQol'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    text1 = text_1

    text2 = text_2
    """ 调用短文本相似度 """
    result = client.simnet(text1, text2)
    return result["score"]


def getmainword():
    with open(r"C:\Users\X250\Desktop\5g长尾词\关键词.txt", "r") as f_word:
        return [word.strip("\n") for word in f_word.readlines()]


def get_list_dict():
    with open(r"C:\Users\X250\Desktop\结果.txt", "r") as f:
        result = f.readline()
        result_list = ast.literal_eval(result)
        return result_list


def get_words(word_list):
    save_words = []
    for item in word_list:
        for key, value in item.items():
            length = len(value)
            keep_word_dict = {}
            keep_word = []
            for i in range(length - 1):
                simiar = get_baidu_result(value[i], value[i + 1])
                print(
                    f"关键词: {value[i]} \n 关键词：{value[i+1]} \n 相似度：{simiar} \n ========="
                )
                if simiar < 0.9:
                    keep_word.append(value[i + 1])
                time.sleep(1)
            keep_word_dict[key] = keep_word

    save_words.append(keep_word_dict)


def qieci(kw_list):
    word_dict_list = []
    for item in kw_list:
        jieba.add_word("物联网")
        ci = jieba.lcut(item)
        ai = list(filter(lambda x: x != " ", ci))
        if len(ai) > 0:
            for lword in ai:
                if lword != "5g":
                    word_dict_list.append(lword)
    return word_dict_list


def save_to_txt(my_list, base_path):
    try:
        with open(base_path, "w") as f:
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


def save_to_csv(your_list):
    filepath = r"C:\Users\X250\Desktop\最终要的数据.csv"
    try:
        with open(filepath, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["主词", "长尾词"])
            for item in w_list:
                for key, value in item.items():
                    for value_item in value:
                        writer.writerow([key, value_item])
                        print(f">>>> {key},{value_item}")
        print("保持完毕")
    except:
        traceback.print_exc()
        print("保存失败")


if __name__ == "__main__":
    # word_list = getmainword()
    # file_list = qieci(word_list)
    # m_list = find_and_opencsv(file_list)
    # save_to_txt(m_list)
    w_list = get_list_dict()
    my_list = get_words(w_list)
    # path = r"C:\Users\X250\Desktop\temp_word.txt"
    save_to_csv(my_list)
    # save_to_txt(str(my_list), path)