import os
import sys
import platform
from datetime import datetime
from collections import defaultdict

class HomeworkSystem:
    def __init__(self):
        self.names = {}
        self.homework_stats = defaultdict(int)
        self.total_required = 0  # 初始化为0
        self.report_dir = "StatisticsResult"
        self._init_console_encoding()
        self.load_names()

    def _init_console_encoding(self):
        """处理不同系统的控制台编码问题"""
        if sys.platform == 'win32':
            try:
                from ctypes import windll
                windll.kernel32.SetConsoleOutputCP(65001)
                windll.kernel32.SetConsoleCP(65001)
            except Exception as e:
                print("警告：无法设置控制台编码，建议使用现代终端")

    def load_names(self):
        """兼容全平台的名单加载"""
        try:
            file_path = os.path.join(os.getcwd(), "NameList.txt")
            with open(file_path, "rb") as f:
                content = f.read().decode('utf-8-sig').splitlines()

            for line in content:
                line = line.strip()
                if not line:
                    continue
                
                if '\t' in line:
                    parts = line.split('\t', 1)
                else:
                    parts = line.split(maxsplit=1)
                
                student_id = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else ""
                self.names[student_id] = name
                
        except IOError as e:
            print("名单加载失败: {}".format(str(e)))
            sys.exit(1)

    def show_menu(self):
        """增强型菜单系统"""
        while True:
            print("\n" + "="*50)
            print("作业登记系统（当前总次数：{}）".format(
                self.total_required if self.total_required > 0 else "未设置"
            ))
            print("="*50)
            print("1. 设置/修改总应交次数")
            print("2. 批量登记缺交")
            print("3. 查看实时统计")
            print("4. 生成统计报告")
            print("Q. 保存退出")
            choice = input("请选择操作：").strip().upper()

            if choice == '1':
                self.set_total_required()
            elif choice == '2':
                if not self.check_required_set():
                    continue
                self.record_loop()
            elif choice == '3':
                if not self.check_required_set():
                    continue
                self.display_enhanced_stats()
                input("\n按回车返回主菜单...")
            elif choice == '4':
                self.generate_report()
                input("\n按回车返回主菜单...")
            elif choice == 'Q':
                self.generate_report()
                print("\n最终报告路径：{}".format(
                    os.path.abspath(self.report_dir).replace("\\", "/")))
                break
            else:
                print("无效输入，请重新输入1-4或Q")
                input("按回车继续...")

    def check_required_set(self):
        """检查总次数是否已设置"""
        if self.total_required <= 0:
            print("错误：请先设置总应交次数！")
            return False
        return True

    def set_total_required(self):
        """独立的总次数设置方法"""
        while True:
            input_str = input("请输入总应交次数（输入Q返回）: ").strip()
            if input_str.upper() == 'Q':
                return
            
            try:
                new_total = int(input_str)
                if new_total <= 0:
                    print("错误：次数必须大于0")
                    continue
                
                # 保留原有数据时需要确认
                if self.total_required > 0 and len(self.homework_stats) > 0:
                    confirm = input("当前已有登记数据，确定要修改总次数吗？(Y/N): ").lower()
                    if confirm != 'y':
                        return
                
                self.total_required = new_total
                print("总次数已更新为：", self.total_required)
                return
            except ValueError:
                print("错误：请输入有效数字")

    def record_loop(self):
        """新版数据录入循环"""
        print("\n"+ "="*50)
        print("作业登记系统（输入Q退出）")
        print("="*50)
        
        while True:
            # 输入学号阶段
            student_id = input("\n请输入学生学号（输入Q结束）: ").strip().upper()
            if student_id == 'Q':
                break
            
            # 验证学号
            if student_id not in self.names:
                print("错误：无效的学生学号")
                continue
                
            # 输入缺交次数
            missed = input("请输入缺交次数（输入Q结束）: ").strip().upper()
            if missed == 'Q':
                break
            
            try:
                missed = int(missed)
                if missed < 0:
                    print("错误：次数不能为负数")
                    continue
                if missed > self.total_required:
                    print(f"错误：缺交次数不能超过总次数（{self.total_required}次）")
                    continue
                    
                self.homework_stats[student_id] = missed
                print("成功记录：{} 缺交{}次".format(self.names[student_id], missed))
                
            except ValueError:
                print("错误：请输入有效数字")

    def display_enhanced_stats(self):
        """增强统计显示"""
        print("\n{:=^50}".format(" 实时统计 "))
        print("{:<12}{:<10}{:<12}{:<10}{:<12}".format(
            '学号', '姓名', '缺交次数', '缺交率', '状态'))
        
        if not self.homework_stats:
            print("\n{:^50}".format("暂无缺交记录"))
            return

        for sid, missed in sorted(self.homework_stats.items(),
                                key=lambda x: x[1], reverse=True):
            rate = missed / self.total_required * 100
            status = "严重缺交" if rate >= 20 else "需关注" if rate >= 10 else "正常"
            print("{:<12}{:<10}{:<12}{:<10.1f}% {:<12}".format(
                sid,
                self.names.get(sid, '未知'),
                missed,
                rate,
                status))
        
        print("\n统计摘要：")
        print("- 总应交次数：{}".format(self.total_required))
        print("- 登记人数：{}/{}".format(
            len(self.homework_stats), 
            len(self.names)))
        print("- 平均缺交率：{:.1f}%".format(
            sum(self.homework_stats.values())/self.total_required/len(self.homework_stats)*100 
            if self.homework_stats else 0))

    def generate_report(self):
        """增强版报告生成"""
        try:
            if not os.path.exists(self.report_dir):
                os.makedirs(self.report_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = "{}_Report.txt".format(timestamp)
            file_path = os.path.join(self.report_dir, filename)
            
            sorted_stats = sorted(self.homework_stats.items(),
                                key=lambda x: x[1], reverse=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("作业统计报告\n")
                f.write("生成时间: {}\n".format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                f.write("总应交次数: {}\n".format(self.total_required))
                f.write("-"*60 + "\n")
                f.write("{:<10}{:<10}{:<12}{:<10}\n".format(
                    '学号', '姓名', '缺交次数', '缺交率'))
                
                for sid, missed in sorted_stats:
                    rate = (missed / self.total_required) * 100
                    f.write("{:<10}{:<10}{:<12}{:.1f}%\n".format(
                        sid,
                        self.names.get(sid, '未知'),
                        missed,
                        rate))
                        
            print("报告已生成: {}".format(
                os.path.abspath(file_path).replace("\\", "/")))
            
        except Exception as e:
            print("报告生成失败: {}".format(str(e)))

if __name__ == "__main__":
    # 环境检查
    if sys.version_info < (3, 0):
        print("需要Python 3.0或更高版本")
        sys.exit(1)
        
    # macOS特殊处理
    if sys.platform == 'darwin':
        os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    
    try:
        system = HomeworkSystem()
        system.show_menu()
    except KeyboardInterrupt:
        print("\n程序已中断")
