import os
import re
import traceback
import sys
import argparse

# 显示程序标题
print("="*50)
print("--------------（小说TXT文件分割工具）-------------")
print("\n软件用于将小说TXT文件自动分割成多个章节文件                    \n--------------问题反馈，联系作者：xy8011")
print("="*50)


def remove_chapter_headings(content):
    """
    删除文本中所有类似"第一章 标题"的内容
    :param content: 原始文本内容
    :return: 删除章节标题后的文本
    """
    # 匹配类似"第一章 标题"的模式
    # 支持中文数字和阿拉伯数字
    pattern = re.compile(r'第[一二三四五六七八九十百千0-9]+章\s+.+', re.UNICODE)
    # 替换匹配的内容为空字符串
    cleaned_content = pattern.sub('', content)
    return cleaned_content


def clean_empty_lines(content):
    """
    清理文本中的所有空行（包括仅含空格/制表符的行）
    :param content: 原始文本内容
    :return: 清理空行后的文本
    """
    # 按行分割，过滤空行
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # 去除行首尾的空格/制表符/换行符
        stripped_line = line.strip()
        # 仅保留非空行
        if stripped_line:
            cleaned_lines.append(line)  # 保留原行格式（仅删除空行，不修改有效行的缩进）

    # 重新拼接文本
    return '\n'.join(cleaned_lines)


def split_novel_files():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='小说自动分章工具')
    parser.add_argument('--start', type=int, default=None, help='起始章节数（默认为1）')
    args = parser.parse_args()
    
    # 核心修改：获取脚本运行时的当前工作目录（由bat文件指定）
    target_folder = os.getcwd()
    print(f"当前处理目录：{target_folder}")
    
    # 设置起始章节数（支持命令行参数和交互式输入两种模式）
    if args.start is not None:
        # 使用命令行参数
        start_chapter = args.start
    else:
        # 交互式输入
        while True:
            try:
                user_input = input("请输入起始章节数（默认为1）：").strip()
                if not user_input:
                    start_chapter = 1
                else:
                    start_chapter = int(user_input)
                if start_chapter < 1:
                    print("起始章节数不能小于1，请重新输入")
                else:
                    break
            except ValueError:
                print("请输入有效的数字")
    
    print(f"起始章节数：{start_chapter}")

    # 标点符号正则（优化：移除重复字符，简化正则）
    punctuation_pattern = re.compile(r'[。，；：！？""''()\[\]【】]')
    # 全量清洗标点的正则（移除所有符号，只留纯文字）
    clean_symbol_pattern = re.compile(r'[。，；：！？""''()\[\]【】、·~@#￥%……&*（）—+-={}|《》？“”‘’｛｝【】￥¥∧∨～﹉﹊﹍﹎﹋﹌﹟﹠﹡﹢﹦﹤‐￣¯―]')
    '''
    # 显示程序标题
    print("="*50)
    print("--------------（小说TXT文件分割工具）-------------")
    print("\n软件用于将小说TXT文件自动分割成多个章节文件                    \n--------------问题反馈，联系作者：xy8011")
    # print("="*50)
     '''
    # 交互式选择每章节最小字数
    print("="*50)
    print("请选择每章节最小字数：")
    print("  A. 1200字（默认，直接按回车）")
    print("  B. 2400字")
    print("  C. 自定义字数")
    print("="*50)

    while True:
        choice = input("请输入选择（A/B/C）：").strip().upper()
        if not choice:  # 默认选项
            min_chars = 1200
            break
        elif choice == 'A':
            min_chars = 1200
            break
        elif choice == 'B':
            min_chars = 2400
            break
        elif choice == 'C':
            try:
                custom_chars = int(input("请输入自定义字数：").strip())
                if custom_chars > 0:
                    min_chars = custom_chars
                    break
                else:
                    print("请输入大于0的数字")
            except ValueError:
                print("请输入有效的数字")
        else:
            print("无效选项，请输入A、B或C")
    
    print(f"已选择每章节最少{min_chars}字")
    min_desc_len = 5  # 标题最少3字（大于2字）
    max_desc_len = 14  # 标题最多14字（小于15字）

    # Windows非法文件名字符
    illegal_chars = r'[\\/:*?"<>|]+'
    # 不可见字符
    invisible_chars = re.compile(r'[\x00-\x1f\x7f-\x9f]')

    if not os.path.exists(target_folder):
        print("错误：文件夹不存在")
        return

    # 统计处理结果
    total_files = 0
    success_files = 0
    fail_files = []

    for root, dirs, files in os.walk(target_folder):
        for file_name in files:
            if not file_name.lower().endswith('.txt'):
                continue
            # 跳过已经生成的章节文件
            if re.search(r'第\d+章', file_name):
                continue
            total_files += 1
            file_path = os.path.join(root, file_name)
            print(f"\n正在处理：{file_path}")

            try:
                # 增强编码处理：尝试多种常见编码
                encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
                content = None
                used_encoding = None
                for enc in encodings:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            content = f.read()
                        used_encoding = enc
                        break
                    except:
                        continue
                if content is None:
                    print(f"  错误：无法识别{file_name}的编码，跳过")
                    fail_files.append(file_name)
                    continue

                # 删除章节标题
                content = remove_chapter_headings(content)

                # 清理空行
                content = clean_empty_lines(content)

                total_chars = len(content)
                if total_chars == 0:
                    print(f"  警告：{file_name} 内容为空，跳过")
                    fail_files.append(file_name)
                    continue

                chapters = []  # 暂存章节列表 (章节名, 章节内容)
                chapter_num = start_chapter
                start_pos = 0

                # 第一步：按规则分割所有候选章节
                while start_pos < total_chars:
                    remaining = total_chars - start_pos

                    # 分割逻辑：1200字以上 + 取到句号为止
                    if remaining <= min_chars:
                        # 先暂存为候选最后一章
                        chapter_content = content[start_pos:]
                        end_pos = total_chars
                    else:
                        min_pos = start_pos + min_chars
                        period_pos = content.find('。', min_pos)
                        if period_pos != -1:
                            end_pos = period_pos + 1
                        else:
                            end_pos = total_chars
                        chapter_content = content[start_pos:end_pos]

                    # 提取标题描述（3-14字规则）
                    chapter_desc = ""
                    # 1. ！前面的内容
                    ex_pos = chapter_content.find('！')
                    if ex_pos != -1:
                        bef = chapter_content[:ex_pos]
                        matches = list(punctuation_pattern.finditer(bef))
                        if matches:
                            p = matches[-1].end()
                            t = bef[p:].strip()
                        else:
                            t = bef.strip()
                        if min_desc_len <= len(t) <= max_desc_len:
                            chapter_desc = t

                    # 2. ！不行 → “”中间的内容
                    if not chapter_desc:
                        quote_m = re.search(r'“([^”]+)”', chapter_content)
                        if quote_m:
                            t = quote_m.group(1).strip()
                            if min_desc_len <= len(t) <= max_desc_len:
                                chapter_desc = t

                    # 3. ""不行 → ？前面的内容
                    if not chapter_desc:
                        q_pos = chapter_content.find('？')
                        if q_pos == -1:
                            q_pos = chapter_content.find('?')
                        if q_pos != -1:
                            bef = chapter_content[:q_pos]
                            matches = list(punctuation_pattern.finditer(bef))
                            if matches:
                                p = matches[-1].end()
                                t = bef[p:].strip()
                            else:
                                t = bef.strip()
                            if min_desc_len <= len(t) <= max_desc_len:
                                chapter_desc = t

                    # 4. ：后面的内容
                    if not chapter_desc:
                        colon_pos = chapter_content.find('：')
                        if colon_pos != -1:
                            t = chapter_content[colon_pos+1:].strip()
                            if min_desc_len <= len(t) <= max_desc_len:
                                chapter_desc = t

                    # 5. ——后面的内容
                    if not chapter_desc:
                        dash_pos = chapter_content.find('——')
                        if dash_pos != -1:
                            t = chapter_content[dash_pos+2:].strip()
                            if min_desc_len <= len(t) <= max_desc_len:
                                chapter_desc = t

                    # 6. 兜底：段落前7-14字
                    if not chapter_desc:
                        first_period_pos = chapter_content.find('。')
                        if first_period_pos != -1 and first_period_pos >= min_desc_len:
                            t = chapter_content[:first_period_pos].strip()
                        else:
                            t = chapter_content[:max_desc_len].strip()
                        if min_desc_len <= len(t) <= max_desc_len:
                            chapter_desc = t

                    # ========== 清洗标题符号 ==========
                    # 1. 移除所有中文/英文标点
                    chapter_desc = clean_symbol_pattern.sub('', chapter_desc)
                    # 2. 移除不可见字符
                    chapter_desc = invisible_chars.sub('', chapter_desc)
                    # 3. 移除Windows非法字符
                    chapter_desc = re.sub(illegal_chars, '', chapter_desc)
                    # 4. 去除首尾空格/制表符
                    chapter_desc = chapter_desc.replace('　', ' ').replace('\t', ' ').strip()
                    # 5. 兜底：清洗后若为空/仅空格，置为空
                    if not chapter_desc or chapter_desc.isspace():
                        chapter_desc = ""

                    # 生成章节名
                    if chapter_desc:
                        chapter_name = f"第{chapter_num}章 {chapter_desc}"
                    else:
                        chapter_name = f"第{chapter_num}章"

                    # 添加到候选章节列表
                    chapters.append((chapter_name, chapter_content))
                    start_pos = end_pos
                    chapter_num += 1

                # 第二步：处理最后一章（不足1200字合并到上一章）
                if len(chapters) >= 2:  # 至少有两个候选章节时才需要合并
                    last_chapter_name, last_chapter_content = chapters[-1]
                    # 检查最后一章字数是否不足1200
                    if len(last_chapter_content) < min_chars:
                        print(f"  最后一章字数{len(last_chapter_content)}<1200，合并到上一章")
                        # 将最后一章内容合并到倒数第二章
                        prev_chapter_name, prev_chapter_content = chapters[-2]
                        merged_content = prev_chapter_content + last_chapter_content
                        chapters[-2] = (prev_chapter_name, merged_content)
                        # 删除最后一章
                        del chapters[-1]

                # 第三步：重新编号章节并合并为一个文件
                merged_content = ""
                for idx, (c_name, c_content) in enumerate(chapters):
                    # 重新编号章节名（避免合并后编号断层）
                    # 提取原章节编号，替换为连续编号，从用户指定的起始章节数开始
                    current_chapter_num = start_chapter + idx
                    num_match = re.search(r'第(\d+)章', c_name)
                    if num_match:
                        old_num = num_match.group(1)
                        new_chapter_name = c_name.replace(f"第{old_num}章", f"第{current_chapter_num}章")
                    else:
                        new_chapter_name = f"第{current_chapter_num}章" if not c_name else c_name
                    
                    # 合并内容，在每个章节前添加章节名
                    merged_content += new_chapter_name + "\n" + c_content + "\n\n"

                # 写入回原文件
                try:
                    with open(file_path, 'w', encoding=used_encoding or 'utf-8', errors='replace') as f:
                        f.write(merged_content)
                except Exception as write_err:
                    print(f"  错误：写入{file_name}失败 - {str(write_err)}")
                    fail_files.append(file_name)
                    continue

                print(f"  处理完成：{file_name} → 插入{len(chapters)}个章节标题（已清理空行）")
                success_files += 1

            except Exception as e:
                print(f"  出错：{file_name} - {str(e)}")
                traceback.print_exc()
                fail_files.append(file_name)
                continue

    # 输出处理汇总
    print("\n" + "="*60)
    print(f"处理汇总：")
    print(f"   总计扫描TXT文件：{total_files} 个")
    print(f"   成功处理：{success_files} 个")
    print(f"   失败/跳过：{len(fail_files)} 个")
    if fail_files:
        print(f"   失败文件列表：{', '.join(fail_files)}")
    print("="*60)


if __name__ == "__main__":
    split_novel_files()
    # 防止bat运行后窗口立即关闭
    input("\n全部处理完成！\n--问题反馈，功能定制，软件制作，请加：xy8011\n按任意键退出...")
