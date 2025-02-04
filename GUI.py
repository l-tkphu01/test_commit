from tkinter import *
from tkinter.ttk import Combobox, Treeview, Notebook
from tkinter import ttk, messagebox
import pandas as pd
import os
from PIL import Image, ImageTk
import time
import math 
# Đọc dữ liệu từ file CSV
df = pd.read_csv('data.csv')

def my_function():
    # Đoạn mã bạn muốn tính thời gian chạy
    time.sleep(2)  # Giả sử chương trình mất 2 giây để thực hiện

# Ghi lại thời gian bắt đầu
start_time = time.time()

def search_data(column, value, data):
    if column == "Tất cả" or value == "Tất cả":
        df_filtered = data
    elif column and value:
        df_filtered = data[data[column].astype(str).str.contains(value, case=False, na=False)]
    elif column:
        df_filtered = data[[column]]
    else:
        df_filtered = data
    return df_filtered

def sort_data(column, data, reverse=False):
    if column:
        df_sorted = data.sort_values(by=column, ascending=not reverse)
        return df_sorted
    return data

def locDuLieu():
    df_new = pd.read_csv('newFileCleanData.csv')
    xemDuLieu(df_new)

def crudData(dataframe=None):
    # Tạo cửa sổ mới cho CRUD
    new_window = Toplevel(window)
    new_window.title("Xem dữ liệu trước khi lọc")
    new_window.attributes('-fullscreen', True)
    new_window.config(bg="#f0f8ff")

    # Tiêu đề
    label_title = Label(new_window, text="CRUD NEW DATA", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title.pack(pady=20)

    # Tabs cho nội dung (có thể thêm nếu cần)
    notebook = Notebook(new_window)
    notebook.pack(fill=BOTH, expand=True, pady=10)

    # Nút quay lại để đóng cửa sổ
    button_back_new = Button(new_window, text="Quay lại", command=new_window.destroy, font=("Arial", 14), bg="#5F9EA0", fg="white", relief="raised")
    button_back_new.pack(pady=10)

    # Tạo khung màu cyan bao quanh các nút CRUD
    cyan_frame = Frame(new_window, bg="#00FFFF", padx=40, pady=40)
    cyan_frame.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Khung chứa các nút CRUD
    frame_crud = Frame(cyan_frame, bg="#E0FFFF")
    frame_crud.pack(padx=10, pady=10)

    # Thiết lập cấu hình hàng cho chiều dọc
    for i in range(4):
        frame_crud.grid_rowconfigure(i, weight=1)

    # Nút CREATE
    button_create = Button(frame_crud, text="CREATE", command=lambda: create_data(dataframe), font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", width=30, height=2)
    button_create.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Nút READ
    button_read = Button(frame_crud, text="READ", command=lambda: read_data(dataframe), font=("Arial", 14), bg="#2196F3", fg="white", relief="raised", width=30, height=2)
    button_read.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Nút UPDATE
    button_update = Button(frame_crud, text="UPDATE", command=update_data, font=("Arial", 14), bg="#FFC107", fg="white", relief="raised", width=30, height=2)
    button_update.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Nút DELETE
    button_delete = Button(frame_crud, text="DELETE", command=lambda: delete_data(dataframe), font=("Arial", 14), bg="#F44336", fg="white", relief="raised", width=30, height=2)
    button_delete.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")


def create_data(df_new=None):
    # Tên file CSV cố định
    csv_file = "data.csv"

    if df_new is None:
        if os.path.exists(csv_file):
            df_new = pd.read_csv(csv_file)
        else:
            df_new = pd.DataFrame(columns=["Column1", "Column2", "Column3"])

    # Tạo cửa sổ mới cho phần create
    create_window = Toplevel()
    create_window.title("Thêm dữ liệu mới")
    create_window.attributes('-fullscreen', True)
    create_window.config(bg="#f0f8ff")

    label_title = Label(create_window, text="<< CREATE DATA >>", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title.pack(pady=20)

    # Chia cửa sổ thành hai phần
    frame_left = Frame(create_window, bg="#f0f8ff", width=600)
    frame_left.pack(side=LEFT, fill=BOTH, expand=True)

    frame_right = Frame(create_window, bg="#e6f7ff", width=600)
    frame_right.pack(side=RIGHT, fill=BOTH, expand=True)

    # --- Phần nhập liệu ---
    label_title_left = Label(frame_left, text="Nhập Dữ Liệu", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title_left.pack(pady=10)

    frame_data = Frame(frame_left, bg="#ffffff", relief="solid", bd=2)
    frame_data.pack(padx=5, pady=10, fill=BOTH, expand=True)

    labels = []
    entries = []

    # Duyệt qua các cột của df_new
    for idx, col in enumerate(df_new.columns):
        label = Label(frame_data, text=f"{col}:", font=("Arial", 12), bg="#ffffff", fg="#333333")
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(frame_data, font=("Arial", 12))
        entry.grid(row=idx, column=1, padx=10, pady=5)
        labels.append(label)
        entries.append(entry)

    # --- Biến và hàm liên quan đến phân trang ---
    current_page = 1
    page_size = 50
    current_data = df_new.copy()

    def update_page_label(current_page, total_pages):
        label_page.config(text=f"Trang {current_page}/{total_pages}")

    def paginate_data(page):
        total_pages = (len(current_data) // page_size) + (1 if len(current_data) % page_size != 0 else 0)
        start_idx = (page - 1) * page_size
        end_idx = page * page_size
        return current_data.iloc[start_idx:end_idx], total_pages

    def load_paginated_data(page):
        paginated_data, total_pages = paginate_data(page)
        tree.delete(*tree.get_children())  # Xóa dữ liệu cũ
        for _, row in paginated_data.iterrows():
            tree.insert("", "end", values=list(row))
        update_page_label(page, total_pages)
        button_prev.config(state=DISABLED if page == 1 else NORMAL)
        button_next.config(state=DISABLED if page == total_pages else NORMAL)

    def go_to_next_page():
        nonlocal current_page
        current_page += 1
        load_paginated_data(current_page)

    def go_to_previous_page():
        nonlocal current_page
        current_page -= 1
        load_paginated_data(current_page)

    # --- Hàm lưu dữ liệu ---
    def save_data():
        nonlocal df_new, current_page
        new_data = {}
        for idx, col in enumerate(df_new.columns):
            value = entries[idx].get().strip()
            if not value:
                messagebox.showwarning("Lỗi", f"Không được để trống ô {col}. Vui lòng nhập dữ liệu.")
                return 
            new_data[col] = value

        # Chuyển dữ liệu mới thành DataFrame
        new_row = pd.DataFrame([new_data])

        # Cập nhật DataFrame và ghi vào file CSV
        if os.path.exists(csv_file):
            df_new = pd.concat([df_new, new_row], ignore_index=True)  # Cập nhật df_new trước
        else:
            df_new = new_row

        # Ghi dữ liệu vào file CSV
        df_new.to_csv(csv_file, index=False)
        print(f"Dữ liệu đã được lưu vào {csv_file}")

        # Làm mới phân trang với dữ liệu mới
        load_paginated_data(current_page)

        # Xóa các ô nhập liệu (đặt lại thành rỗng)
        for entry in entries:
            entry.delete(0, END)

    # Khung chứa nút Lưu và Đóng
    button_frame = Frame(frame_left, bg="#f0f8ff")
    button_frame.pack(pady=10)

    save_button = Button(button_frame, text="Lưu", command=save_data, font=("Arial", 12), relief="raised", width=20, height=2)
    save_button.pack(side=LEFT, padx=10)

    close_button = Button(button_frame, text="Đóng", command=create_window.destroy, font=("Arial", 12), relief="raised", width=20, height=2)
    close_button.pack(side=LEFT, padx=10)
        
    # --- Phần hiển thị dữ liệu ---
    label_view = Label(frame_right, text="Dữ Liệu Hiện Có", font=("Arial", 18, 'bold'), bg="#e6f7ff", fg="#333333")
    label_view.pack(pady=10)

    # --- Khung điều khiển tìm kiếm và sắp xếp ---
    frame_controls = Frame(frame_right, bg="#e6f7ff", relief="solid", bd=2)
    frame_controls.pack(fill=X, padx=10, pady=(10, 10))

    # Tìm kiếm
    label_search_column = Label(frame_controls, text="Tìm kiếm theo cột:", bg="#e6f7ff", font=("Arial", 12))
    label_search_column.grid(row=0, column=0, padx=10, pady=10)

    # Combobox để chọn cột
    combo_search_column = Combobox(frame_controls, values=["Tất cả"] + list(df_new.columns), font=("Arial", 12))
    combo_search_column.grid(row=0, column=1, padx=10, pady=10)
    combo_search_column.set("Tất cả")

    label_value = Label(frame_controls, text="Nhập giá trị:", bg="#e6f7ff", font=("Arial", 12))
    label_value.grid(row=0, column=2, padx=10, pady=10)

    # Combobox để chọn giá trị tìm kiếm
    combo_values = Combobox(frame_controls, font=("Arial", 12))
    combo_values.grid(row=0, column=3, padx=10, pady=10)

    label_value = Label(frame_controls, text="Nhập giá trị:", bg="#e6f7ff", font=("Arial", 12))
    label_value.grid(row=0, column=2, padx=10, pady=10)

    combo_values = Combobox(frame_controls, font=("Arial", 12))
    combo_values.grid(row=0, column=3, padx=10, pady=10)

    def update_values(event):
        column = combo_search_column.get()  
        if column and column != "Tất cả":  
            unique_values = df_new[column].dropna().unique().tolist()
            combo_values['values'] = ["Tất cả"] + unique_values  
        else:
            combo_values['values'] = ["Tất cả"]

    combo_search_column.bind("<<ComboboxSelected>>", update_values)

    def perform_search():
        selected_column = combo_search_column.get()  
        selected_value = combo_values.get() 

        if not selected_value:
            messagebox.showwarning("Lỗi", "Vui lòng chọn giá trị để tìm kiếm.")
            return

        if selected_column == "Tất cả":
            filtered_data = df_new[df_new.apply(lambda row: selected_value.lower() in row.astype(str).str.lower().values, axis=1)]
        else:
            filtered_data = df_new[df_new[selected_column].astype(str).str.contains(selected_value, case=False, na=False)]

        # Hiển thị kết quả tìm kiếm trong bảng
        tree.delete(*tree.get_children())
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=list(row))

    def search_and_paginate():
        nonlocal current_data, current_page
        selected_column = combo_search_column.get()
        search_value = combo_values.get()
        if selected_column and search_value:
            current_data = df_new[df_new[selected_column].astype(str).str.contains(search_value, case=False, na=False)]
        else:
            current_data = df_new
        current_page = 1
        load_paginated_data(current_page)

    button_search = Button(frame_controls, text="Tìm kiếm", command=search_and_paginate, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised")
    button_search.grid(row=0, column=4, padx=10, pady=10)

    # Sắp xếp
    label_sort_column = Label(frame_controls, text="Sắp xếp theo cột:", bg="#e6f7ff", font=("Arial", 12))
    label_sort_column.grid(row=1, column=0, padx=10, pady=10)

    combo_sort_column = Combobox(frame_controls, values=list(df_new.columns), font=("Arial", 12))
    combo_sort_column.grid(row=1, column=1, padx=10, pady=10)
    combo_sort_column.set("Chọn cột")

    def sort_and_paginate(reverse=False):
        nonlocal current_data, current_page
        selected_column = combo_sort_column.get()
        if selected_column:
            current_data = current_data.sort_values(by=selected_column, ascending=not reverse)
            current_page = 1
            load_paginated_data(current_page)
        
    def reset_table():
        nonlocal current_page, current_data
        combo_search_column.set("Tất cả")
        combo_values.set("")
        current_page = 1
        current_data = df_new.copy()
        load_paginated_data(current_page)

    button_reset = Button(frame_controls, text="Reset", command=reset_table, font=("Arial", 12), bg="#f44336", fg="white", relief="raised")
    button_reset.grid(row=0, column=5, padx=10, pady=10)


    button_sort_asc = Button(frame_controls, text="Sắp xếp tăng", command=lambda: sort_and_paginate(reverse=False), font=("Arial", 12), bg="#2196F3", fg="white", relief="raised")
    button_sort_asc.grid(row=1, column=2, padx=10, pady=10)

    button_sort_desc = Button(frame_controls, text="Sắp xếp giảm", command=lambda: sort_and_paginate(reverse=True), font=("Arial", 12), bg="#FF5722", fg="white", relief="raised")
    button_sort_desc.grid(row=1, column=3, padx=10, pady=10)

    # Khung bảng dữ liệu
    frame_table_container = Frame(frame_right, bg="#e6f7ff", relief="solid", bd=2)
    frame_table_container.pack(fill=BOTH, expand=True, padx=(10, 10), pady=(10, 0))

    y_scroll = Scrollbar(frame_table_container, orient=VERTICAL)
    y_scroll.pack(side=RIGHT, fill=Y)

    x_scroll = Scrollbar(frame_table_container, orient=HORIZONTAL)
    x_scroll.pack(side=BOTTOM, fill=X)

    tree = Treeview(frame_table_container, columns=list(df_new.columns), yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set, show="headings")
    tree.pack(fill=BOTH, expand=True)

    for col in df_new.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=CENTER)

    y_scroll.config(command=tree.yview)
    x_scroll.config(command=tree.xview)

    # Thanh điều khiển phân trang
    frame_pagination = Frame(frame_right, bg="#e6f7ff")
    frame_pagination.pack(fill=X, padx=(10, 10), pady=(10, 10))

    button_prev = Button(frame_pagination, text="<< Trước", command=go_to_previous_page, font=("Arial", 12), bg="#FFC107", fg="white", relief="raised")
    button_prev.pack(side=LEFT, padx=10)

    label_page = Label(frame_pagination, text="Trang 1/1", font=("Arial", 12), bg="#e6f7ff", fg="#333333")
    label_page.pack(side=LEFT, padx=10)

    button_next = Button(frame_pagination, text="Tiếp >>", command=go_to_next_page, font=("Arial", 12), bg="#FFC107", fg="white", relief="raised")
    button_next.pack(side=LEFT, padx=10)

    # Hiển thị dữ liệu ban đầu
    load_paginated_data(current_page)
    
def read_data(dataframe):
    df_new1 = pd.read_csv('data.csv')
    xemDuLieu(df_new1)

# Hàm phân trang
def paginate_data(data, page, page_size=10):
    total_pages = (len(data) + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return data.iloc[start_idx:end_idx], total_pages

# Hàm tìm kiếm dữ liệu
def search_data(column, value, data):
    if column == "Tất cả" or value == "Tất cả":
        return data
    return data[data[column] == value]

# Hàm sắp xếp dữ liệu
def sort_data(column, data, reverse=False):
    if column in data.columns:
        return data.sort_values(by=column, ascending=not reverse)
    return data

def update_data():
    # Đọc dữ liệu từ file CSV
    dataframe = pd.read_csv("data.csv")

    # Tạo cửa sổ cập nhật
    update_window = Toplevel(window)
    update_window.title("Xem dữ liệu trước khi lọc")
    update_window.attributes('-fullscreen', True)
    update_window.config(bg="#f0f8ff")

    # Tiêu đề
    label_title = Label(update_window, text="CẬP NHẬT DỮ LIỆU", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title.pack(pady=20)

    # Khung chứa nút và bộ lọc
    frame_buttons = Frame(update_window, bg="#e6f7ff")
    frame_buttons.pack(pady=10)

    # Dropdown chọn cột
    label_column = Label(frame_buttons, text="Chọn cột:", bg="#e6f7ff", font=("Arial", 12))
    label_column.grid(row=0, column=0, padx=10)
    combo_columns = Combobox(frame_buttons, values=list(dataframe.columns), font=("Arial", 12))
    combo_columns.grid(row=0, column=1, padx=10)

    # Dropdown nhập giá trị
    label_value = Label(frame_buttons, text="Nhập giá trị:", bg="#e6f7ff", font=("Arial", 12))
    label_value.grid(row=0, column=2, padx=10)
    combo_values = Combobox(frame_buttons, font=("Arial", 12))
    combo_values.grid(row=0, column=3, padx=10)

    def update_values(event):
        column = combo_columns.get()
        if column and column != "Tất cả":
            unique_values = dataframe[column].dropna().unique().tolist()
            combo_values['values'] = ["Tất cả"] + unique_values
        else:
            combo_values['values'] = ["Tất cả"]

    combo_columns.bind("<<ComboboxSelected>>", update_values)

    # Nút tìm kiếm
    def search_and_paginate():
        nonlocal current_data, current_page
        current_data = search_data(combo_columns.get(), combo_values.get(), dataframe)
        current_page = 1
        paginated_data, total_pages = paginate_data(current_data, current_page)
        load_data(paginated_data)
        update_page_label(current_page, total_pages)

    button_search = Button(frame_buttons, text="Tìm kiếm", command=search_and_paginate, font=("Arial", 12), bg="#4CAF50", fg="white")
    button_search.grid(row=0, column=4, padx=10)

    # Nút Reset
    def reset_filters():
        nonlocal current_data, current_page
        combo_columns.set("")
        combo_values.set("")
        current_data = dataframe  # Reset lại toàn bộ dữ liệu
        current_page = 1
        paginated_data, total_pages = paginate_data(current_data, current_page)
        load_data(paginated_data)
        update_page_label(current_page, total_pages)

    button_reset = Button(frame_buttons, text="Reset", command=reset_filters, font=("Arial", 12), bg="#FF5722", fg="white")
    button_reset.grid(row=0, column=5, padx=10)

    # Khung bao quanh bảng dữ liệu
    frame_data_container = Frame(update_window, bg="#f0f8ff")
    frame_data_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Khung chứa dữ liệu
    frame_content = Frame(frame_data_container, bg="#e6f7ff")
    frame_content.pack(fill=BOTH, expand=True)

    # Tạo Treeview
    tree = Treeview(frame_content, columns=list(dataframe.columns), show="headings")
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=CENTER)

    # Thêm Scrollbar dọc
    scroll_y = Scrollbar(frame_content, orient=VERTICAL, command=tree.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scroll_y.set)

    # Thêm Scrollbar ngang
    scroll_x = Scrollbar(frame_content, orient=HORIZONTAL, command=tree.xview)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.configure(xscrollcommand=scroll_x.set)

    tree.pack(side=LEFT, fill=BOTH, expand=True)

    current_data = dataframe
    current_page = 1

    def load_data(data):
        tree.delete(*tree.get_children())
        for index, row in data.iterrows():
            tree.insert("", "end", iid=index, values=list(row))  # Dùng index làm iid

    def paginate_data(data, page, per_page=50):
        total_pages = -(-len(data) // per_page)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        return data.iloc[start_idx:end_idx], total_pages

    def update_page_label(current_page, total_pages):
        label_page.config(text=f"Trang {current_page}/{total_pages}")

    def change_page(direction):
        nonlocal current_page
        paginated_data, total_pages = paginate_data(current_data, current_page + direction)
        if 1 <= current_page + direction <= total_pages:
            current_page += direction
            load_data(paginated_data)
            update_page_label(current_page, total_pages)

    frame_pagination = Frame(update_window, bg="#e6f7ff")
    frame_pagination.pack(pady=10)
    label_page = Label(frame_pagination, text="")
    label_page.pack()

    btn_prev = Button(frame_pagination, text="Trang trước", command=lambda: change_page(-1))
    btn_prev.pack(side=LEFT, padx=5)
    btn_next = Button(frame_pagination, text="Trang tiếp", command=lambda: change_page(1))
    btn_next.pack(side=LEFT, padx=5)

    def open_update_window():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một dòng để cập nhật!")
            return

        selected_index = tree.index(selected_item[0])  # Sử dụng tree.index để lấy chỉ số chính xác của dòng đã chọn
        selected_row = current_data.iloc[selected_index]  # Lấy từ current_data

        # Tạo cửa sổ nổi
        edit_window = Toplevel(update_window)
        edit_window.title("Chỉnh sửa dữ liệu")
        edit_window.geometry("600x400")  # Tăng kích thước để dễ hiển thị
        edit_window.config(bg="#f0f8ff")

        # Tạo canvas để bao bọc nội dung
        canvas = Canvas(edit_window, bg="#f0f8ff")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Thanh cuộn dọc
        v_scrollbar = Scrollbar(edit_window, orient=VERTICAL, command=canvas.yview)
        v_scrollbar.pack(side=RIGHT, fill=Y)

        # Kết nối canvas với thanh cuộn
        canvas.configure(yscrollcommand=v_scrollbar.set)

        # Frame nội dung bên trong canvas
        frame_content = Frame(canvas, bg="#f0f8ff")
        canvas.create_window((0, 0), window=frame_content, anchor="nw")

        # Cập nhật kích thước vùng cuộn
        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_content.bind("<Configure>", update_scroll_region)

        # Tạo các trường nhập dữ liệu
        entry_widgets = {}
        for idx, col in enumerate(dataframe.columns):
            label = Label(frame_content, text=col, font=("Arial", 12), bg="#f0f8ff")
            label.grid(row=idx, column=0, pady=5, padx=5, sticky="w")
            entry = Entry(frame_content, font=("Arial", 12), width=30)
            entry.insert(0, selected_row[col])
            entry.grid(row=idx, column=1, pady=5, padx=5)
            entry_widgets[col] = entry

        # Nút lưu
        def save_updates():
            nonlocal dataframe, current_data
            for col, entry in entry_widgets.items():
                new_value = entry.get()
                if new_value != selected_row[col]:  # Chỉ cập nhật nếu giá trị mới khác giá trị cũ
                    dataframe.at[selected_index, col] = new_value  # Cập nhật vào dataframe gốc
                    current_data.at[selected_index, col] = new_value  # Cập nhật vào current_data

            dataframe.to_csv("data.csv", index=False)
            load_data(current_data)  # Hiển thị lại dữ liệu sau khi cập nhật
            edit_window.destroy()
            messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật!")

        # Thêm nút lưu vào cuối cùng
        Button(frame_content, text="Lưu", font=("Arial", 14), bg="#4CAF50", fg="white", command=save_updates).grid(
            row=len(dataframe.columns), column=0, columnspan=2, pady=20)

        # Bật cuộn bằng chuột
        def on_mousewheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

    button_update = Button(update_window, text="Cập nhật giá trị", command=open_update_window, font=("Arial", 12), bg="#2196F3", fg="white")
    button_update.pack(pady=10)

    # Nút Đóng
    button_close = Button(update_window, text="Đóng", command=update_window.destroy, font=("Arial", 12), bg="#F44336", fg="white")
    button_close.pack(pady=10)

    paginated_data, total_pages = paginate_data(dataframe, current_page)
    load_data(paginated_data)
    update_page_label(current_page, total_pages)

def delete_data(dataframe):
    # Tạo cửa sổ mới cho phần delete
    delete_window = Toplevel()
    delete_window.title("Thêm dữ liệu mới")
    delete_window.attributes('-fullscreen', True)
    delete_window.config(bg="#f0f8ff")

    label_title = Label(delete_window, text="DELETE DATA", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title.pack(pady=20)

    # Tabs cho nội dung
    notebook = Notebook(delete_window)
    notebook.pack(fill=BOTH, expand=True, pady=10)

def xemBieuDo():
    charts_window = Toplevel(window)
    charts_window.title("Biểu đồ thống kê")
    charts_window.attributes('-fullscreen', True)
    charts_window.config(bg="#f0f8ff")

    # Frame chứa phần chọn biểu đồ
    frame_chart_selection = Frame(charts_window, bg="#f0f8ff")
    frame_chart_selection.pack(pady=5, anchor="n")  # Giảm khoảng cách phía trên

    # Nhãn hướng dẫn
    label_select_chart = Label(frame_chart_selection, text="Chọn biểu đồ:", font=("Arial", 14), bg="#f0f8ff")
    label_select_chart.grid(row=0, column=0, padx=10, pady=5)  # Giảm khoảng cách

    # Combobox chọn biểu đồ
    chart_options = [
        "Số lượng phim theo thời gian", 
        "Top 5 công ty sản xuất", 
        "Top đạo diễn theo thể loại", 
        "Top 10 thể loại phim", 
        "Biểu đồ phân tán dựa trên ngân sách và doanh thu",
        "Biểu đồ tương quan giữa các cột dữ liệu",
        "Ngân sách đầu tư qua các năm",
        "Doanh thu của từng thể loại qua từng năm",
        "Các từ khóa phổ biến",
        "Tổng doanh thu của từng thể loại theo từng tháng",
        "Số lượng phim phát hành theo tháng",
        "Doanh thu trung bình theo từng thể loại",
        "Ngân sách của từng thể loại qua từng năm"
    ]
    combo_charts = Combobox(frame_chart_selection, values=chart_options, font=("Arial", 12), width=50, state="readonly")
    combo_charts.grid(row=0, column=1, padx=10, pady=5)  # Giảm khoảng cách
    combo_charts.set("Chọn biểu đồ để xem")

    # Nút quay lại
    button_back_new = Button(frame_chart_selection, text="Quay lại", command=charts_window.destroy, font=("Arial", 14), bg="#FF5733", fg="white", relief="raised")
    button_back_new.grid(row=0, column=2, padx=10, pady=5)  # Giảm khoảng cách

    # Frame chứa hình ảnh biểu đồ
    frame_chart_image = Frame(charts_window, bg="#f0f8ff")
    frame_chart_image.pack(expand=True, fill=BOTH, padx=10, pady=10, anchor="n")  # Điều chỉnh padding và căn phía trên

    # Label để hiển thị biểu đồ
    label_chart = Label(frame_chart_image, bg="#f0f8ff")
    label_chart.pack(expand=True, anchor="n", padx=20, pady=10)  # Đẩy nội dung lên trên

    # Từ điển ánh xạ tên biểu đồ với tên file
    chart_images = {
        "Số lượng phim theo thời gian": "soluongphimquacacnam.png",
        "Top 5 công ty sản xuất": "top5congty.png",
        "Top đạo diễn theo thể loại": "top6daodien.png",
        "Top 10 thể loại phim": "Top10theloaiduocyeuthich.png",
        "Biểu đồ phân tán dựa trên ngân sách và doanh thu": "Bieudophantan.png",
        "Biểu đồ tương quan giữa các cột dữ liệu": "Bieudotuongquan.png", 
        "Ngân sách đầu tư qua các năm": "Ngansachtheotungnam.png",
        "Doanh thu của từng thể loại qua từng năm": "Bieudomientheodoanhthu.png",
        "Các từ khóa phổ biến": "Tukhoaphobien.png",
        "Tổng doanh thu của từng thể loại theo từng tháng": "Tongdoanhthutheloaiphim.png",
        "Số lượng phim phát hành theo tháng": "Soluongphimphathangtheothang.png",
        "Doanh thu trung bình theo từng thể loại": "Doanhthutrungbinhtheotheloai.png",
        "Ngân sách của từng thể loại qua từng năm": "Bieudomientheongansach.png"
    }

    # Hàm cập nhật biểu đồ
    def update_chart(event):
        selected_chart = combo_charts.get()
        if selected_chart in chart_images:
            img = Image.open(chart_images[selected_chart])
            img = img.resize((1080, 672))  # Điều chỉnh kích thước hình ảnh nếu cần
            img = ImageTk.PhotoImage(img)
            label_chart.configure(image=img)
            label_chart.image = img  # Giữ tham chiếu để tránh bị garbage collector xóa

    combo_charts.bind("<<ComboboxSelected>>", update_chart)  # Liên kết Combobox với hàm
    


# Hàm phân trang
def paginate_data(data, page, rows_per_page=50):
    total_rows = len(data)
    total_pages = math.ceil(total_rows / rows_per_page)
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    paginated_data = data.iloc[start_idx:end_idx]
    return paginated_data, total_pages

# Định nghĩa các hàm cho các nút
def xemDuLieu(dataframe=df):
    new_window = Toplevel(window)
    new_window.title("Xem dữ liệu trước khi lọc")
    new_window.attributes('-fullscreen', True)
    new_window.config(bg="#f0f8ff")  # Background color for the new window

    label_title = Label(new_window, text="Dữ liệu phim từ năm", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
    label_title.pack(pady=20)

    # Tabs cho nội dung
    notebook = Notebook(new_window)
    notebook.pack(fill=BOTH, expand=True, pady=10)

    # Tạo tab dữ liệu chính
    tab_data = Frame(notebook, bg="#e6f7ff")
    notebook.add(tab_data, text="Dữ liệu")

    frame_new_buttons = Frame(tab_data, bg="#e6f7ff")
    frame_new_buttons.pack(pady=10)

    label_column = Label(frame_new_buttons, text="Chọn cột:", bg="#e6f7ff", font=("Arial", 12))
    label_column.grid(row=0, column=0, padx=10, pady=10)

    combo_columns = Combobox(frame_new_buttons, values=["Tất cả"] + list(dataframe.columns), font=("Arial", 12))
    combo_columns.grid(row=0, column=1, padx=10, pady=10)

    label_value = Label(frame_new_buttons, text="Nhập giá trị:", bg="#e6f7ff", font=("Arial", 12))
    label_value.grid(row=0, column=2, padx=10, pady=10)

    combo_values = Combobox(frame_new_buttons, font=("Arial", 12))
    combo_values.grid(row=0, column=3, padx=10, pady=10)

    def update_values(event):
        column = combo_columns.get()
        if column and column != "Tất cả":
            unique_values = dataframe[column].dropna().unique().tolist()
            combo_values['values'] = ["Tất cả"] + unique_values
        else:
            combo_values['values'] = ["Tất cả"]

    combo_columns.bind("<<ComboboxSelected>>", update_values)
    
    # Biến để lưu trữ dữ liệu hiện tại và trang hiện tại
    current_data = dataframe
    current_page = 1

    # Frame chứa nội dung dữ liệu
    frame_new_content = Frame(tab_data, bg="#e6f7ff")
    frame_new_content.pack(fill=BOTH, expand=True)

    # Treeview với thanh cuộn ngang và dọc
    tree = Treeview(frame_new_content, columns=list(dataframe.columns), show="headings")
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=CENTER)

    # Thanh cuộn ngang
    scroll_x = Scrollbar(frame_new_content, orient=HORIZONTAL, command=tree.xview)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.configure(xscrollcommand=scroll_x.set)

    # Thanh cuộn dọc
    scroll_y = Scrollbar(frame_new_content, orient=VERTICAL, command=tree.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scroll_y.set)

    tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Frame chứa nút điều hướng trang
    frame_pagination = Frame(tab_data)
    frame_pagination.pack(pady=10)

    label_page = Label(frame_pagination, text="")
    label_page.pack()

    def update_page_label(current_page, total_pages):
        label_page.config(text=f"Trang {current_page}/{total_pages}")

    def load_data(data):
        tree.delete(*tree.get_children())
        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))

    def change_page(direction):
        nonlocal current_page, current_data
        paginated_data, total_pages = paginate_data(current_data, current_page + direction)
        
        if 1 <= current_page + direction <= total_pages:
            current_page += direction
            load_data(paginated_data)
            update_page_label(current_page, total_pages)

    btn_prev = Button(frame_pagination, text="Trang trước", command=lambda: change_page(-1))
    btn_prev.pack(side=LEFT, padx=5)

    btn_next = Button(frame_pagination, text="Trang tiếp", command=lambda: change_page(1))
    btn_next.pack(side=LEFT, padx=5)
    
    def search_and_paginate():
        nonlocal current_data, current_page
        current_data = search_data(combo_columns.get(), combo_values.get(), dataframe)
        current_page = 1
        paginated_data, total_pages = paginate_data(current_data, current_page)
        load_data(paginated_data)
        update_page_label(current_page, total_pages)

    def sort_and_paginate(column, reverse=False):
        nonlocal current_data, current_page
        current_data = sort_data(column, current_data, reverse)
        current_page = 1
        paginated_data, total_pages = paginate_data(current_data, current_page)
        load_data(paginated_data)
        update_page_label(current_page, total_pages)

    button_search_new = Button(frame_new_buttons, text="Tìm kiếm", command=lambda: load_data(search_data(combo_columns.get(), combo_values.get(), dataframe)), font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised")
    button_search_new.grid(row=0, column=4, padx=10, pady=10)
    
    button_search_new = Button(frame_new_buttons, text="Tìm kiếm", command=search_and_paginate,  font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised")
    button_search_new.grid(row=0, column=4, padx=10, pady=10)

    label_sort = Label(frame_new_buttons, text="Sắp xếp theo:")
    label_sort.grid(row=0, column=5, padx=10, pady=10)

    combo_sort = Combobox(frame_new_buttons, values=list(dataframe.columns))
    combo_sort.grid(row=0, column=6, padx=10, pady=10)

    button_sort_az = Button(frame_new_buttons, text="Sắp xếp tăng", command=lambda: sort_and_paginate(combo_sort.get(), False), font=("Arial", 12), bg="#2196F3", fg="white", relief="raised")
    button_sort_az.grid(row=0, column=7, padx=10, pady=10)

    button_sort_za = Button(frame_new_buttons, text="Sắp xếp giảm", command=lambda: sort_and_paginate(combo_sort.get(), True), font=("Arial", 12), bg="#FF5722", fg="white", relief="raised")
    button_sort_za.grid(row=0, column=8, padx=10, pady=10)

    # Tải dữ liệu ban đầu với phân trang
    initial_data, total_pages = paginate_data(dataframe, current_page)
    load_data(initial_data)
    update_page_label(current_page, total_pages)

    # Tab phụ (ví dụ: thống kê)
    tab_stats = Frame(notebook, bg="#f0f8ff")
    notebook.add(tab_stats, text="Thống kê")

    label_stats = Label(tab_stats, text="Thống kê dữ liệu (ví dụ: tổng số phim, doanh thu trung bình)", font=("Arial", 12), bg="#f0f8ff")
    label_stats.pack(pady=10)

    total_movies = len(dataframe)
    avg_revenue = dataframe["revenue"].mean() if "revenue" in dataframe.columns else 0

    stats_text = f"Tổng số phim: {total_movies}\nDoanh thu trung bình: {avg_revenue:.2f}"
    label_stats_data = Label(tab_stats, text=stats_text, font=("Arial", 12), bg="#f0f8ff")
    label_stats_data.pack(pady=10)

    button_back_new = Button(new_window, text="Quay lại", command=new_window.destroy, font=("Arial", 14), bg="#FF5733", fg="white", relief="raised")
    button_back_new.pack(pady=10)

# Tạo cửa sổ chính

window = Tk()
window.title("Dữ liệu phim nước ngoài từ năm")
window.geometry("1366x768")
window.config(bg="#000000")

label_title = Label(window, text="Dữ liệu phim nước ngoài từ năm 1966 - 2015", font=("Arial", 18, 'bold'), bg="#f0f8ff", fg="#333333")
label_title.pack(pady=20)

frame_buttons = Frame(window, bg="#ff0000")
frame_buttons.pack(pady=10)

# Gọi hàm xem dữ liệu
button_view = Button(frame_buttons, text="Xem dữ liệu", width=12, height=2, command=lambda: xemDuLieu(df), font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised")
button_view.grid(row=1, column=0, padx=5, pady=5)

button_filter = Button(frame_buttons, text="Lọc dữ liệu", width=12, height=2, command=locDuLieu, font=("Arial", 12), bg="#FF5722", fg="white", relief="raised")
button_filter.grid(row=1, column=1, padx=5, pady=5)

button_crud = Button(frame_buttons, text="CRUD", width=12, height=2, command=lambda: crudData(df), font=("Arial", 12), bg="#2196F3", fg="white", relief="raised")
button_crud.grid(row=1, column=2, padx=5, pady=5)

button_analyze = Button(frame_buttons, text="Xem biểu đồ và phân tích", width=24, height=2,command=xemBieuDo, font=("Arial", 12), bg="#ff7f50", fg="white", relief="raised" )
button_analyze.grid(row=1, column=4, padx=5, pady=5)

frame_content = Frame(window, bg="#f0f8ff")
frame_content.pack(pady=10)

button_back = Button(window, text="X", command=quit, font=("Arial", 14), bg="#FF5733", fg="white", relief="raised")
button_back.pack(pady=20)
# Ghi lại thời gian kết thúc
end_time = time.time()
# Chạy ứng dụng Tkinter
window.mainloop()


# Tính thời gian chạy
execution_time = end_time - start_time

# In ra thời gian chạy (đơn vị giây)
print(f"Thời gian chạy của chương trình là: {execution_time} giây")