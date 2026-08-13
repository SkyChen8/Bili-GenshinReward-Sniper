import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import time
import threading
from datetime import datetime, timedelta

class BiliSniperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B站原神奖励极速狙击台 V2.0 (多线程长连接版)")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        self.is_running = False
        self.setup_ui()

    def setup_ui(self):
        # ================= 1. 配置输入区 =================
        input_frame = ttk.LabelFrame(self.root, text=" 🔑 账号与任务配置 ", padding=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        # SESSDATA
        ttk.Label(input_frame, text="SESSDATA:").grid(row=0, column=0, sticky="w", pady=5)
        self.sess_entry = ttk.Entry(input_frame, width=50, show="*")
        self.sess_entry.grid(row=0, column=1, padx=10, pady=5)

        # bili_jct
        ttk.Label(input_frame, text="bili_jct (BID):").grid(row=1, column=0, sticky="w", pady=5)
        self.jct_entry = ttk.Entry(input_frame, width=50, show="*")
        self.jct_entry.grid(row=1, column=1, padx=10, pady=5)

        # Task ID
        ttk.Label(input_frame, text="项目代码 (Task ID):").grid(row=2, column=0, sticky="w", pady=5)
        self.tid_entry = ttk.Entry(input_frame, width=50)
        self.tid_entry.insert(0, "18ERA2wloghvipp00") # 默认填入 11:00 原石任务
        self.tid_entry.grid(row=2, column=1, padx=10, pady=5)

        # ================= 2. 控制按钮区 =================
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="🚀 启动自动狙击", bg="#ff6699", fg="white", font=("微软雅黑", 12, "bold"), command=self.start_sniper)
        self.start_btn.pack(side="left", fill="x", expand=True, ipady=5)

        # ================= 3. 运行日志区 =================
        log_frame = ttk.LabelFrame(self.root, text=" 📜 运行日志 ", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.log_area.pack(fill="both", expand=True)
        self.log_area.config(state='disabled')

        self.log("✅ 界面初始化完成，等待填入配置...")

    def log(self, message):
        """安全的日志打印函数，将文本输出到界面上"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END) # 自动滚动到底部
        self.log_area.config(state='disabled')

    def start_sniper(self):
        if self.is_running:
            return
            
        sess = self.sess_entry.get().strip()
        jct = self.jct_entry.get().strip()
        tid = self.tid_entry.get().strip()
        
        if not sess or not jct or not tid:
            messagebox.showwarning("警告", "请填满所有配置信息！")
            return

        self.is_running = True
        self.start_btn.config(state="disabled", text="⏳ 狙击潜伏中...", bg="#cccccc")
        self.log("\n" + "="*40)
        self.log("🚀 初始化狙击线程...")
        
        # 启动后台线程执行核心逻辑，防止 GUI 卡死
        threading.Thread(target=self.sniper_logic, args=(sess, jct, tid), daemon=True).start()

    def sniper_logic(self, sess, jct, tid):
        # 组装请求参数
        activity_id = "1ERAzwloghvcpc00"
        api_url = f"https://api.bilibili.com/x/activity_components/mission/receive?csrf={jct}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": f"https://www.bilibili.com/blackboard/era/award-exchange.html?task_id={tid}",
            "Cookie": f"SESSDATA={sess}; bili_jct={jct};",
            "Origin": "https://www.bilibili.com"
        }
        payload = {"csrf": jct, "task_id": tid, "activity_id": activity_id, "receive_from": "missionPage"}

        # 建立长连接
        session = requests.Session()
        session.headers.update(headers)

        # 计算目标时间 (11:00)
        now = datetime.now()
        target_time = now.replace(hour=11, minute=0, second=0, microsecond=0)
        if now >= target_time:
            target_time += timedelta(days=1)
            
        self.log(f"🎯 锁定目标时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        connection_warmed_up = False

        def fire_single_shot(shot_idx):
            try:
                resp = session.post(api_url, data=payload, timeout=3)
                self.log(f"  [{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] (子弹 {shot_idx}) 响应: {resp.json()}")
            except Exception as e:
                self.log(f"  (子弹 {shot_idx}) 异常: {e}")

        # 主控循环
        while True:
            current_time = datetime.now()
            time_diff = (target_time - current_time).total_seconds()

            # 提前 5 秒预热
            if 4.5 <= time_diff <= 5.5 and not connection_warmed_up:
                self.log(f"[{current_time.strftime('%H:%M:%S')}] 🔌 正在预热 TCP 长连接...")
                try:
                    session.get("https://api.bilibili.com/x/serverdate", timeout=3)
                    self.log("✅ 管道预热完成，子弹上膛！")
                except:
                    pass
                connection_warmed_up = True

            # 到达 00.000 秒，开火！
            if time_diff <= 0.000:
                self.log(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 🚀 跨过阀门，多线程全开！")
                for i in range(6):
                    self.log(f"  -> 第 {i+1} 发子弹飞出...")
                    threading.Thread(target=fire_single_shot, args=(i+1,), daemon=True).start()
                    time.sleep(0.15)
                
                time.sleep(3) # 给线程留出打日志的时间
                self.log("🏁 本次狙击任务结束。")
                break

            # 智能休眠反馈
            if time_diff > 60:
                if int(time_diff) % 10 == 0:
                    self.log(f"[{current_time.strftime('%H:%M:%S')}] 💤 距开火约 {int(time_diff/60)} 分钟...")
                time.sleep(1)
            elif time_diff > 5:
                self.log(f"[{current_time.strftime('%H:%M:%S')}] ⏱️ 倒计时: {int(time_diff)} 秒")
                time.sleep(1)
            else:
                time.sleep(0.001)

        # 恢复按钮状态
        self.start_btn.config(state="normal", text="🚀 启动自动狙击", bg="#ff6699")
        self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = BiliSniperGUI(root)
    root.mainloop()