# Project Hermes / Spirit Tool

桌面端符号工作台。它把塔罗牌、字卡、占星骰子、易经、妈祖灵签、雷诺曼和筊杯放进同一个 GUI，支持本地抽取、记录、导出和可选 AI 解读建议。

Project Hermes 适合想直接打开使用的人：无需搭 Agent 环境，也可以完成日常抽取与归档。

## 适合谁

- 想要一个可视化桌面工具，直接抽取并保存记录。
- 想把多套符号系统放在同一轮问题里使用。
- 想保留本地优先的使用方式，AI 建议只在需要时开启。
- 想把桌面抽取结果交给 Agent Skill 做后续处理。

## 功能

### 符号系统

| 符号系统 | 内容 |
|---|---|
| 塔罗牌 | 22 张大阿卡纳 + 56 张小阿卡纳，含正逆位 |
| 字卡 | 支持导入 JSON / TXT / MD 字卡库，随机抽取 3 张 |
| 占星骰子 | 行星 × 星座 × 宫位，含尊贵状态、上升星座、飞星 |
| 易经 | 64 卦，含本卦、变爻、之卦 |
| 妈祖灵签 | 60 签，四句古诗 |
| 雷诺曼 | 36 张雷诺曼牌 |
| 筊杯 | 圣杯、笑杯、阴杯 |

### 工作流功能

- 海龟汤模式：输入 Yes / No 问题后掷筊杯。
- 自由解读：在文本区记录自己的解读。
- 导出：复制、导出 Markdown、导出 TXT。
- AI 解读建议：配置 OpenAI 兼容 API 后，可获取方向提示和偏误提醒。

## AI 位置

AI 解读建议是可选增强。核心抽取、记录和导出都可以离线完成。

建议把 AI 放在三个位置：

1. 整理符号材料。
2. 提醒可能的确认偏误。
3. 给出可供参考的解读方向。

最终解读、是否继续追问、是否接受筊杯结果，由使用者自己判断。

## 使用方式

### 直接运行

从 [Releases](../../releases) 下载 `SpiritTool_v2.exe`，双击运行。

### 从源码运行

```bash
cd spirit_tool_hermes
python main.py
```

依赖：

- Python 3.10+
- 标准库：`tkinter`、`json`、`urllib` 等

桌面版核心功能无需安装第三方包。

### AI 解读配置

1. 点击顶部 `[API设置]`。
2. 填入 API URL，例如 `https://api.example.com`。
3. 填入 API Token 和 Model 名称。
4. 点击 `[测试连接]`。
5. 保存后，抽取完成时点击 `[AI解读]`。

OpenAI 兼容 API、代理和中转服务均可尝试。

## 项目结构

```text
spirit_tool_hermes/
├── README.md
├── main.py
├── main_kivy.py
├── modules/
│   ├── tarot.py
│   ├── wordcard.py
│   ├── astro_dice.py
│   ├── yijing.py
│   ├── mazu.py
│   ├── jiaobei.py
│   ├── lenormand.py
│   └── api_client.py
├── data/
│   ├── wordcards_hermes.json
│   ├── mazu_signs.json
│   └── system_prompt.md
└── SpiritTool.spec
```

## 与其他工具的关系

| 工具 | 作用 |
|---|---|
| Project Hermes | 桌面工作台，适合直接使用和导出记录 |
| spirit-communication-system v5.0 | Agent 全流程版，适合沉浸式自动沟通流程 |
| spirit-communication-system v5.1 Lite | 原始符号抽取版，适合交给使用者或其他 Skill 后处理 |
| Symbol Anchor Check | 塔罗属性校验器，检查 Book T 属性支持度 |
| 梅花易数 Skill | 易经 / 梅花断卦流程器 |

Project Hermes 的定位是入口工具。它可以单独使用，也可以把结果交给 Agent Skill。

## 打包

```bash
cd spirit_tool_hermes
pyinstaller SpiritTool.spec --noconfirm
```

输出文件：

```text
dist/SpiritTool_v2.exe
```

## 来源与边界

本项目包含四类内容：

1. 传统与公开来源：塔罗、易经、妈祖灵签、雷诺曼、占星骰子、筊杯等符号系统。
2. 作者整理：GUI 流程、字卡库、输出格式、默认 system prompt、导出结构。
3. 程序生成：随机抽取结果、日志、导出文件。
4. AI 参与：可选解读建议、偏误提醒和文本整理。

本项目用于个人占卜、符号分析、创作、记录和实验性工作流。它不提供现实决策担保，不替代医疗、法律、财务或心理咨询建议。

## License

MIT
