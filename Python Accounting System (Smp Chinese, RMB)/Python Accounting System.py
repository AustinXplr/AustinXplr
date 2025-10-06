import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import matplotlib
import numpy as np

# 设置中文字体支持
def set_chinese_font():
    try:
        # 尝试使用系统支持的中文字体
        if matplotlib.get_backend().lower() != 'agg':  # 只在需要显示时设置
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except:
        pass  # 如果设置失败，继续使用默认字体

# 创建必要的文件夹
def create_folders():
    log_dir = "Logs"
    charts_dir = "Charts"
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    return os.path.join(log_dir, "expense_log.txt")

# 文件路径
LOG_FILE = create_folders()

# 加载记账数据
def load_expenses():
    expenses = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    date, amount = parts
                    expenses[date] = float(amount)
    return expenses

# 保存记账数据
def save_expenses(expenses):
    with open(LOG_FILE, "w") as f:
        for date, amount in expenses.items():
            f.write(f"{date},{amount:.2f}\n")

# 添加记账记录
def add_expense():
    date = input("请输入日期（格式YYYY.MM.DD）：")
    try:
        # 验证日期格式
        datetime.datetime.strptime(date, "%Y.%m.%d")
    except ValueError:
        print("日期格式错误！")
        return
    
    try:
        amount = float(input("请输入总支出¥："))
        if amount < 0:  # 允许零支出
            print("金额不能为负数！")
            return
    except ValueError:
        print("金额格式错误！")
        return
    
    expenses = load_expenses()
    expenses[date] = amount
    save_expenses(expenses)
    print("记账明细已添加")

# 查看所有记账记录
def view_expenses():
    expenses = load_expenses()
    
    if not expenses:
        print("暂无记账记录！")
        return
    
    print("\n================\n记账明细\n================")
    print("日期        |支出金额")
    
    # 按日期排序
    sorted_dates = sorted(expenses.keys())
    for date in sorted_dates:
        print(f"{date}|¥{expenses[date]:.2f}")
    
    print("================")
    
    # 询问是否继续
    while True:
        cont = input("是否继续？（Y/N）：").upper()
        if cont == "Y":
            break
        elif cont == "N":
            print("谢谢使用！")
            exit()
        else:
            print("无效输入，请重新输入")

# 修改记账记录
def modify_expense():
    date = input("请输入需要修改的日期（格式YYYY.MM.DD）：")
    
    expenses = load_expenses()
    if date not in expenses:
        print("该日期无记录！")
        return
    
    try:
        new_amount = float(input("请输入修改后的总支出金额¥："))
        if new_amount < 0:  # 允许零支出
            print("金额不能为负数！")
            return
    except ValueError:
        print("金额格式错误！")
        return
    
    expenses[date] = new_amount
    save_expenses(expenses)
    print("修改成功！")

# 删除记账记录
def delete_expense():
    date = input("请输入需要删除的日期（格式YYYY.MM.DD）：")
    
    expenses = load_expenses()
    if date not in expenses:
        print("该日期无记录！")
        return
    
    del expenses[date]
    save_expenses(expenses)
    print("删除成功！")

# 生成可视化图表
def generate_chart():
    try:
        # 获取日期范围
        start_date_str = input("请输入图表的起始日期（格式YYYY.MM.DD）：")
        end_date_str = input("请输入图表的终止日期（格式YYYY.MM.DD）：")
        
        # 转换为日期对象
        start_date = datetime.datetime.strptime(start_date_str, "%Y.%m.%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y.%m.%d")
        
        if start_date > end_date:
            print("起始日期不能晚于终止日期！")
            return
    except ValueError:
        print("日期格式错误！")
        return
    
    # 加载数据
    expenses = load_expenses()
    
    # 创建日期范围内所有日期的列表
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    
    # 为每个日期创建金额列表（包括零支出日期）
    amounts = []
    for date in all_dates:
        date_str = date.strftime("%Y.%m.%d")
        # 如果该日期有记录，使用记录值；否则设为0
        amounts.append(expenses.get(date_str, 0.0))
    
    # 计算平均值（排除零支出日）
    non_zero_amounts = [a for a in amounts if a > 0]
    avg_amount = sum(non_zero_amounts) / len(non_zero_amounts) if non_zero_amounts else 0
    
    # 设置中文字体
    set_chinese_font()
    
    # 创建图表
    plt.figure(figsize=(12, 6))
    
    # 创建新的数据序列以实现垂直线效果
    new_dates = []
    new_amounts = []
    zero_points = []  # 存储零支出点位置
    
    # 处理每个数据点
    for i in range(len(all_dates)):
        date = all_dates[i]
        amount = amounts[i]
        
        # 如果是零支出点
        if amount == 0:
            # 添加到零支出点列表
            zero_points.append((date, 0))
            
            # 添加零值点
            new_dates.append(date)
            new_amounts.append(0)
            
            # 添加后一个点（如果存在）的起始
            if i < len(all_dates) - 1:
                next_amount = amounts[i+1]
                if next_amount > 0:
                    # 添加起始点（相同日期，保持零值）
                    new_dates.append(date)
                    new_amounts.append(0)
        else:
            # 对于非零点，直接添加
            new_dates.append(date)
            new_amounts.append(amount)
    
    # 绘制折线图 - 实现零支出点的垂直线效果
    plt.plot(new_dates, new_amounts, 'b-', label='连接线', linewidth=2)
    
    # 添加非零点标记
    non_zero_dates = [d for d, a in zip(all_dates, amounts) if a > 0]
    non_zero_amounts = [a for a in amounts if a > 0]
    plt.plot(non_zero_dates, non_zero_amounts, 'bo', markersize=8, label='支出点')
    
    # 突出显示零支出点
    if zero_points:
        zero_dates, zero_amounts = zip(*zero_points)
        plt.scatter(zero_dates, zero_amounts, s=120, c='red', marker='o', 
                   edgecolors='black', zorder=4, label='零支出')
    
    # 添加平均值虚线（使用红色虚线）
    plt.axhline(y=avg_amount, color='r', linestyle='--', 
                label=f'平均值: ¥{avg_amount:.2f}', linewidth=1.5)
    
    # 设置图表格式
    plt.title(f"支出折线图 ({start_date_str} 至 {end_date_str})")
    plt.xlabel("日期")
    plt.ylabel("支出金额 (¥)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 设置Y轴范围 - 确保零支出点可见
    if amounts:
        y_min = min(min(amounts), 0) - 10
        y_max = max(max(amounts), 0) + 20
        plt.ylim(y_min, y_max)
    
    # 设置日期格式
    date_format = DateFormatter("%Y.%m.%d")
    plt.gca().xaxis.set_major_formatter(date_format)
    
    # 根据日期数量设置刻度间隔
    num_dates = len(all_dates)
    if num_dates <= 10:
        interval = 1
    else:
        interval = max(1, num_dates // 10)
    
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    plt.gcf().autofmt_xdate()
    
    # 保存图表
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chart_path = os.path.join("Charts", f"{timestamp}.jpg")
    plt.savefig(chart_path, bbox_inches='tight', dpi=150)
    plt.close()
    
    print(f"图表已保存至路径：{os.path.abspath(chart_path)}")            

# 主程序
def main():
    while True:
        print("\n================\nPython记账系统\n================")
        print("请选择操作：")
        print("1.记账")
        print("2.查看所有记账明细")
        print("3.修改记账明细")
        print("4.删除记账明细")
        print("5.生成可视化图表")
        print("q.退出")
        print("================")
        
        choice = input("请选择：")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            modify_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            generate_chart()
        elif choice.lower() == "q":
            print("谢谢使用！")
            break
        else:
            print("无效选择，请重新输入！")

if __name__ == "__main__":
    main()
