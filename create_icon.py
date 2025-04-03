#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """创建一个简单的图标文件"""
    # 创建一个 256x256 的图像，背景为白色
    img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制一个圆形背景
    draw.ellipse([20, 20, 236, 236], fill=(52, 152, 219))
    
    # 绘制一个计算器形状
    draw.rectangle([80, 60, 176, 196], fill=(255, 255, 255))
    draw.rectangle([80, 60, 176, 196], outline=(0, 0, 0), width=3)
    
    # 绘制计算器按钮
    for i in range(3):
        for j in range(3):
            draw.rectangle([90 + i*30, 70 + j*30, 110 + i*30, 90 + j*30], fill=(240, 240, 240))
            draw.rectangle([90 + i*30, 70 + j*30, 110 + i*30, 90 + j*30], outline=(0, 0, 0), width=1)
    
    # 绘制等号按钮
    draw.rectangle([90, 160, 166, 180], fill=(240, 240, 240))
    draw.rectangle([90, 160, 166, 180], outline=(0, 0, 0), width=1)
    
    # 保存为ICO文件
    img.save('icon.ico', format='ICO')
    print("图标已创建: icon.ico")

if __name__ == "__main__":
    create_icon() 