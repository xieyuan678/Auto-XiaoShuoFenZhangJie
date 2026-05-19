# Auto-XiaoShuoFenZhangJie

Auto-XiaoShuoFenZhangJie（自动小说分章节工具）是一个自动化处理工具，旨在将整本小说文本按照章节进行智能分割，生成结构化的分章节文件，便于后续编辑、排版、导出或在不同平台发布。

## 项目特性

- **智能章节识别**：自动识别并分割小说中的章节标题，支持常见的中文、数字和自定义章节格式（如“第一章”、“Chapter 1”等）。
- **批量处理**：支持批量导入、处理多本小说文件，提升工作效率。
- **多格式支持**：输入支持 TXT、EPUB 等常见文本格式，输出支持多章节 TXT 或结构化目录。
- **高可定制性**：章节分割规则可配置，适配不同来源的小说文本。
- **易于集成**：可作为命令行工具或 Python 包集成到其他项目中。

## 使用说明

### 安装

克隆本仓库到本地并进入目录：
```bash
git clone https://github.com/xieyuan678/Auto-XiaoShuoFenZhangJie.git
cd Auto-XiaoShuoFenZhangJie
```

（如有 requirements.txt 可补充如下）
```bash
pip install -r requirements.txt
```

### 快速开始

以命令行工具方式运行，假设`main.py`为入口文件：

```bash
python main.py --input 输入小说.txt --output 输出目录
```

支持的参数示例：

- `--input/-i`   ：待处理的小说原文文件
- `--output/-o`  ：输出的分章节目录
- `--pattern/-p` ：自定义章节分割正则（可选）

### 示例

```bash
python main.py -i 三国演义全集.txt -o output_dir -p "^第[一二三四五六七八九十百千0-9]+章"
```

### 输出结果
- 处理完成后，每个章节会保存为单独的文本文件，文件名为章节标题或序号。
- 还可输出章节目录索引文件（如 toc.json 或 toc.md），便于进一步加工。

## 适用场景

- 小说编辑与排版准备
- 网络文学平台章节管理
- 文本挖掘与自然语言处理预处理
- 电子书格式转换辅助

## 目录结构示例

```
Auto-XiaoShuoFenZhangJie/
├── main.py
├── utils.py
├── requirements.txt
├── README.md
└── example/
    └── 三国演义全集.txt
```

## 贡献与联系

欢迎 Issue、PR 以及任何建议和反馈！

- 作者：xieyuan678
- 项目主页：https://github.com/xieyuan678/Auto-XiaoShuoFenZhangJie

## 开源许可证

本项目采用 MIT License 许可。
