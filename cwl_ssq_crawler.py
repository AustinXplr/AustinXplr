import requests
import numpy as np
from datetime import datetime

class GetData():
    def __init__(self, url, params, headers, data_name):
        self.url = url
        self.params = params
        self.headers = headers
        self.data_name = data_name
        self.data = self.get_data()

    def get_data(self):
        reqs = requests.get(url=self.url, params=self.params, headers=self.headers)
        results = reqs.json()[self.data_name]
        return results

class DataAnalyze(GetData):
    def __init__(self, url, params, headers, data_name):
        super().__init__(url, params, headers, data_name)

    def get_numbers(self):
        datas = {}
        reds = []
        blues = []
        for result in self.data:
            reds.append(result['red'].split(','))
            blues.append(result['blue'])

        datas['red'] = reds
        datas['blue'] = blues
        return datas

    def analysis(self):
        """
        分析每个位置的红球和蓝球的概率。
        """
        data = self.get_numbers()
        red_positions = [{} for _ in range(6)]  # 6个红球位置的概率统计
        blue_count = [0] * 16  # 蓝球的概率统计（1-16）

        # 统计红球每个位置的数字出现次数
        for red_balls in data['red']:
            for i, ball in enumerate(red_balls):  # i表示位置（0-5）
                number = int(ball)
                if number not in red_positions[i]:
                    red_positions[i][number] = 0
                red_positions[i][number] += 1

        # 统计蓝球的出现次数
        for blue_ball in data['blue']:
            blue_count[int(blue_ball) - 1] += 1

        # 按出现次数排序并计算概率
        red_probabilities = []
        for position in red_positions:
            sorted_position = sorted(position.items(), key=lambda x: x[1], reverse=True)
            red_probabilities.append([num for num, _ in sorted_position])

        blue_probabilities = np.argsort(-np.array(blue_count)) + 1  # 按概率从高到低排序

        return red_probabilities, blue_probabilities.tolist()

def fix_duplicates(reds, red_probabilities):
    """
    检查并修正红球号码中的重复值。
    如果出现重复值，通过替换为概率次高的号码修复。
    """
    unique_numbers = set()
    for i, red in enumerate(reds):
        if red not in unique_numbers:
            unique_numbers.add(red)
        else:
            # 当前红球号码重复，寻找概率次高的号码进行替换
            for candidate in red_probabilities[i]:
                if candidate not in unique_numbers:
                    reds[i] = candidate
                    unique_numbers.add(candidate)
                    break
    return reds

def generate_predictions(red_probabilities, blue_probabilities, count):
    """
    根据红球和蓝球的概率，生成指定数量的号码。
    """
    predictions = []
    for i in range(count):  # 根据用户指定的数量生成号码
        red_numbers = []
        for pos in range(6):  # 遍历6个红球位置
            if i < len(red_probabilities[pos]):
                # 如果当前位置的概率列表中有第i高概率的号码
                red_numbers.append(red_probabilities[pos][i])
            else:
                # 如果当前位置的概率列表不足，则循环使用当前位置的号码填充
                red_numbers.append(red_probabilities[pos][i % len(red_probabilities[pos])])
        red_numbers = fix_duplicates(red_numbers, red_probabilities)  # 检查并修正重复值
        blue_number = blue_probabilities[i % len(blue_probabilities)]  # 蓝球也循环选取
        # 将红球和蓝球转换为两位数格式
        predictions.append((["{:02d}".format(num) for num in red_numbers], "{:02d}".format(blue_number)))
    return predictions

def write_predictions_to_file(predictions, issueCount):
    """
    将预测结果写入格式化的txt文件。
    """
    file_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"双色球号码预测_{file_time}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("双色球号码预测\n")
        f.write(f"{file_time}\n")
        f.write(f"根据双色球近 {issueCount} 期的开奖结果分析：\n")
        
        for i, (reds, blue) in enumerate(predictions, start=1):
            f.write(f"预测{i:>2}> 红区 {' '.join(reds)} - 蓝区 {blue}\n")
            if i % 5 == 0 and i != len(predictions):  # 每 5 组后添加分隔符
                f.write("======================================\n")
        
        # 若最后一组不足5个，用占位符填充
        remaining = 5 - (len(predictions) % 5)
        if remaining < 5:  # 如果需要填充
            for j in range(remaining):
                f.write(f"预测{len(predictions) + j + 1:>2}> 红区 -- -- -- -- -- -- - 蓝区 --\n")
    
    print(f"预测结果已保存到文件：{filename}")

def get_total_issues():
    url = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-encoding': 'gzip, deflate, br, zstd',
        'Accept-language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'HMF_CI=0cb594b22cfb81197d998ef7b8d079009ff245fe4eb054cc556876b181043e660c58299c17ad742956450b425b947cd42ddaf47f3c6c0bf577a33f8ee0590a05c8; 21_vq=6',
        'Host': 'www.cwl.gov.cn',
        'Referer': 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/',
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    params = {
        'name': 'ssq',
        'issueCount': '',  # 不指定期数，获取所有数据
        'issueStart': '',
        'issueEnd': '',
        'dayStart': '',
        'dayEnd': '',
    }

    # 发送请求
    reqs = requests.get(url=url, params=params, headers=headers)
    data = reqs.json()

    # 检查可能的字段
    if 'result' in data:
        total_issues = len(data['result'])  # 结果数据的长度
        return total_issues
    else:
        raise ValueError("无法获取双色球总期数，接口返回数据格式可能已更改。")

def run_once(issueCount, predictionCount):
    url = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
    params = {
        'name': 'ssq',
        'issueCount': issueCount,
        'issueStart': '',
        'issueEnd': '',
        'dayStart': '',
        'dayEnd': '',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-encoding': 'gzip, deflate, br, zstd',
        'Accept-language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'HMF_CI=0cb594b22cfb81197d998ef7b8d079009ff245fe4eb054cc556876b181043e660c58299c17ad742956450b425b947cd42ddaf47f3c6c0bf577a33f8ee0590a05c8; 21_vq=6',
        'Host': 'www.cwl.gov.cn',
        'Referer': 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/',
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    lottery = DataAnalyze(url, params, headers, 'result')
    red_probabilities, blue_probabilities = lottery.analysis()

    # 生成预测号码
    predictions = generate_predictions(red_probabilities, blue_probabilities, predictionCount)

    # 输出预测结果到文件
    write_predictions_to_file(predictions, issueCount)

def main_loop():
    print("双色球号码预测")
    print("预测结果不保证完全准确，请理性购彩")
    while True:
        try:
            issueCount = input("要根据最近多少期的开奖结果进行分析？（输入 'A' 获取所有历史期数）")
            if issueCount.strip() == '0':
                print("无法运行，请重试！")
                continue
            if issueCount.strip().upper() == 'A':
                issueCount = get_total_issues()
                print(f"双色球当前总期数为：{issueCount}")
            else:
                issueCount = int(issueCount.strip())

            predictionCount = int(input("要预测多少个号码？").strip())
            if predictionCount <= 0:
                print("预测号码数量必须大于0，请重试！")
                continue

            run_once(issueCount, predictionCount)
            break
        except Exception as e:
            print(f"发生错误：{e}，请重试！")

if __name__ == '__main__':
    main_loop()
