import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="我的个人行程计划", page_icon="📅", layout="wide")

st.title("📅 个人行程计划表")

# 定义数据保存的文件名
DATA_FILE = "itinerary_data.csv"

# 初始化或加载数据
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["日期", "时间", "活动内容", "地点", "备注"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# 侧边栏：添加新行程
st.sidebar.header("➕ 添加新行程")
with st.sidebar.form("add_form", clear_on_submit=True):
    date = st.date_input("日期", datetime.today())
    time = st.time_input("时间", datetime.now().time())
    activity = st.text_input("活动内容* (必填)")
    location = st.text_input("地点")
    notes = st.text_area("备注")
    
    submitted = st.form_submit_button("保存行程")
    
    if submitted:
        if activity.strip() == "":
            st.error("活动内容不能为空！")
        else:
            # 将新数据添加到 DataFrame 中
            new_data = pd.DataFrame({
                "日期": [date.strftime("%Y-%m-%d")],
                "时间": [time.strftime("%H:%M")],
                "活动内容": [activity],
                "地点": [location],
                "备注": [notes]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            # 按日期和时间排序
            df = df.sort_values(by=["日期", "时间"]).reset_index(drop=True)
            save_data(df)
            st.success("行程添加成功！")
            st.rerun() # 刷新页面显示最新数据

# 主页面：展示行程
st.subheader("📋 我的行程列表")

if df.empty:
    st.info("目前还没有任何行程安排，请在左侧添加！")
else:
    # 提供日期筛选功能
    dates = df["日期"].unique().tolist()
    selected_date = st.selectbox("筛选日期 (默认显示全部)", ["全部"] + dates)
    
    if selected_date != "全部":
        display_df = df[df["日期"] == selected_date]
    else:
        display_df = df
        
    # 显示数据表格
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # 删除功能
    st.markdown("---")
    st.subheader("🗑️ 删除行程")
    delete_index = st.selectbox("选择要删除的行程序号 (对应表格行数，从0开始)", range(len(df)))
    if st.button("删除选中的行程"):
        df = df.drop(delete_index).reset_index(drop=True)
        save_data(df)
        st.success("删除成功！")
        st.rerun()