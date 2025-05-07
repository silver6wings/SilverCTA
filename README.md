# SilverCTA

---

# 项目简介

SilverCTA 是基于 [天勤量化](https://www.shinnytech.com/products/tqsdk) 搭建的期货量化交易策略框架

项目还在早期，各方面有限，欢迎大家提意见，完善功能

# 环境配置

建议 Python 版本 3.10

## 安装指令

> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

其他可用镜像

1) https://pypi.tuna.tsinghua.edu.cn/simple/ 清华大学
2) https://pypi.mirrors.ustc.edu.cn/simple/ 中国科技大学
3) http://pypi.mirrors.ustc.edu.cn/simple/ 中国科学技术大学
4) http://mirrors.aliyun.com/pypi/simple/ 阿里云

# 使用方法

## 账号配置

新建 `credentials.py` 并在文件中配置你的天勤量化的账号和密码

格式参考 `credentials_sample.py` 中的内容

## 运行策略

`run_sample.py` 是框架使用模板

`run_shield.py` 是最基本的止损防护
