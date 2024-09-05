import streamlit as st
import pandas as pd

# 设置页面标题
st.set_page_config(page_title="数据集整理应用")

# 初始化会话状态
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['background_info', 'question', 'answer'])
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'add_data_clicked' not in st.session_state:
    st.session_state.add_data_clicked = False


# 定义函数
def load_data():
    uploaded_file = st.session_state.uploaded_file
    if uploaded_file is not None:
        st.session_state.data = pd.read_csv(uploaded_file)
        st.session_state.current_index = 0
        st.success("数据加载成功！")


def save_data():
    st.session_state.data.to_csv("dataset.csv", index=False)
    st.success("数据保存成功！")


def add_data_clicked():
    st.session_state.add_data_clicked = True


def update_data():
    st.session_state.data.loc[st.session_state.current_index] = [
        st.session_state.edit_background,
        st.session_state.edit_question,
        st.session_state.edit_answer
    ]
    st.success("数据更新成功！")


def delete_data():
    st.session_state.data = st.session_state.data.drop(st.session_state.current_index).reset_index(drop=True)
    if st.session_state.current_index >= len(st.session_state.data):
        st.session_state.current_index = max(0, len(st.session_state.data) - 1)
    st.success("数据删除成功！")


def change_index(step):
    new_index = st.session_state.current_index + step
    if 0 <= new_index < len(st.session_state.data):
        st.session_state.current_index = new_index


# 主应用界面
st.title("数据集整理应用")

# 侧边栏：数据加载和保存
with st.sidebar:
    st.header("数据操作")
    st.file_uploader("选择CSV文件", type="csv", key="uploaded_file", on_change=load_data)
    if st.button("保存数据"):
        save_data()

# 添加新数据的部分
st.header("添加新数据")
new_background = st.text_area("新背景信息", key="new_background")
new_question = st.text_input("新问题", key="new_question")
new_answer = st.text_area("新答案", key="new_answer")

if st.button("添加数据", on_click=add_data_clicked):
    pass

if st.session_state.add_data_clicked:
    if new_question:  # 只检查问题是否填写
        new_data = pd.DataFrame({
            'background_info': [new_background],
            'question': [new_question],
            'answer': [new_answer]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.session_state.current_index = len(st.session_state.data) - 1
        st.success("数据添加成功！")
        st.session_state.add_data_clicked = False
        st.experimental_rerun()
    else:
        st.warning("请至少填写问题后再添加数据。")
        st.session_state.add_data_clicked = False

# 主界面：数据浏览和编辑
st.header("浏览和编辑现有数据")
if len(st.session_state.data) > 0:
    st.write(f"当前数据索引：{st.session_state.current_index + 1}/{len(st.session_state.data)}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("上一条", on_click=change_index, args=(-1,)):
            pass
    with col2:
        if st.button("下一条", on_click=change_index, args=(1,)):
            pass
    with col3:
        if st.button("删除当前数据", on_click=delete_data):
            pass

    current_data = st.session_state.data.iloc[st.session_state.current_index]
    edit_background = st.text_area("背景信息", current_data['background_info'], key="edit_background")
    edit_question = st.text_input("问题", current_data['question'], key="edit_question")
    edit_answer = st.text_area("答案", current_data['answer'], key="edit_answer")

    if st.button("更新数据"):
        update_data()
else:
    st.write("当前没有数据。请在上方添加新数据或从侧边栏加载数据。")

# 显示当前数据集
st.header("当前数据集")
st.dataframe(st.session_state.data)