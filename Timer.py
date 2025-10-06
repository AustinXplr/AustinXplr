import tkinter as tk
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("计时器")
        self.root.configure(bg='white')
        self.root.geometry("800x400")
        
        # 设置窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"800x400+{x}+{y}")
        
        # 创建提示标签
        self.instruction = tk.Label(
            root,
            text="计时器：按空格键开始/停止计时，按R键重置",
            font=('黑体', 24, 'bold'),  # 稍微减小字号以容纳更多文字
            fg='black',
            bg='white'
        )
        self.instruction.pack(pady=15)
        
        # 创建时间显示标签
        self.time_label = tk.Label(
            root,
            text="0.00 s",
            font=('黑体', 100, 'bold'),
            fg='black',
            bg='white'
        )
        self.time_label.pack(expand=True)
        
        # 绑定键盘事件
        self.root.bind('<space>', self.toggle_timer)
        self.root.bind('<r>', self.reset_timer)  # 添加R键绑定
        self.root.bind('<R>', self.reset_timer)  # 处理大写R键
        
        # 计时器状态变量
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.last_update = 0

    def toggle_timer(self, event):
        if not self.running:
            # 开始计时
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_time()
        else:
            # 停止计时
            self.running = False

    def reset_timer(self, event):
        """重置计时器到初始状态"""
        self.running = False
        self.elapsed_time = 0
        self.time_label.config(text="0.00 s")
        # 更新提示文字颜色提供视觉反馈
        original_color = self.instruction.cget('fg')
        self.instruction.config(fg='red')
        self.root.after(200, lambda: self.instruction.config(fg=original_color))

    def update_time(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            
            # 每10毫秒更新一次显示
            if int(self.elapsed_time * 100) != self.last_update:
                # 使用兼容Python 3.0的字符串格式化
                display_time = "{:.2f} s".format(self.elapsed_time)
                self.time_label.config(text=display_time)
                self.last_update = int(self.elapsed_time * 100)
            
            # 使用after方法调度下一次更新
            self.root.after(10, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
