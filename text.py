#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 首先尝试从项目的主模块或工具模块导入发送邮件的函数
# 例如，如果发送邮件的功能在 utils/notify.py 中，可能是：
# from utils.notify import send_email
# 或者如果配置加载在 main.py 中，可能是：
# from main import load_config, send_email  (如果main里有的话)

# 如果无法直接导入，或者不确定结构，可以手动复制需要的代码（如下面的简化版）

import yagmail  # 确保已安装 yagmail :cite[1]:cite[4]
import yaml     # 确保已安装 PyYAML
import os

def test_email_send():
    """测试邮件发送功能"""
    try:
        # 1. 加载配置 (假设配置文件是 config.yaml)
        config_path = 'config.yaml'
        if not os.path.exists(config_path):
            print(f"错误：配置文件 {config_path} 不存在！")
            return False

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        smtp_cfg = config.get('smtp', {})
        notify_cfg = config.get('notify', {})

        if not smtp_cfg or not notify_cfg:
            print("错误：配置文件中未找到 'smtp' 或 'notify' 部分！")
            return False

        if not notify_cfg.get('enable', False):
            print("通知功能未在配置中启用！")
            return False

        # 2. 使用 yagmail 连接服务器 (参考项目实际使用的库) :cite[1]:cite[4]
        # 如果你的项目用的是 smtplib:cite[5]:cite[6]:cite[9]，则需要调整代码
        yag = yagmail.SMTP(user=smtp_cfg.get('user'),
                           password=smtp_cfg.get('password'),
                           host=smtp_cfg.get('host'),
                           port=smtp_cfg.get('port', 465), # 通常465是SSL端口:cite[1]:cite[4]
                           smtp_ssl=smtp_cfg.get('ssl', True))

        # 3. 构造测试邮件内容
        test_subject = "测试邮件 - 邮箱功能验证"
        test_contents = [
            "这是一封自动发送的测试邮件。",
            "如果你能收到这封邮件，说明项目的邮箱配置是正确的。",
            "发送时间："
        ]

        # 4. 发送邮件
        yag.send(to=notify_cfg.get('to'),
                 subject=test_subject,
                 contents=test_contents)
        print("测试邮件已发送！请检查你的收件箱（和垃圾邮件箱）。")
        return True

    except Exception as e:
        print(f"发送测试邮件时出错：{e}")
        return False

if __name__ == '__main__':
    test_email_send()
