import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import time
from datetime import datetime, timedelta

class BiliSniperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("B站原神奖励自动狙击器 - GitHub 开源版")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.is_running = False  # 控制抢购循环的开关
        self.setup_ui()

    def setup_ui(self):
        # ================= 1. 凭证设置区 =================
        frame_auth = ttk.LabelFrame(self.root, text=" 核心凭证配置 (本地保存，绝对安全) ", padding=10)
        frame_auth.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_auth, text="SESSDATA:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_sess = ttk.Entry(frame_auth, width=60)
        self.entry_sess.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame_auth, text="bili_jct:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_jct = ttk.Entry(frame_auth, width=60)
        self.entry_jct.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(frame_auth, text="任务 ID:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_task = ttk.Entry(frame_auth, width=60)
        self.entry_task.insert(0, "18ERA2wloghvipp00") # 默认 11:00 任务
        self.entry_task.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # ================= 2. 战术设置区 =================
        frame_tactic = ttk.LabelFrame(self.root, text=" 狙击战术参数 ", padding=10)
        frame_tactic.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_tactic, text="提前开火量 (秒):").grid(row=0, column=0, sticky="w")
        self.entry_advance = ttk.Entry(frame_tactic, width=10)
        self.entry_advance.insert(0, "0.900")
        self.entry_advance.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(frame_tactic, text="连发次数:").grid(row=0, column=2, sticky="w", padx=10)
        self.entry_shots = ttk.Entry(frame_tactic, width=10)
        self.entry_shots.insert(0, "6")
        self.entry_shots.grid(row=0, column=3, sticky="w", padx=5)

        ttk.Label(frame_tactic, text="连发间隔 (秒):").grid(row=0, column=4, sticky="w", padx=10)
        self.entry_interval = ttk.Entry(frame_tactic, width=10)
        self.entry_interval.insert(0, "0.4")
        self.entry_interval.grid(row=0, column=5, sticky="w", padx=5)

        # ================= 3. 操作按钮区 =================
        frame_btns = tk.Frame(self.root)
        frame_btns.pack(fill="x", padx=10, pady=10)

        self.btn_test = ttk.Button(frame_btns, text="📡 测算服务器延迟", command=self.start_latency_test)
        self.btn_test.pack(side="left", padx=5)

        self.btn_start = ttk.Button(frame_btns, text="🚀 启动狙击系统", command=self.toggle_sniper)
        self.btn_start.pack(side="right", padx=5)

        # ================= 4. 日志输出区 =================
        frame_log = ttk.LabelFrame(self.root, text=" 战报终端 ", padding=10)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(frame_log, wrap=tk.WORD, state='disabled', bg="black", fg="green", font=("Consolas", 10))
        self.log_area.pack(fill="both", expand=True)

        self.log("系统初始化完成。本项目仅供开源技术交流。")
        self.log("请填入凭证后，点击测算延迟，或直接启动。")

    # ================= 核心功能函数 =================
    def log(self, message):
        """线程安全的日志输出"""
        def append():
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
            self.log_area.see(tk.END)
            self.log_area.config(state='disabled')
        self.root.after(0, append)

    def get_api_params(self):
        """读取并验证界面上的参数"""
        sess = self.entry_sess.get().strip()
        jct = self.entry_jct.get().strip()
        task = self.entry_task.get().strip()
        
        if not sess or not jct or not task:
            messagebox.showwarning("警告", "请完整填写 SESSDATA, bili_jct 和任务 ID！")
            return None
        return sess, jct, task

    # ---------------- 延迟测试模块 ----------------
    def start_latency_test(self):
        params = self.get_api_params()
        if not params: return
        self.btn_test.config(state="disabled")
        threading.Thread(target=self._run_latency_test, daemon=True).start()

    def _run_latency_test(self):
        self.log("开始向 B站接口发送探测包...")
        test_url = "https://api.bilibili.com/x/activity_components/mission/receive"
        latencies = []
        for i in range(3):
            start = time.time()
            try:
                requests.get(test_url, timeout=3)
            except:
                pass
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            self.log(f"探测包 {i+1}: 耗时 {latency:.0f} 毫秒")
            time.sleep(0.5)
            
        avg = sum(latencies) / len(latencies) / 1000
        self.log(f"✅ 平均延迟: {avg:.3f} 秒")
        
        # 自动帮用户计算最佳提前量 = 延迟 + 0.3秒缓冲
        suggest_time = avg + 0.3
        self.log(f"💡 已自动为您计算最佳提前量: {suggest_time:.3f} 秒，并填入上方表单。")
        
        # 将计算结果写回 UI 界面
        self.root.after(0, lambda: [self.entry_advance.delete(0, tk.END), self.entry_advance.insert(0, f"{suggest_time:.3f}")])
        self.root.after(0, lambda: self.btn_test.config(state="normal"))

    # ---------------- 定时狙击模块 ----------------
    def toggle_sniper(self):
        if not self.is_running:
            params = self.get_api_params()
            if not params: return
            self.is_running = True
            self.btn_start.config(text="🛑 紧急停止狙击")
            self.entry_sess.config(state="disabled")
            self.entry_jct.config(state="disabled")
            
            # 开启新线程运行 while 循环，防止 GUI 卡死
            threading.Thread(target=self._run_sniper_loop, args=(params,), daemon=True).start()
        else:
            self.is_running = False
            self.btn_start.config(text="🚀 启动狙击系统")
            self.entry_sess.config(state="normal")
            self.entry_jct.config(state="normal")
            self.log("已手动停止任务。")

    def _run_sniper_loop(self, params):
        sess, jct, task = params
        activity_id = "1ERAzwloghvcpc00"
        api_url = f"https://api.bilibili.com/x/activity_components/mission/receive?csrf={jct}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": f"https://www.bilibili.com/blackboard/era/award-exchange.html?task_id={task}",
            "Cookie": f"SESSDATA={sess}; bili_jct={jct};",
        }
        payload = {"csrf": jct, "task_id": task, "activity_id": activity_id, "receive_from": "missionPage"}
        
        try:
            adv_time = float(self.entry_advance.get())
            shots = int(self.entry_shots.get())
            interval = float(self.entry_interval.get())
        except ValueError:
            self.log("❌ 战术参数格式错误，必须是数字！已退出。")
            self.root.after(0, self.toggle_sniper)
            return

        # 智能判定：如果当前是 10点多，默认瞄准 11:00 (这里简化为取下一个整点或半点，你可以根据需要调整)
        now = datetime.now()
        target = now.replace(hour=11, minute=0, second=0, microsecond=0)
        if now >= target: target += timedelta(days=1)
        
        self.log(f"🎯 目标锁定！预计开火时间: {target}")
        self.log(f"战术确认: 提前 {adv_time} 秒, 连发 {shots} 次, 间隔 {interval} 秒")

        while self.is_running:
            now = datetime.now()
            diff = (target - now).total_seconds()
            
            if diff <= adv_time:
                self._fire(api_url, headers, payload, shots, interval)
                self.root.after(0, self.toggle_sniper) # 射击完毕后，自动恢复按钮状态
                break
                
            if diff > 60:
                time.sleep(1) # GUI 模式下每次最多睡1秒，以便及时响应“停止”按钮
                if int(diff) % 60 == 0:
                    self.log(f"💤 潜伏中，距离开火还有 {int(diff/60)} 分钟...")
            elif diff > 5:
                time.sleep(0.5)
                if int(diff*10) % 10 == 0:
                    self.log(f"⏱️ 倒计时: {int(diff)} 秒")
            else:
                time.sleep(0.01)

    def _fire(self, url, headers, payload, shots, interval):
        self.log("💥 目标进入射程，开始极限连发！！！")
        for i in range(shots):
            if not self.is_running: break # 允许中途强制停止
            try:
                self.log(f"  -> 第 {i+1} 发破甲弹射出...")
                resp = requests.post(url, headers=headers, data=payload, timeout=5)
                self.log(f"  [响应码:{resp.status_code}] 返回: {resp.json()}")
                time.sleep(interval)
            except Exception as e:
                self.log(f"  网络异常: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BiliSniperApp(root)
    root.mainloop()