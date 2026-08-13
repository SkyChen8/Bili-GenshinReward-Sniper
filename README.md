# Bili-GenshinReward-Sniper
"A lightweight, multi-threaded Python GUI tool for automated Bilibili Genshin Impact event reward claiming, featuring CSRF bypass and high-latency compensation."

[English](#english-version) | **[中文说明](#中文说明)**

---

## <a id="中文说明"></a>🇨🇳 中文说明

> **⚠️ 免责声明 (Disclaimer)**
> 本项目仅供个人学习、网络协议逆向与技术交流使用。请勿用于商业用途或恶意压测。开发者不对因使用本项目而导致的账号封禁、数据异常或其他任何损失承担任何责任。使用即代表您已知晓并同意此条款。

### 💡 项目起源
最近突然对 B站的创作者激励有点兴趣，连续手动试了好几天根本抢不到奖品。于是索性研究了一下底层 API 接口和抢购脚本的原理，顺手就摸了这个小工具出来。

### 📌 项目简介
这是一个基于 Python (`tkinter`) 开发的轻量级桌面端自动化工具，专为 B站 **原神 7.0 版本UP主激励计划** 及相关活动设计。针对跨国网络访问可能带来的高延迟痛点，本项目实现了**高延迟提前量补偿**与**多线程高频火力网覆盖**策略。

### ✨ 核心功能
*   **轻量 GUI 面板：** 提供简洁直观的图形操作界面，参数实时可配。
*   **智能延迟测算：** 内置服务器网络探测模块，一键测算延迟并自动套用最佳提前量公式。
*   **多线程并发：** 采用守护线程驱动倒计时与高频请求，确保主界面丝滑不卡死。
*   **安全防御绕过：** 完美适配 B站后端的 CSRF (`bili_jct`) 双重校验及表单传输规范。

### 🛠️ 快速开始
1. 克隆项目：`git clone https://github.com/SkyChen8/Bili-GenshinReward-Sniper.git`
2. 安装依赖：`pip install requests`
3. 运行程序：`python bili_gui_sniper.py`

### 📖 如何获取核心参数 (TODO)
> *（提示：此处未来可补充如何通过浏览器 F12 抓包获取 SESSDATA 和 bili_jct 的图文教程）*

---

## <a id="english-version"></a>🇬🇧 English Version

> **⚠️ Disclaimer**
> This project is for personal learning, network protocol reverse engineering, and technical communication purposes only. Do not use it for commercial purposes or malicious stress testing. The developer is not responsible for any account bans, data anomalies, or losses caused by using this project.

### 💡 Motivation
I suddenly got interested in Bilibili's creator incentive events recently. After failing to manually grab any rewards for several days, I decided to study the underlying APIs and script mechanisms, and casually built this tool to share.

### 📌 Overview
A lightweight desktop automation tool developed in Python (`tkinter`), specifically designed for Bilibili's **Genshin Impact Version 7.0 Creator Incentive Plan** and related events. It features high-latency compensation and multi-threaded rapid-fire strategies to counter network delay issues.

### ✨ Features
*   **Lightweight GUI:** Clean and intuitive graphical interface with real-time configurable parameters.
*   **Smart Latency Testing:** Built-in network probe to measure latency and automatically calculate the optimal advance time.
*   **Multi-threading:** Uses daemon threads for countdowns and requests, keeping the UI smooth.
*   **CSRF Bypass:** Fully compatible with Bilibili's backend validation and form submission standards.

### 🛠️ Quick Start
1. Clone the repo: `git clone https://github.com/SkyChen8/Bili-GenshinReward-Sniper.git`
2. Install dependencies: `pip install requests`
3. Run the app: `python bili_gui_sniper.py`

---

## 📄 License
本项目采用 [MIT License](LICENSE) 开源协议。