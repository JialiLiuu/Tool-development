# SQL编译器开发

### 设计：test.cpp用于分割SQL字符串建立语法树；calculate.py用于读取py脚本文件提取SQL字符串，传给test.cpp编译成的动态链接库，如.so或者.dll

#### 前期目标：提取SQL引入的其他表名
#### 后期目标：提取表名及条件
