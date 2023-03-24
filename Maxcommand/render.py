# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs



def render_and_save(width, height, file_path):
    # 设置渲染输出大小
    rt.renderWidth = width
    rt.renderHeight = height

    # 创建一个 Point2 对象
    output_size = rt.Point2(width, height)

    # 渲染当前视图并获取位图
    rendered_image = rt.render(outputSize=output_size)

    # 保存位图
    rendered_image.filename = file_path
    rt.save(rendered_image)
    #关闭预览窗口
    rt.close(rendered_image)


def reViews():
    rt.redrawViews()