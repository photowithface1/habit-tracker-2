import streamlit as st
import json
import os

DATA_FILE = "habit_web_data.json"

# 預設資料
def default_data():
    return {
        "habits": {},
        "rewards": {
            "喝杯珍奶": 10,
            "看一集影集": 20,
            "週末外出活動": 50
        },
        "score": 0
    }

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return default_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化資料
data = load_data()
st.title("🎯 每日習慣與獎勵追蹤")

# ==== 設定習慣 ====
st.sidebar.header("📝 新增或修改習慣")
new_habit = st.sidebar.text_input("習慣名稱")
new_score = st.sidebar.number_input("分數", min_value=1, step=1)
if st.sidebar.button("➕ 加入習慣"):
    if new_habit:
        data["habits"][new_habit] = new_score
        save_data(data)
        st.sidebar.success(f"已新增習慣「{new_habit}」")

# ==== 完成習慣打卡 ====
st.header("✅ 今天完成的習慣")
total_score = 0

completed = []
for habit, point in data["habits"].items():
    if st.checkbox(f"{habit}（+{point}分）"):
        total_score += point
        completed.append(habit)

if st.button("👉 完成打卡"):
    data["score"] += total_score
    save_data(data)
    st.success(f"已新增 {total_score} 分，目前總分為 {data['score']} 分！")

st.divider()

# ==== 兌換獎勵 ====
st.header("🎁 兌換獎勵")
for reward, cost in data["rewards"].items():
    if st.button(f"兌換：{reward}（{cost} 分）"):
        if data["score"] >= cost:
            data["score"] -= cost
            save_data(data)
            st.success(f"你成功兌換了「{reward}」，剩餘 {data['score']} 分。")
        else:
            st.warning("分數不足，請繼續努力！")

st.divider()
st.metric("⭐ 目前累積總分：", f"{data['score']} 分")
