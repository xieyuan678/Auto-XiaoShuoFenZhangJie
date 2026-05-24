import subprocess
from datetime import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'git_diff_log.txt')

try:
    result = subprocess.run(['git', 'diff', 'HEAD'], capture_output=True, text=True, cwd=script_dir)
    diff_content = result.stdout.strip()

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")

        if diff_content:
            f.write(diff_content)
            f.write("\n")
            print(f"已保存git diff到：{log_file}")
        else:
            f.write("（无变更）\n")
            print("当前没有变更内容")

except Exception as e:
    print(f"错误：{e}")