import streamlit as st
import json
import random
import os

st.set_page_config(page_title="Математическа академия", layout="centered")

# --- ФУНКЦИИ ---
def load_tasks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- МЕНЮТА В SIDEBAR ---
st.sidebar.title("📚 Избор на ниво")

# 1. Избор на клас (Папките в data/)
grade_opt = {
    "1. Клас": "grade_1",
    "2. Клас": "grade_2",
    "3. Клас": "grade_3"
}
selected_grade = st.sidebar.selectbox("Избери клас:", list(grade_opt.keys()))
folder = grade_opt[selected_grade]

# 2. Избор на тема (Файловете в избраната папка)
# Взимаме списък с всички .json файлове в папката
data_path = f"data/{folder}"
if os.path.exists(data_path):
    files = [f for f in os.listdir(data_path) if f.endswith('.json')]
    # Превръщаме името на файла в красиво име за менюто (напр. 'math.json' -> 'Math')
    clean_names = {f.replace('.json', '').capitalize(): f for f in files}
    
    if clean_names:
        selected_theme_name = st.sidebar.selectbox("Избери тема:", list(clean_names.keys()))
        selected_file = clean_names[selected_theme_name]
        full_path = os.path.join(data_path, selected_file)
    else:
        st.error("Няма намерени теми в тази папка.")
        st.stop()
else:
    st.error(f"Папката {data_path} не съществува в GitHub.")
    st.stop()

# --- ЛОГИКА НА ТЕСТА ---
if 'current_task' not in st.session_state or st.sidebar.button("Нулирай теста"):
    all_tasks = load_tasks(full_path)
    st.session_state.tasks_pool = all_tasks
    st.session_state.current_task = random.choice(all_tasks)
    st.session_state.streak = 0
    st.session_state.level = 'easy'

st.title(f"📖 {selected_theme_name} ({selected_grade})")

# Показване на задачата
task = st.session_state.current_task
st.write(f"### Задача: {task['question']}")

user_ans = st.text_input("Твоят отговор:", key="ans_input")

if st.button("Провери"):
    if user_ans.strip() == str(task['answer']):
        st.success("✅ Браво! Продължавай така.")
        st.session_state.streak += 1
        
        # Тук можеш да добавиш логиката за смяна на нива (easy -> medium)
        # За момента просто избираме нова задача от същия файл
        st.session_state.current_task = random.choice(st.session_state.tasks_pool)
        st.rerun()
    else:
        st.error(f"❌ Грешка. Опитай отново! (Серията ти от верни отговори се нулира)")
        st.session_state.streak = 0
        st.rerun()

st.sidebar.divider()
st.sidebar.write(f"🔥 Серия: {st.session_state.streak} верни")
