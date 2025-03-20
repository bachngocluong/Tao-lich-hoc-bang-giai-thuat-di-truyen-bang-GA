import random
import numpy as np
import streamlit as st
import pandas as pd
import json
import os

# Thêm CSS tùy chỉnh
st.markdown("""
    <style>
    /* Toàn bộ trang chính */
    .main { 
        background-color: #0aaf8e; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); 
        color: white; 
    }
    
    /* Nút bấm */
    .stButton>button { 
        background-color: #ff7675; 
        color: white; 
        border: none; 
        border-radius: 5px; 
        padding: 10px 20px; 
        cursor: pointer; 
        transition: transform 0.2s ease, background-color 0.3s ease; 
    }
    .stButton>button:hover { 
        background-color: #d63031; 
        transform: scale(1.05); 
    }
    
    /* Ô nhập liệu */
    .stTextInput>div>input, 
    .stNumberInput>div>input, 
    .stTextArea>div>textarea { 
        border: 2px solid #ffffff; 
        border-radius: 10px; 
        padding: 10px; 
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1); 
        transition: box-shadow 0.3s ease; 
    }
    .stTextInput>div>input:focus, 
    .stNumberInput>div>input:focus, 
    .stTextArea>div>textarea:focus { 
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.8); 
        border-color: #ffffff; 
    }
    
    /* Tiêu đề */
    h1, h2, h3 { 
        color: #ffffff; 
        font-family: 'Arial', sans-serif; 
        text-align: center; 
        font-weight: bold; 
        text-shadow: 2px 2px rgba(0, 0, 0, 0.2); 
    }
    
    /* Sidebar */
    .sidebar .sidebar-content { 
        background-color: #16d39a; 
        border-radius: 10px; 
        padding: 15px; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); 
        color: white; 
    }
    </style>
""", unsafe_allow_html=True)

# Đường dẫn file lưu trữ dữ liệu
DATA_FILE = "schedule_data.json"

# ============================== HÀM LƯU VÀ TẢI DỮ LIỆU ============================== #
def save_data():
    data = {
        "classroom_data": st.session_state.classroom_data,
        "teacher_data": st.session_state.teacher_data,
        "student_groups": st.session_state.student_groups,
        "courses": st.session_state.courses
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.classroom_data = data.get("classroom_data", [])
            st.session_state.teacher_data = data.get("teacher_data", [])
            st.session_state.student_groups = data.get("student_groups", [])
            st.session_state.courses = data.get("courses", [])
        st.info("Đã tải dữ liệu từ lần nhập trước!")

# ============================== GIAO DIỆN STREAMLIT ============================== #
st.title("Lập Lịch Học Tự Động bằng Thuật Toán Di Truyền")
st.markdown("Ứng dụng này tự động lưu dữ liệu sau mỗi lần nhập.")

# Sidebar điều hướng
st.sidebar.title("Điều Hướng")
menu = st.sidebar.radio("Chọn chức năng", ["Nhập Dữ Liệu", "Xem Lịch Học"])

# Khởi tạo session state nếu chưa có
if 'classroom_data' not in st.session_state:
    st.session_state.classroom_data = []
    st.session_state.teacher_data = []
    st.session_state.student_groups = []
    st.session_state.courses = []
    load_data()  # Tải dữ liệu từ file nếu có

# ============================== HÀM NHẬP DỮ LIỆU ============================== #
def input_data():
    st.header("Nhập Dữ Liệu Đầu Vào")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Phòng Học", "Giáo Viên", "Nhóm Sinh Viên", "Môn Học"])
    
    with tab1:
        st.subheader("Thông Tin Phòng Học")
        num_classrooms = st.number_input("Số lượng phòng học", min_value=1, step=1, key="num_classrooms")
        for i in range(num_classrooms):
            with st.expander(f"Phòng học {i+1}", expanded=False):
                room_name = st.text_input(f"Tên phòng học {i+1}", key=f"room_name_{i}")
                capacity = st.number_input(f"Sức chứa", min_value=1, step=1, key=f"capacity_{i}")
                equipment = st.text_input(f"Thiết bị (cách nhau bằng dấu phẩy)", key=f"equip_{i}")
                if st.button(f"Lưu phòng {i+1}", key=f"save_room_{i}"):
                    st.session_state.classroom_data.append({
                        "name": room_name, "capacity": capacity, "equipment": equipment.split(",")
                    })
                    save_data()  # Tự động lưu sau khi thêm
                    st.success(f"Đã lưu phòng {room_name}")
    
    with tab2:
        st.subheader("Thông Tin Giáo Viên")
        num_teachers = st.number_input("Số lượng giáo viên", min_value=1, step=1, key="num_teachers")
        for i in range(num_teachers):
            with st.expander(f"Giáo viên {i+1}", expanded=False):
                teacher_name = st.text_input(f"Tên giáo viên {i+1}", key=f"teacher_name_{i}")
                available_times = st.text_area(f"Thời gian rảnh (Thứ-HH:MM-HH:MM, cách nhau dấu phẩy)", key=f"time_{i}")
                if st.button(f"Lưu giáo viên {i+1}", key=f"save_teacher_{i}"):
                    st.session_state.teacher_data.append({
                        "name": teacher_name, "available_times": [t.strip() for t in available_times.split(",") if t.strip()]
                    })
                    save_data()  # Tự động lưu sau khi thêm
                    st.success(f"Đã lưu giáo viên {teacher_name}")
    
    with tab3:
        st.subheader("Thông Tin Nhóm Sinh Viên")
        num_groups = st.number_input("Số lượng nhóm sinh viên", min_value=1, step=1, key="num_groups")
        for i in range(num_groups):
            with st.expander(f"Nhóm sinh viên {i+1}", expanded=False):
                group_name = st.text_input(f"Tên nhóm {i+1}", key=f"group_name_{i}")
                student_count = st.number_input(f"Số sinh viên", min_value=1, step=1, key=f"size_{i}")
                if st.button(f"Lưu nhóm {i+1}", key=f"save_group_{i}"):
                    st.session_state.student_groups.append({
                        "name": group_name, "size": student_count
                    })
                    save_data()  # Tự động lưu sau khi thêm
                    st.success(f"Đã lưu nhóm {group_name}")
    
    with tab4:
        st.subheader("Thông Tin Môn Học")
        num_courses = st.number_input("Số lượng môn học", min_value=1, step=1, key="num_courses")
        for i in range(num_courses):
            with st.expander(f"Môn học {i+1}", expanded=False):
                course_name = st.text_input(f"Tên môn học {i+1}", key=f"course_name_{i}")
                teacher = st.text_input(f"Giáo viên", key=f"course_teacher_{i}")
                group = st.text_input(f"Nhóm sinh viên", key=f"course_group_{i}")
                duration = st.number_input(f"Thời lượng (số tiết)", min_value=1, step=1, key=f"duration_{i}")
                required_equipment = st.text_input(f"Thiết bị yêu cầu (cách nhau bằng dấu phẩy)", key=f"req_equip_{i}")
                if st.button(f"Lưu môn {i+1}", key=f"save_course_{i}"):
                    st.session_state.courses.append({
                        "name": course_name, "teacher": teacher, "group": group, 
                        "duration": duration, "required_equipment": required_equipment.split(",")
                    })
                    save_data()  # Tự động lưu sau khi thêm
                    st.success(f"Đã lưu môn {course_name}")

# ============================== THUẬT TOÁN DI TRUYỀN ============================== #
def generate_schedule():
    schedule = []
    for course in st.session_state.courses:
        teacher = next((t for t in st.session_state.teacher_data if t['name'] == course['teacher']), None)
        if not teacher:
            continue
        room = random.choice(st.session_state.classroom_data)
        time = random.choice(teacher['available_times'])
        schedule.append({"Môn học": course["name"], "Phòng học": room["name"], "Giáo viên": course["teacher"], "Nhóm sinh viên": course["group"], "Thời gian": time})
    return schedule

def fitness_function(schedule):
    score = 0
    used_times = set()
    for entry in schedule:
        if entry['Thời gian'] not in used_times:
            score += 1
            used_times.add(entry['Thời gian'])
    return score

def crossover(parent1, parent2):
    crossover_point = len(parent1) // 2
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(schedule):
    idx = random.randint(0, len(schedule) - 1)
    teacher = next((t for t in st.session_state.teacher_data if t['name'] == schedule[idx]['Giáo viên']), None)
    if teacher:
        schedule[idx]["Thời gian"] = random.choice(teacher['available_times'])
    return schedule

def genetic_algorithm():
    population_size = 100
    generations = 500
    mutation_rate = 0.1
    
    population = [generate_schedule() for _ in range(population_size)]
    for _ in range(generations):
        population = sorted(population, key=lambda s: fitness_function(s), reverse=True)
        new_population = population[:10]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return population[0]

# ============================== CHẠY ỨNG DỤNG ============================== #
if menu == "Nhập Dữ Liệu":
    input_data()
    if st.button("Xóa Dữ Liệu", key="clear_data"):
        st.session_state.classroom_data = []
        st.session_state.teacher_data = []
        st.session_state.student_groups = []
        st.session_state.courses = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.success("Đã xóa toàn bộ dữ liệu!")
elif menu == "Xem Lịch Học":
    st.header("Lịch Học Tối Ưu")
    if not st.session_state.courses:
        st.warning("Vui lòng nhập dữ liệu trước khi tạo lịch!")
    elif st.button("Tạo Lịch Học", key="generate_schedule"):
        with st.spinner("Đang tạo lịch học tối ưu..."):
            best_schedule = genetic_algorithm()
        st.subheader("Kết Quả Lịch Học")
        df_schedule = pd.DataFrame(best_schedule)
        styled_df = df_schedule.style.set_properties(**{
            'background-color': '#ffffff',
            'color': '#333333',
            'border-color': '#cccccc',
            'text-align': 'center',
            'font-size': '14px',
            'padding': '8px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center')]}
        ])
        st.dataframe(styled_df, height=300)
        st.download_button("Tải xuống lịch học (CSV)", df_schedule.to_csv(index=False), "lich_hoc.csv", "text/csv")