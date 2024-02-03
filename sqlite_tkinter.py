from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import pandas as pd
import os

entry_list_start = []
labels_list = []
tree_list = []
scroll_list= []

def create_db():

    global entry_list_start
    global labels_list
    if labels_list:   # удаляем последний label в списке
        labels_list.pop().destroy()

    # получаем значения с каждого label (name, surname и age)
    name = str_name.get()
    surname = str_surname.get()
    age = str_age.get()

    # создаем объект con соединения с БД
    con = sql.connect('people.db')

    if name != '' and  surname != '' and  age != '':

        # создаем объект cursor, чтобы делать SQL запросы к БД
        cur = con.cursor()

        # создаем таблицу, если ее еще не создали
        cur.execute("CREATE TABLE IF NOT EXISTS `people` (`name` STRING, `surname` STRING, 'age' INTEGER)")

        # добавляем значения в нашу таблицу
        cur.execute(f"INSERT INTO `people` VALUES ('{name}', '{surname}', '{age}')")
        con.commit()

        if entry_list_start:   # удаляем все entry
            for entry in entry_list_start:
                entry.delete(0, END)

        # обязательно закрываем cursor
        cur.close()

    else:
        # выводим label, в случае, если ввели пустые значения (такое не будем вводить в нашу БД, чтобы не копились пустые строки)
        label4 = Label(window, text='Вы ввели не все данные!', font=('Arial', 12, 'bold'), bg='red')
        label4.place(x=30, y=250)
        # добавляем в список label4, чтобы потом удалить (для обновления в window) 
        labels_list.append(label4)

    # обязательно закрываем соединение con
    con.close()

    # Выводим таблицу с обновлением
    withdraw_db()

def get_table(db):

    global tree_list, scroll_list
    if tree_list:   # удалить последний tree
        tree_list.pop().destroy()
        scroll_list.pop().destroy()

    columns = ("name", "surname", "age")
    tree = ttk.Treeview(columns=columns, show="headings")

    # cоздаем вертикальную полосу прокрутки
    scroll = Scrollbar(orient = VERTICAL, command = tree.yview)
    scroll.pack(side = RIGHT, fill = Y)

    # конфигурируем поле ввода с полосой прокрутки
    tree.config(yscrollcommand = scroll.set)
    # добавляем в список scroll, чтобы потом удалить (для обновления в window) 
    scroll_list.append(scroll)

    # расположение tree на window
    tree.place(x=400, y=50)

    # определяем заголовки с выравниваем
    tree.heading("name", text="Имя", anchor=W)
    tree.heading("surname", text="Фамилия", anchor=W)
    tree.heading("age", text="Возраст", anchor=W)

    # настраиваем столбцы
    tree.column("#1", stretch=NO, width=150)
    tree.column("#2", stretch=NO, width=150)
    tree.column("#3", stretch=NO, width=100)

    # добавляем данные
    for idx in db.index:
        name = db.loc[idx,'name']
        surname = db.loc[idx,'surname']
        age = db.loc[idx,'age']

        # если данные не пустые, то добавляем данные
        if name != '' and  surname != '' and  age != '': 
            tree.insert("", END, values=(name, surname, age))
    # добавляем в список tree, чтобы потом удалить (для обновления в window)       
    tree_list.append(tree)


def create_db_new():

    db_name = 'people.db'
    db_is_new = not os.path.exists(db_name)

    # создаем объект con соединения с БД
    con = sql.connect('people.db')

    # создаем объект cursor, чтобы делать SQL запросы к БД
    cur = con.cursor()

    if db_is_new:

        cur.execute("CREATE TABLE IF NOT EXISTS `people` (`name` STRING, `surname` STRING, 'age' INTEGER)")

        # Словарь с данными (name,surname,age)
        list_values = {
            'elem1' : 
            {'name' : 'Ira', 
            'surname' : 'Kireeva',
            'age' : '25'},
            'elem2' : 
            {'name' : 'Alex', 
            'surname' : 'Kireev',
            'age' : '31'}
        }
        # Заполняем пустую таблицу данными из словаря
        for elem in list_values:
            name = list_values.get(elem).get('name')
            surname = list_values.get(elem).get('surname')
            age = list_values.get(elem).get('age')
            cur.execute((f"INSERT INTO `people` VALUES ('{name}', '{surname}', '{age}')"))
        con.commit() # сохраняем коммитом

        # обязательно закрываем cursor
        cur.close()
        # обязательно закрываем соединение con
        con.close()

def withdraw_db():

    # создаем объект con соединения с БД
    con = sql.connect('people.db')

    # вывести столбцы из таблиц nwi_oam_ericsson, nodes_rnc, nodes_siteswitch
    db = pd.read_sql("SELECT * FROM `people`",con)

    # обязательно закрываем соединение con
    con.close()

    # выводим таблицу
    get_table(db)

# Создаем новую БД, если еще не создана
create_db_new()

# Создаем графическое окно
window = Tk()
window.title('БД') # заголовок окна
window.geometry('850x350') # размер окна

# ~~~~~~~ Name ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Добавляем label 'Имя' для ввода, в, случае, если необходимо добавить новые данные в БД
label1 = Label(window, text='Имя', font=('Hack 20', 12, 'bold'))
label1.place(x=30, y=50)
# добавляем Entry для str_name
str_name = Entry(font='Hack 20', width=10)
str_name.place(x=120, y=50)
# добавляем в список str_name, чтобы потом удалить (для обновления в window) 
entry_list_start.append(str_name)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~ Surname ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Добавляем label 'Фамилия' для ввода, в, случае, если необходимо добавить новые данные в БД
label2 = Label(window, text='Фамилия', font=('Hack 20', 12, 'bold'))
label2.place(x=30, y=100) 
# добавляем Entry для str_surname
str_surname = Entry(font='Hack 20', width=10)
str_surname.place(x=120, y=100)
# добавляем в список str_surname, чтобы потом удалить (для обновления в window)  
entry_list_start.append(str_surname)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~ Age ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Добавляем label 'Возраст' для ввода, в, случае, если необходимо добавить новые данные в БД
label3 = Label(window, text='Возраст', font=('Hack 20', 12, 'bold'))
label3.place(x=30, y=150) 
# добавляем Entry для str_age
str_age = Entry(font='Hack 20', width=10)
str_age.place(x=120, y=150) 
# добавляем в список str_age, чтобы потом удалить (для обновления в window) 
entry_list_start.append(str_age)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~ Ввод данных в db ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Добавляем button(кнопку) для ввода новых данных, если необходимо добавить новые данные в БД
btn_switch1 = Button(window, text='Внести данные', bg='orange', fg='red',
            width=20, font=("Hack 20", 16, 'bold'), command=create_db)
btn_switch1.place(x=30, y=200) 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~ Вывод данных из db ~~~~~~~~~~~~~~~~~~~~~~~~
# Добавляем button(кнопку) для вывода данных из БД
btn_switch2 = Button(window, text='Вывести данные', bg='green', fg='black',
            width=20, font=("Hack 20", 16, 'bold'), command=withdraw_db)
btn_switch2.place(x=30, y=300) 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# цикл обработки событий окна
window.mainloop()
