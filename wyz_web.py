#E:\pycharm_python\pythonProject\venv\Lib\site-packages\streamlit

#run app.py

import PySpice.Probe
import streamlit as st
import schemdraw
schemdraw.use('matplotlib')
import schemdraw.elements as elm
import matplotlib.pyplot as plt

# 使用 schemdraw 创建电路图
def draw_circuit():
    # 创建电路图对象
    d = schemdraw.Drawing()

    # 添加电池元件
    d.add(elm.Battery().up().label('9V'))

    # 添加电阻元件
    d.add(elm.Resistor().right().label('1kΩ'))

    # 添加导线连接
    d.add(elm.Line().right())
    d.add(elm.Ground())

    # 返回matplotlib的figure对象
    image_bytes = d.draw(canvas="matplotlib")#https://schemdraw.readthedocs.io/en/latest/classes/drawing.html
    return image_bytes.fig


# 获取电路图
fig = draw_circuit()

# 显示电路图
st.pyplot(fig)


