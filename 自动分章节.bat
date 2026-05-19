@echo off
chcp 65001 >nul
echo ==============================
echo      小说TXT文件分割工具
echo ==============================
echo 当前处理目录：%cd%
echo 使用的Python路径：D:\便携Python\python.exe
echo ------------------------------

:: 检查指定路径的Python是否存在
if not exist "D:\便携Python\python.exe" (
    echo ❌ 错误：未找到指定的Python程序！
    echo    路径：D:\便携Python\python.exe
    echo    请检查路径是否正确，或修改bat文件中的Python路径。
    pause
    exit /b 1
)

:: 让用户输入起始章节号
set /p start_chapter=请输入起始章节号(默认7): 

:: 如果用户没有输入，则使用默认值7
if "%start_chapter%"=="" set start_chapter=7

echo.
echo 正在启动处理程序，起始章节号: %start_chapter%
echo ------------------------------

:: 运行Python脚本（%~dp0表示bat文件所在目录，确保脚本和bat同目录）
"D:\便携Python\python.exe" "%~dp0split_novel.py" --start %start_chapter%

:: 保持窗口打开，方便查看结果
echo ------------------------------
echo 处理结束！按任意键退出...
pause >nul