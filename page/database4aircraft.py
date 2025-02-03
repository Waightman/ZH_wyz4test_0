import streamlit as st
import sqlite3
import pandas as pd

# 连接数据库（如果数据库文件不存在，SQLite会自动创建）
conn = sqlite3.connect('absorber_materials.db')
cursor = conn.cursor()

# 创建表（如果表不存在）
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    frequency REAL,
    thickness REAL,
    loss_factor REAL
)
""")
conn.commit()

# 标题
st.title("吸波材料数据库")


# 显示材料数据
def view_materials(query, params=()):
    df = pd.read_sql(query, conn, params=params)
    st.dataframe(df)


# 添加材料
def add_material(name, material_type, frequency, thickness, loss_factor):
    cursor.execute("""
    INSERT INTO materials (name, type, frequency, thickness, loss_factor)
    VALUES (?, ?, ?, ?, ?)
    """, (name, material_type, frequency, thickness, loss_factor))
    conn.commit()


# 更新材料
def update_material(id, name, material_type, frequency, thickness, loss_factor):
    cursor.execute("""
    UPDATE materials
    SET name = ?, type = ?, frequency = ?, thickness = ?, loss_factor = ?
    WHERE id = ?
    """, (name, material_type, frequency, thickness, loss_factor, id))
    conn.commit()


# 删除材料
def delete_material(id):
    cursor.execute("DELETE FROM materials WHERE id = ?", (id,))
    conn.commit()


# 筛选材料（支持频率范围筛选）
def filter_materials(frequency_min, frequency_max, thickness, loss_factor):
    query = "SELECT * FROM materials WHERE 1=1"
    params = []

    if frequency_min is not None and frequency_max is not None:
        query += " AND frequency BETWEEN ? AND ?"
        params.extend([frequency_min, frequency_max])

    if thickness is not None:
        query += " AND thickness = ?"
        params.append(thickness)

    if loss_factor is not None:
        query += " AND loss_factor = ?"
        params.append(loss_factor)

    return query, params


# 显示操作面板
menu = ["查看材料", "添加材料", "更新材料", "删除材料", "筛选材料"]
choice = st.sidebar.selectbox("选择操作", menu)

if choice == "查看材料":
    st.subheader("所有材料")
    view_materials("SELECT * FROM materials")

elif choice == "添加材料":
    st.subheader("添加新材料")
    name = st.text_input("材料名称")
    material_type = st.text_input("材料类型")
    frequency = st.number_input("频率 (GHz)", min_value=0.0, step=0.1)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, step=0.1)
    loss_factor = st.number_input("损耗因子", min_value=0.0, step=0.01)

    if st.button("添加材料"):
        add_material(name, material_type, frequency, thickness, loss_factor)
        st.success("材料已添加")

elif choice == "更新材料":
    st.subheader("更新材料")
    material_id = st.number_input("输入要更新的材料ID", min_value=1, step=1)
    name = st.text_input("材料名称")
    material_type = st.text_input("材料类型")
    frequency = st.number_input("频率 (GHz)", min_value=0.0, step=0.1)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, step=0.1)
    loss_factor = st.number_input("损耗因子", min_value=0.0, step=0.01)

    if st.button("更新材料"):
        update_material(material_id, name, material_type, frequency, thickness, loss_factor)
        st.success("材料已更新")

elif choice == "删除材料":
    st.subheader("删除材料")
    material_id = st.number_input("输入要删除的材料ID", min_value=1, step=1)

    if st.button("删除材料"):
        delete_material(material_id)
        st.success("材料已删除")

elif choice == "筛选材料":
    st.subheader("筛选材料")

    # 筛选条件选择框
    frequency_min = st.number_input("最小频率 (GHz)", min_value=0.0, step=0.1, value=None)
    frequency_max = st.number_input("最大频率 (GHz)", min_value=0.0, step=0.1, value=None)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, step=0.1, value=None)
    loss_factor = st.number_input("损耗因子", min_value=0.0, step=0.01, value=None)

    if st.button("筛选"):
        if frequency_min is not None and frequency_max is not None:
            query, params = filter_materials(frequency_min, frequency_max, thickness, loss_factor)
            view_materials(query, params)
        else:
            st.warning("请输入有效的频率范围")
