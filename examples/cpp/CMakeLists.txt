cmake_minimum_required(VERSION 3.15)
project(easy_trainer_examples CXX)

set(CMAKE_CXX_STANDARD 17)

# 源码是 UTF-8 中文注释, MSVC 默认按本地代码页解码会把汉字里的 0x5C 当成续行符
if(MSVC)
    add_compile_options(/utf-8)
endif()

# 依赖: OpenCV 与 ONNX Runtime(下载解压后把根目录路径填进 ONNXRUNTIME_DIR)
find_package(OpenCV REQUIRED)
set(ONNXRUNTIME_DIR "" CACHE PATH "ONNX Runtime 解压目录(含 include/ 与 lib/)")

include_directories(${OpenCV_INCLUDE_DIRS} ${ONNXRUNTIME_DIR}/include)
link_directories(${ONNXRUNTIME_DIR}/lib)

foreach(target detect segment classify)
    add_executable(${target} ${target}.cpp)
    target_link_libraries(${target} ${OpenCV_LIBS} onnxruntime)
endforeach()
