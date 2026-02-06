# Spirit Tool — 灵体沟通工具

一个基于符号学随机抽取的沟通辅助工具。通过塔罗牌、字卡、占星骰子等多套符号系统生成随机结果，配合筊杯验证机制，辅助用户完成符号解读。

v2 新增 AI 解读建议功能——符号抽取后可调用 OpenAI 兼容 API，获取解读方向参考。

---

## 功能

### 符号系统（6 套）

| 符号系统 | 说明 |
|---------|------|
| **塔罗牌** | 22 大阿卡纳 + 56 小阿卡纳，含正逆位 |
| **字卡** | 可导入自定义字卡库（JSON/TXT/MD），随机抽 3 张 |
| **占星骰子** | 行星 × 星座 × 宫位，含尊贵状态、上升星座、飞星 |
| **易经** | 64 卦，含本卦、变爻、之卦 |
| **妈祖灵签** | 60 签，四句古诗 |
| **雷诺曼** | 36 张雷诺曼牌 |

### 验证与流程

- **筊杯**：圣杯（确认）/ 笑杯（有保留）/ 阴杯（偏差）
- **海龟汤模式**：输入 Yes/No 问题，自动掷筊杯
- **自由解读**：文本输入区提交解读，记录到日志
- **导出**：一键复制 / 导出 MD / 导出 TXT

### AI 解读建议（v2）

- 支持 OpenAI 兼容格式的 API（包括各类代理/中转服务）
- 流式输出，逐 token 显示
- AI 仅提供解读方向建议和确认偏误提醒，不替代用户判断
- 内置默认 system prompt，可在设置中自定义覆盖

---

## 使用

### 直接运行

从 [Releases](../../releases) 下载 `SpiritTool_v2.exe`，双击运行，无需安装。

### 从源码运行

```bash
cd spirit_tool_hermes
python main.py
```

依赖：Python 3.10+，仅使用标准库（tkinter、json、urllib 等），**无需 pip install 任何第三方包**。

### AI 解读配置

1. 点击顶部 `[API设置]`
2. 填入 API URL（基础地址即可，如 `https://api.example.com`，程序自动补全路径）
3. 填入 API Token 和 Model 名称
4. 点击 `[测试连接]` 确认可用
5. 保存后，抽取完成后点击工具栏 `[AI解读]` 即可

不配置 API 也可以正常使用全部抽取和验证功能。

---

## 工作流程

```
输入沟通对象和问题
        ↓
选择符号系统 → 开始抽取
        ↓
   [AI解读]（可选）— 获取方向建议
        ↓
用户自行解读 → 提交解读
        ↓
筊杯验证 → 海龟汤细化 → 结束本轮
        ↓
复制 / 导出记录
```

---

## 项目结构

```
spirit_tool_hermes/
├── main.py                 # GUI 主程序
├── modules/
│   ├── tarot.py            # 塔罗牌
│   ├── wordcard.py         # 字卡（支持导入）
│   ├── astro_dice.py       # 占星骰子
│   ├── yijing.py           # 易经
│   ├── mazu.py             # 妈祖灵签
│   ├── jiaobei.py          # 筊杯
│   ├── lenormand.py        # 雷诺曼
│   └── api_client.py       # API 调用模块（v2）
├── data/
│   ├── wordcards_hermes.json   # 默认字卡库
│   ├── mazu_signs.json         # 妈祖签文
│   └── system_prompt.md        # AI 默认 system prompt
└── SpiritTool.spec         # PyInstaller 打包配置
```

---

## 打包

```bash
cd spirit_tool_hermes
pyinstaller SpiritTool.spec --noconfirm
```

输出：`dist/SpiritTool_v2.exe`（单文件，约 15MB）

---

## 设计原则

- **信任随机性**：所有符号结果由程序随机生成，不做预设筛选
- **人在回路**：AI 仅提供建议方向，最终解读由用户完成
- **筊杯验证**：解读完成后通过随机筊杯进行确认/否定，形成反馈闭环
- **零依赖**：纯 Python 标准库实现，不需要安装任何第三方包
- **本地优先**：核心功能完全离线可用，AI 为可选增强

---

## License

MIT
