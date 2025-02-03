import streamlit as st
import pandas as pd
import numpy as np
import os
from vectfit3 import vectfit
from vectfit3 import opts
from scipy.constants import pi
import skrf as rf
import wyz_io
# 定义一个函数来清理并转换为复数
def to_complex(val):
    try:
        # 替换 'i' 为 'j'，然后转换为复数
        val = val.replace('i', 'j')  # 替换 'i' 为 'j'
        return complex(val)  # 转换为复数
    except ValueError:
        # 如果无法转换为复数，打印错误并返回 NaN
        print(f"无法转换为复数: {val}")
        return np.nan


# 函数用于验证路径的合法性
def is_valid_path(path):
    # 检查路径是否存在且为有效目录或文件
    return os.path.isdir(path) or os.path.isfile(path)
# markdown
st.markdown('西安电子科技大学')

# 设置网页标题
st.title('环境效应仿真支持平台V0.0')
# 展示一级标题
st.header('1. 场路转化说明')
st.text('本仿真平台支持将电磁场仿真得到的电磁数据利用矢量拟合等方法转化为时域电路模型')

### 场路转化模块
####1. 定义一个文件长传按钮，支持的类型暂定为txt，xls以及csv三种类型
uploaded_file_set = st.file_uploader("选择文件:", type=["txt", "csv", "xls", "xlsx", "ztm"], accept_multiple_files=True)
feild2cuirt_start = st.button("场路转化开始")

spice_model_path = st.text_input('请输入spice模型文件存储路径', max_chars=100, help='最大长度为100字符')
# 检查路径是否为空
if spice_model_path:
    # 如果路径不合法，提示用户重新输入
    if not is_valid_path(spice_model_path):
        st.error(f"路径 '{spice_model_path}' 不合法！请确保路径存在且是文件夹或文件。")
    else:
        st.success(f"路径 '{spice_model_path}' 合法！")
Z_f_n_n_list = []
fre_list = []
if len(uploaded_file_set) != 0:
    for uploaded_file in uploaded_file_set:
        st.write(uploaded_file.name)
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        print("文件名:", file_name)  # 输出: 文件名: /home/user/documents/example
        print("扩展名:", file_extension)  # 输出: 扩展名: .txt
        match file_extension:
            case ".txt":
                dataframe = pd.read_csv(uploaded_file, delimiter=',', header=None)
                st.write(dataframe)
                # 假设文件中的列已经包含复数形式的字符串
                # 将字符串转换为复数类型
                df_complex = dataframe.applymap(to_complex)
                arr = df_complex.to_numpy()
                opts["asymp"] = 3  # Modified to include D and E in fitting
                opts["phaseplot"] = True  # Modified to include the phase angle graph
                N = arr.shape[1]
                weights = np.ones(N, dtype=np.float64)
                n = 3
                # Order of aproximation
                poles = -2 * pi * np.logspace(0, 4, n, dtype=np.complex128)  # Initial searching poles
                arr = np.transpose(arr)
                s = arr[:, 0]
                f = arr[:, 1]
                (SER, poles, rmserr, fit) = vectfit(f, s, poles, weights, opts)
                aaaa = 666;
                ####
            case ".ztm":
                ztm_file = uploaded_file#"E:\公司工作（低空防御）\场路仿真\场路转换算法\Composite_ZCM_3\Composite_ZCM_Configuration.xml"
                result_data,fre_data = wyz_io.read_matrix_from_txt(ztm_file)
                Z_f_n_n_list.append(result_data)
                fre_list.append(fre_data)
                ceshi = 1

            case _:
                print("文件格式错误")

    #####这里需要对数据进行排序
    frequency_ordered_index = np.argsort(fre_list)  ####Z矩阵也需要按照这个进行处理
    Z_f_n_n_list_ordered=[]
    frequency_ordered = []
    for fer_ordered in frequency_ordered_index:
        Z_f_n_n_list_ordered.append(Z_f_n_n_list[fer_ordered])
        frequency_ordered.append(fre_list[fer_ordered])
    Z_fnn_matrix = np.stack(Z_f_n_n_list_ordered, axis=0)


    ntw = rf.Network(frequency=np.array(frequency_ordered)*1e6, z=Z_fnn_matrix)
    #ntw2 = rf.Network.from_z(Z_fnn_matrix,f=np.array(frequency_ordered) * 1e6)
    print(ntw)
    vf = rf.VectorFitting(ntw)


    vf.vector_fit(n_poles_real=1, n_poles_cmplx=2,fit_constant=False)
    passive_flag = vf.is_passive()
    vf.plot_convergence()
    vf.passivity_enforce()  # won't do anything if model is already passive
    vf.write_spice_subcircuit_s('wyz2.sp')

