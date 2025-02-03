import re

def parse_spice_file(sp_file_path):
    # 打开并读取SPICE文件
    with open(sp_file_path, 'r') as file:
        spice_data = file.readlines()

    # 查找所有的.SUBCKT定义，并提取名称和端口
    subckt_info = []
    subckt_name = None
    ports = []

    for line in spice_data:
        line = line.strip()  # 去除行两边的空格
        if line.startswith('*') or not line:  # 跳过注释行和空行
            continue
        if line.startswith('.SUBCKT'):
            # 解析子电路名称和端口
            match = re.match(r'\.SUBCKT\s+(\S+)\s+(.*)', line)
            if match:
                subckt_name = match.group(1)  # 获取子电路名称
                ports = match.group(2).split()  # 获取端口列表
                subckt_info.append({'subckt_name': subckt_name, 'ports': ports})

    return subckt_info

# 解析 .sp 文件，提取等效电路名称和端口
sp_file_path = 'wyz.sp'  # 替换为你的SPICE文件路径
subcircuit_info = parse_spice_file(sp_file_path)

# 输出解析结果
for subckt in subcircuit_info:
    print(f"Subcircuit: {subckt['subckt_name']}")
    print(f"Ports: {', '.join(subckt['ports'])}")
