#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
灵体沟通工具 - Spirit Tool
Tkinter GUI 主程序
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
import json
import threading
from datetime import datetime

# PyInstaller 兼容路径
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_PATH)

from modules import tarot, wordcard, astro_dice, yijing, mazu, jiaobei, lenormand
from modules import api_client


class SpiritToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("灵体沟通工具")
        self.root.geometry("960x780")
        self.root.minsize(800, 600)

        # 数据路径
        self.data_dir = os.path.join(BASE_PATH, "data")
        self.output_dir = os.path.join(BASE_PATH, "output")
        os.makedirs(self.output_dir, exist_ok=True)

        # 数据
        self.wordcards = []
        self.mazu_signs = []
        self.session_log = []
        self.round_count = 0
        self.jiaobei_count = 0
        self.ai_busy = False

        # API 配置（保存在用户可写目录）
        if getattr(sys, 'frozen', False):
            # PyInstaller: 保存到 exe 所在目录的 data/ 下
            self.config_dir = os.path.join(os.path.dirname(sys.executable), "data")
        else:
            self.config_dir = self.data_dir
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_path = os.path.join(self.config_dir, "config.json")
        self.api_config = api_client.load_config(self.config_path)

        # 默认 system prompt
        self.default_system_prompt = ""
        sp_path = os.path.join(self.data_dir, "system_prompt.md")
        if os.path.exists(sp_path):
            try:
                with open(sp_path, 'r', encoding='utf-8') as f:
                    self.default_system_prompt = f.read()
            except Exception:
                pass

        # 加载默认数据
        self._load_defaults()

        # 构建 UI
        self._build_ui()

    # ── 数据加载 ──────────────────────────────────────────

    def _load_defaults(self):
        """加载默认数据"""
        # Hermes 字卡
        wc_path = os.path.join(self.data_dir, "wordcards_hermes.json")
        if os.path.exists(wc_path):
            try:
                self.wordcards = wordcard.load_cards(wc_path)
            except Exception:
                self.wordcards = []

        # 妈祖灵签
        mz_path = os.path.join(self.data_dir, "mazu_signs.json")
        if os.path.exists(mz_path):
            try:
                self.mazu_signs = mazu.load_signs(mz_path)
            except Exception:
                self.mazu_signs = []

    # ── UI 构建 ───────────────────────────────────────────

    def _build_ui(self):
        # 主框架使用 grid 布局
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # 运行记录区可伸缩

        self._build_top_bar()
        self._build_symbol_bar()
        self._build_log_area()
        self._build_tool_bar()
        self._build_input_area()

    def _build_top_bar(self):
        """顶部栏：沟通对象 + 问题 + API设置"""
        frame = ttk.Frame(self.root, padding="8 8 8 4")
        frame.grid(row=0, column=0, sticky="ew")
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(3, weight=1)

        ttk.Label(frame, text="沟通对象:").grid(row=0, column=0, padx=(0, 4))
        self.entity_var = tk.StringVar(value="Hermes")
        entity_entry = ttk.Entry(frame, textvariable=self.entity_var, width=15)
        entity_entry.grid(row=0, column=1, padx=(0, 16))

        ttk.Label(frame, text="问题:").grid(row=0, column=2, padx=(0, 4))
        self.question_var = tk.StringVar()
        q_entry = ttk.Entry(frame, textvariable=self.question_var)
        q_entry.grid(row=0, column=3, sticky="ew")

        ttk.Button(frame, text="API设置", command=self._open_api_settings).grid(
            row=0, column=4, padx=(12, 0)
        )

    def _build_symbol_bar(self):
        """符号系统选择 + 抽取按钮"""
        frame = ttk.LabelFrame(self.root, text="符号系统", padding="6")
        frame.grid(row=1, column=0, sticky="ew", padx=8, pady=2)

        self.use_tarot = tk.BooleanVar(value=True)
        self.use_wordcard = tk.BooleanVar(value=True)
        self.use_astro = tk.BooleanVar(value=True)
        self.use_yijing = tk.BooleanVar(value=False)
        self.use_mazu = tk.BooleanVar(value=False)
        self.use_lenormand = tk.BooleanVar(value=False)

        checks = [
            ("塔罗牌", self.use_tarot),
            ("字卡", self.use_wordcard),
            ("占星骰子", self.use_astro),
            ("易经", self.use_yijing),
            ("妈祖灵签", self.use_mazu),
            ("雷诺曼", self.use_lenormand),
        ]
        for i, (text, var) in enumerate(checks):
            ttk.Checkbutton(frame, text=text, variable=var).grid(row=0, column=i, padx=6)

        ttk.Button(frame, text="导入字卡", command=self._import_wordcards).grid(row=0, column=len(checks), padx=(16, 4))
        ttk.Button(frame, text="开始抽取", command=self._do_full_draw).grid(row=0, column=len(checks) + 1, padx=4)

    def _build_log_area(self):
        """运行记录区"""
        frame = ttk.LabelFrame(self.root, text="运行记录（可选择复制）", padding="6")
        frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=2)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, font=("Consolas", 10), spacing3=2
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

    def _build_tool_bar(self):
        """工具栏：单独抽取按钮 + 导出"""
        frame = ttk.Frame(self.root, padding="4 2")
        frame.grid(row=3, column=0, sticky="ew", padx=8)

        # 占卜工具按钮
        tools = [
            ("筊杯", self._do_jiaobei),
            ("塔罗", lambda: self._do_single("tarot")),
            ("字卡", lambda: self._do_single("wordcard")),
            ("骰子", lambda: self._do_single("astro")),
            ("易经", lambda: self._do_single("yijing")),
            ("妈祖", lambda: self._do_single("mazu")),
            ("雷诺曼", lambda: self._do_single("lenormand")),
        ]
        for i, (text, cmd) in enumerate(tools):
            ttk.Button(frame, text=text, command=cmd, width=6).grid(row=0, column=i, padx=2)

        # 分隔
        ttk.Separator(frame, orient=tk.VERTICAL).grid(row=0, column=len(tools), padx=6, sticky="ns")

        # AI 解读按钮
        col = len(tools) + 1
        self.ai_btn = ttk.Button(frame, text="AI解读", command=self._do_ai_interp, width=7)
        self.ai_btn.grid(row=0, column=col, padx=2)

        # 分隔
        ttk.Separator(frame, orient=tk.VERTICAL).grid(row=0, column=col + 1, padx=6, sticky="ns")

        # 导出按钮
        ecol = col + 2
        ttk.Button(frame, text="复制全部", command=self._copy_all).grid(row=0, column=ecol, padx=2)
        ttk.Button(frame, text="导出MD", command=self._export_md).grid(row=0, column=ecol + 1, padx=2)
        ttk.Button(frame, text="导出TXT", command=self._export_txt).grid(row=0, column=ecol + 2, padx=2)

    def _build_input_area(self):
        """输入区：解读/海龟汤"""
        frame = ttk.LabelFrame(self.root, text="输入区", padding="6")
        frame.grid(row=4, column=0, sticky="ew", padx=8, pady=(2, 8))
        frame.columnconfigure(0, weight=1)

        self.input_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        self.input_text.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 4))

        ttk.Button(frame, text="提交解读", command=self._submit_interp).grid(row=1, column=0, padx=4, sticky="w")
        ttk.Button(frame, text="提交问题→筊杯", command=self._submit_turtle).grid(row=1, column=1, padx=4, sticky="w")
        ttk.Button(frame, text="结束本轮", command=self._end_round).grid(row=1, column=2, padx=4, sticky="w")
        ttk.Button(frame, text="清空记录", command=self._clear_log).grid(row=1, column=4, padx=4, sticky="e")

    # ── 日志 ──────────────────────────────────────────────

    def _log(self, text):
        """追加文字到运行记录区"""
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.session_log.append(text)

    # ── 主抽取 ────────────────────────────────────────────

    def _do_full_draw(self):
        """按选中的符号系统执行一次完整抽取"""
        entity = self.entity_var.get().strip() or "Hermes"
        question = self.question_var.get().strip()

        self.round_count += 1
        self.jiaobei_count = 0

        self._log(f"\n{'=' * 50}")
        self._log(f"第{self.round_count}轮")
        self._log(f"沟通对象: {entity}")
        if question:
            self._log(f"问题: {question}")
        self._log(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log(f"{'=' * 50}\n")

        if self.use_tarot.get():
            result = tarot.draw(3)
            self._log(tarot.format_result(result))
            self._log("")

        if self.use_wordcard.get():
            if self.wordcards:
                result = wordcard.draw(self.wordcards, 3)
                self._log(wordcard.format_result(result, entity))
            else:
                self._log("=== WORD CARDS ===\n[未加载字卡库，请先导入]")
            self._log("")

        if self.use_astro.get():
            result = astro_dice.draw()
            self._log(astro_dice.format_result(result))
            self._log("")

        if self.use_yijing.get():
            result = yijing.draw()
            self._log(yijing.format_result(result))
            self._log("")

        if self.use_mazu.get():
            if self.mazu_signs:
                result = mazu.draw(self.mazu_signs)
                self._log(mazu.format_result(result))
            else:
                self._log("=== 妈祖灵签 ===\n[签文数据未加载]")
            self._log("")

        if self.use_lenormand.get():
            result = lenormand.draw(3)
            self._log(lenormand.format_result(result))
            self._log("")

    # ── 单独工具 ──────────────────────────────────────────

    def _do_single(self, tool_name):
        """执行单个占卜工具"""
        entity = self.entity_var.get().strip() or "Hermes"

        if tool_name == "tarot":
            result = tarot.draw(3)
            self._log(tarot.format_result(result))
        elif tool_name == "wordcard":
            if self.wordcards:
                result = wordcard.draw(self.wordcards, 3)
                self._log(wordcard.format_result(result, entity))
            else:
                self._log("[未加载字卡库]")
        elif tool_name == "astro":
            result = astro_dice.draw()
            self._log(astro_dice.format_result(result))
        elif tool_name == "yijing":
            result = yijing.draw()
            self._log(yijing.format_result(result))
        elif tool_name == "mazu":
            if self.mazu_signs:
                result = mazu.draw(self.mazu_signs)
                self._log(mazu.format_result(result))
            else:
                self._log("[签文数据未加载]")
        elif tool_name == "lenormand":
            result = lenormand.draw(3)
            self._log(lenormand.format_result(result))

        self._log("")

    def _do_jiaobei(self):
        """筊杯"""
        self.jiaobei_count += 1
        result = jiaobei.draw()
        self._log(f"=== 筊杯 (第{self.jiaobei_count}次) ===")
        self._log(f"{result['cup1']}/{result['cup2']} -- {result['result_cn']}")
        self._log("")

    # ── 输入提交 ──────────────────────────────────────────

    def _submit_interp(self):
        """提交解读"""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            return
        self._log("--- 解读 ---")
        self._log(text)
        self._log("")
        self.input_text.delete("1.0", tk.END)

    def _submit_turtle(self):
        """提交海龟汤问题 + 自动筊杯"""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            return

        self.jiaobei_count += 1
        result = jiaobei.draw()

        self._log(f"Q: {text}")
        self._log(f"→ {result['cup1']}/{result['cup2']} -- {result['result_cn']}")
        self._log("")
        self.input_text.delete("1.0", tk.END)

    def _end_round(self):
        """结束本轮"""
        self._log(f"\n{'─' * 50}")
        self._log(f"第{self.round_count}轮结束")
        self._log(f"{'─' * 50}\n")

    # ── 字卡导入 ──────────────────────────────────────────

    def _import_wordcards(self):
        """导入自定义字卡"""
        path = filedialog.askopenfilename(
            title="选择字卡文件",
            filetypes=[
                ("支持的格式", "*.json *.txt *.md"),
                ("JSON", "*.json"),
                ("文本", "*.txt"),
                ("Markdown", "*.md"),
                ("所有文件", "*.*"),
            ]
        )
        if not path:
            return
        try:
            self.wordcards = wordcard.load_cards(path)
            self._log(f"[系统] 已导入字卡: {len(self.wordcards)} 张 ({os.path.basename(path)})")
            self._log("")
        except Exception as e:
            messagebox.showerror("导入失败", str(e))

    # ── 导出 ──────────────────────────────────────────────

    def _get_full_log(self):
        """获取运行记录全文"""
        return self.log_text.get("1.0", tk.END).strip()

    def _copy_all(self):
        """复制全部到剪贴板"""
        text = self._get_full_log()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._log("[系统] 已复制到剪贴板")

    def _export_md(self):
        """导出为 MD 文件"""
        self._export_file("md")

    def _export_txt(self):
        """导出为 TXT 文件"""
        self._export_file("txt")

    def _export_file(self, ext):
        """导出文件"""
        text = self._get_full_log()
        if not text:
            messagebox.showinfo("提示", "运行记录为空")
            return

        entity = self.entity_var.get().strip() or "Hermes"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"沟通记录_{entity}_{ts}.{ext}"

        path = filedialog.asksaveasfilename(
            initialdir=self.output_dir,
            initialfile=default_name,
            defaultextension=f".{ext}",
            filetypes=[(f"{ext.upper()} 文件", f"*.{ext}"), ("所有文件", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, 'w', encoding='utf-8') as f:
                if ext == "md":
                    f.write(f"# 灵体沟通记录\n\n")
                    f.write(f"**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
                    f.write(f"**沟通对象**: {entity}  \n\n")
                    f.write("---\n\n")
                    f.write("```\n")
                    f.write(text)
                    f.write("\n```\n")
                else:
                    f.write(text)
            self._log(f"[系统] 已导出: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    # ── 清空 ──────────────────────────────────────────────

    def _clear_log(self):
        """清空运行记录"""
        if self.session_log:
            if not messagebox.askyesno("确认", "确定清空所有运行记录？"):
                return
        self.log_text.delete("1.0", tk.END)
        self.session_log.clear()
        self.round_count = 0
        self.jiaobei_count = 0

    # ── API 设置 ─────────────────────────────────────────

    def _open_api_settings(self):
        """打开 API 设置窗口"""
        win = tk.Toplevel(self.root)
        win.title("API 设置")
        win.geometry("560x520")
        win.resizable(True, True)
        win.transient(self.root)
        win.grab_set()

        pad = {"padx": 8, "pady": 4}

        # API URL
        ttk.Label(win, text="API URL:").grid(row=0, column=0, sticky="w", **pad)
        url_var = tk.StringVar(value=self.api_config.get("api_url", ""))
        url_entry = ttk.Entry(win, textvariable=url_var, width=60)
        url_entry.grid(row=0, column=1, sticky="ew", **pad)
        ttk.Label(win, text="填基础地址即可，如 https://api.example.com",
                  foreground="gray").grid(row=0, column=2, sticky="w", padx=(0, 8))

        # API Token
        ttk.Label(win, text="API Token:").grid(row=1, column=0, sticky="w", **pad)
        token_var = tk.StringVar(value=self.api_config.get("api_token", ""))
        ttk.Entry(win, textvariable=token_var, width=60, show="*").grid(row=1, column=1, sticky="ew", **pad)

        # Model
        ttk.Label(win, text="Model:").grid(row=2, column=0, sticky="w", **pad)
        model_var = tk.StringVar(value=self.api_config.get("model", ""))
        ttk.Entry(win, textvariable=model_var, width=60).grid(row=2, column=1, sticky="ew", **pad)

        # System Prompt
        ttk.Label(win, text="System Prompt:").grid(row=3, column=0, sticky="nw", **pad)
        sp_text = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 9), height=16)
        sp_text.grid(row=3, column=1, sticky="nsew", **pad)

        # 填入已保存或默认的 system prompt
        saved_sp = self.api_config.get("system_prompt", "")
        sp_text.insert("1.0", saved_sp if saved_sp else self.default_system_prompt)

        win.columnconfigure(1, weight=1)
        win.rowconfigure(3, weight=1)

        # 按钮栏
        btn_frame = ttk.Frame(win, padding="4")
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        def _save():
            self.api_config["api_url"] = url_var.get().strip()
            self.api_config["api_token"] = token_var.get().strip()
            self.api_config["model"] = model_var.get().strip()
            prompt_content = sp_text.get("1.0", tk.END).strip()
            self.api_config["system_prompt"] = prompt_content
            try:
                api_client.save_config(self.config_path, self.api_config)
                self._log("[系统] API 配置已保存")
            except Exception as e:
                messagebox.showerror("保存失败", str(e), parent=win)
                return
            win.destroy()

        def _test():
            url = url_var.get().strip()
            token = token_var.get().strip()
            model = model_var.get().strip()
            if not url or not token or not model:
                messagebox.showwarning("提示", "请先填写 URL、Token 和 Model", parent=win)
                return
            try:
                reply = api_client.call_chat(
                    url, token, model,
                    [{"role": "user", "content": "Hi, reply with exactly: OK"}],
                    stream=False, timeout=15,
                )
                messagebox.showinfo("连接成功", f"AI 回复: {reply[:100]}", parent=win)
            except api_client.APIError as e:
                messagebox.showerror("连接失败", str(e), parent=win)

        ttk.Button(btn_frame, text="测试连接", command=_test).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text="保存", command=_save).pack(side=tk.RIGHT, padx=8)
        ttk.Button(btn_frame, text="取消", command=win.destroy).pack(side=tk.RIGHT, padx=4)

    # ── AI 解读 ──────────────────────────────────────────

    def _collect_draw_context(self):
        """从日志中收集当前轮次的抽取结果文本"""
        log_text = self._get_full_log()
        if not log_text:
            return ""
        # 找最后一个轮次分隔线之后的内容
        lines = log_text.split("\n")
        last_round_start = 0
        for i, line in enumerate(lines):
            if line.startswith("=" * 20):
                last_round_start = i
        return "\n".join(lines[last_round_start:])

    def _do_ai_interp(self):
        """调用 AI 进行解读（后台线程）"""
        # 检查配置
        url = self.api_config.get("api_url", "")
        token = self.api_config.get("api_token", "")
        model = self.api_config.get("model", "")
        if not url or not token or not model:
            messagebox.showwarning("提示", "请先配置 API（点击顶部 [API设置]）")
            return

        # 检查是否有抽取结果
        context = self._collect_draw_context()
        if not context.strip():
            messagebox.showwarning("提示", "请先执行抽取，再调用 AI 解读")
            return

        if self.ai_busy:
            return

        self.ai_busy = True
        self.ai_btn.configure(text="思考中...", state="disabled")

        entity = self.entity_var.get().strip() or "Hermes"
        question = self.question_var.get().strip()

        # 构造 user message
        user_parts = [f"沟通对象: {entity}"]
        if question:
            user_parts.append(f"问题: {question}")
        user_parts.append(f"\n以下是本轮符号抽取结果:\n{context}")
        user_parts.append("\n请简要分析符号要点、列出可能的解读方向、并提醒我可能的确认偏误。不要给出完整解读，不要模拟灵体说话。")
        user_msg = "\n".join(user_parts)

        # system prompt
        sp = self.api_config.get("system_prompt", "") or self.default_system_prompt

        messages = [
            {"role": "system", "content": sp},
            {"role": "user", "content": user_msg},
        ]

        self._log("--- AI 解读建议 ---")

        def _worker():
            try:
                gen = api_client.call_chat(url, token, model, messages, stream=True, timeout=120)
                for chunk in gen:
                    self.root.after(0, self._append_stream, chunk)
                self.root.after(0, self._ai_done, None)
            except api_client.APIError as e:
                self.root.after(0, self._ai_done, str(e))
            except Exception as e:
                self.root.after(0, self._ai_done, str(e))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def _append_stream(self, text):
        """从流式 API 追加文本到日志区（主线程调用）"""
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        # 同步到 session_log（追加到最后一条或新建）
        if self.session_log and not self.session_log[-1].endswith("\n"):
            self.session_log[-1] += text
        else:
            self.session_log.append(text)

    def _ai_done(self, error):
        """AI 调用结束回调（主线程调用）"""
        self.ai_busy = False
        self.ai_btn.configure(text="AI解读", state="normal")
        if error:
            self._log(f"\n[AI 错误] {error}")
        self._log("\n--- AI 解读结束 ---\n")


def main():
    root = tk.Tk()
    app = SpiritToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
