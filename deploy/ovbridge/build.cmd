@echo off
rem 编译 OpenVINO 转换桥接 ovbridge.dll (改过 ovbridge.cpp 后跑一次, 产物已随仓库提交)
rem   build.cmd [OpenVINO 目录] [输出目录]
rem OpenVINO 目录要含 include\ 与 libs\ (pip 装的 site-packages\openvino 就是这个结构);
rem 默认取 %OVI_DIR%, 再退回 D:\OpenVINO\sdk
chcp 65001 >nul
setlocal
set "HERE=%~dp0"
set "OVI=%~1"
if "%OVI%"=="" set "OVI=%OVI_DIR%"
if "%OVI%"=="" set "OVI=D:\OpenVINO\sdk"
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%HERE%..\Win.deploy\native"

if not exist "%OVI%\include\openvino\openvino.hpp" goto :noovi
if not exist "%OVI%\libs\openvino.lib" goto :noovi

set "VCVARS="
for %%R in (
  "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools"
  "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools"
  "%ProgramFiles%\Microsoft Visual Studio\2022\Community"
  "%ProgramFiles%\Microsoft Visual Studio\2022\Professional"
  "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise"
  "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Community"
) do if exist "%%~R\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%%~R\VC\Auxiliary\Build\vcvars64.bat"
if "%VCVARS%"=="" goto :novc

call "%VCVARS%" >nul
if errorlevel 1 goto :novc
if not exist "%OUT%" mkdir "%OUT%"

pushd "%OUT%"
cl /nologo /LD /EHsc /std:c++17 /MD /O2 /utf-8 /I"%OVI%\include" "%HERE%ovbridge.cpp" /link /LIBPATH:"%OVI%\libs" openvino.lib /OUT:ovbridge.dll
set "RC=%ERRORLEVEL%"
del /q ovbridge.exp ovbridge.lib ovbridge.obj >nul 2>&1
popd

if not "%RC%"=="0" goto :failed
echo 已生成 %OUT%\ovbridge.dll
exit /b 0

:failed
echo 编译失败 (cl 返回 %RC%)
exit /b %RC%

:noovi
echo 找不到 OpenVINO 的 C++ 文件 (需要 include\openvino\openvino.hpp 与 libs\openvino.lib)
echo 当前目录: %OVI%
echo   pip 装的在  <python>\Lib\site-packages\openvino
exit /b 1

:novc
echo 没找到 MSVC 的 vcvars64.bat, 需要 VS 2022 的"使用 C++ 的桌面开发"组件
exit /b 1
