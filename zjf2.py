"""
学生信息包括
学号（唯一）  姓名  性别  年龄  寝室（一间寝室最多安排4人）
寝室编号 男生（100 101 102） 女生（200 201 202）

功能包括：
1. 可以录入学生信息
2. 录入过程中可以为其分配寝室（可选自动分配或手动分配，手动分配的话如果选择的寝室人员已满，提示重新分配）
3. 可以打印各寝室人员列表（做到表格打印是加分项）
4. 可以用学号索引打印特定学生信息，可以打印所有学生信息（做到表格打印是加分项）
5. 可以为学生调整寝室（一人调整到其他寝室，两人交换寝室等，自由发挥）
6. 可以将所有信息存入文件（json格式）
7. 程序启动时，将文件中的学生信息自动导入系统
"""
import json
import random

roomdict = {}

student_list = []

# 新增学生函数
def new_student():
    global student_list
    print("*" * 50)
    print('新增学生')
    ID_studnet_list = []
    for student_dict in student_list:
        ID_studnet_list.append(student_dict['student_ID'])
    while True:
        try:
            student_ID = int(input('请输入学生学号'))
            if str(student_ID) not in ID_studnet_list:
                break
            else:
                print('您输入的学号已存在')
        except ValueError:
            print('您输入的学号有误请重新输入')
    student_name = input('请输入姓名')
    while True:
        student_sex = input('请输入性别')
        if student_sex in ('男', '女'):
            break
        print('您输入的性别有误，请重新输入')
    while True:
        try:
            student_age = int(input('请输入年龄'))
            break
        except ValueError:
                print('您输入的年龄有误，请重新输入')
    while True:
        to_room = input('输入0，自动分配寝室号:\n输入1,手动分配寝室号:')
        if to_room in ('0'):
            student_room = automatic_room(student_sex)  #调用自动分配函数  返回值为房间号
            break
        elif to_room in ('1'):
            student_room = hand_allot_room(student_sex)  #调用手动分配函数 返回值为房间号
            break
        else:
            print('输入有误请重新输入')
    student_dict = {'student_ID': str(student_ID), 'student_name': student_name, 'student_sex': student_sex, 'student_age': student_age, 'student_room': student_room}
    student_list.append(student_dict)
    saveToJson()
    print('添加%s的信息成功' % student_name)


# 寝室的自动分配的函数
def automatic_room(student_sex):
    k = 1 if student_sex == "男" else 2
    while True:
        key = str(random.randint(100 * k, 100 * k + 2))  # 保存模板{key(房间号):count(房间人数)}
        count = roomdict.setdefault(key, 0)
        if count < 4:
            roomdict[key] += 1
            break
    return key


# 显示所有学生信息的函数
def show_all_student():
    print("-" * 50)
    print("显示所有学生信息")
    print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
    print("=" * 50)
    for student_dict in student_list:
        print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
        student_dict['student_ID'], student_dict['student_name'], student_dict['student_sex'], student_dict['student_age'], student_dict['student_room']))


# 搜索学号的函数
def search_student():
    print("======================我是可爱的分割线========================")
    print("[搜索学生信息]\n")
    find_id = input("请你输入想要查找的学号:")
    for student_dict in student_list:  # 打印输出这个字典的值
        if find_id in student_dict['student_ID']:
            print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
            student_dict['student_ID'], student_dict['student_name'], student_dict['student_sex'], student_dict['student_age'],
            student_dict['student_room']))
            return
    print('你想查找的学号不存在')


# 显示寝室的函数
def show_room():
    print("寝室人员列表")
    print("[搜索寝室信息]\n")
    print("1.按寝室号搜索\n")
    print("0.返回主菜单\n")
    choice = input('请输入想要进行的操作')
    print("您想要进行的操作%s" % choice)
    if choice in ("1", '0'):
        if choice == '1':
            find_room = input('您想要查找的寝室号是:')
            for student_dict in student_list:  # 打印输出这个字典的值
                if find_room == student_dict['student_room']:
                    print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (student_dict['student_ID'], student_dict['student_name'], student_dict['student_sex'], student_dict['student_age'],student_dict['student_room']))
        else:
            return
    else:
        print('您输入的操作有误,请重新输入:')
        return


# 删除学生信息函数
def delete_student():
    print("删除学生信息界面")
    delete_ID = input('请输入您想删除的学生号是')
    for student_dict in student_list:
        if delete_ID in student_dict['student_ID']:
            print('%s号学生已经被删除' % student_dict['student_ID'])
            index = student_list.index(student_dict)
            student_list.pop(index)
            saveToJson()
            return
    print('你输入的学号不存在')


# 手动分配寝室函数
def hand_allot_room(student_sex):
    print('手动分配寝室')
    k = 1 if student_sex == '男' else 2
    while True:
        room_choice = input('请输入您想选择的寝室号')
        if room_choice in [str(x) for x in range(k*100,k*100+3)]:
            count = roomdict.setdefault(room_choice,0)
            print(room_choice)
            if count < 4:
                break
            print('该寝室已满')
        else:
            print('您输入的寝室不存在')
    return room_choice


# 双方交换寝室函数
def change_room():
    print('学生寝室交换界面')
    ID_frist = input('请输入你的学号')
    ID_second = input('请输入交换对方的学号')
    ID_list = [] #存放交换双方的空列表
    for card_dict in student_list:
        if card_dict['student_ID']==ID_frist:
            ID_list.append(card_dict)   #存放第一个学生的信息去ID_list[]
        elif card_dict['student_ID']==ID_second:
            ID_list.append(card_dict)   #存放第二个学生的信息去ID_list[]
    if ID_list[0]['student_sex']==ID_list[1]['student_sex']:
        ID_list[0]['student_room'],ID_list[1]['student_room']=ID_list[1]['student_room'],ID_list[0]['student_room']  #交换寝室号码
    else:
        print('男女有别,请换间寝室')
    saveToJson()


# 显示所有的菜单函数
def show_menu():
    while True:
        print("*" * 50)
        print("欢迎使用[寝室管理系统]")
        print()
        print("1.录入学生信息")
        print("2.显示学生信息")
        print("3.搜索学生信息")
        print("4.显示寝室人员列表")
        print("5.寝室人员调整")
        print("6.删除学生信息")
        print("0.退出管理系统")
        print("*" * 50)
        readToJson() #读取数据
        choice = input("请输入你想进行的操作是:")
        if int(choice) == 1: #录入学生信息
            if new_student():
                print("按enter键继续：")
                input()
                continue
        elif int(choice) == 2:#显示学生信息
            show_all_student()
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 3:#搜索学生信息
            search_student()
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 4: #显示寝室人员列表
            show_room()
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 5:
            change_room()  #寝室人员调整
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 6: #删除学生信息
            delete_student()
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 0:  #保存退出学生管理系统
            print("欢迎再次使用学生管理系统！")
            saveToJson()
            break

        else:
            print("请您输入操作相对应的数字：")


# 保存数据
def saveToJson():
    with open('py.json', 'w', encoding="utf-8") as f:
        json.dump(student_list, f, ensure_ascii=False)


# 读取数据
def readToJson():
    global student_list
    try:
        with open("py.json", 'r', encoding="utf-8") as load_f:
            student_list = json.load(load_f)
            if student_list == []:  #当学生列表为空的时候 传入固定的Nolist值进去 保证永远存在学生信息模板
                student_list = Nolist
    except:
        student_list = Nolist


Nolist = [{'student_ID': '1', 'student_name': '路飞', 'student_sex': '男', 'student_age': '15', 'student_room': '100'},
          {'student_ID': '2', 'student_name': '香吉', 'student_sex': '男', 'student_age': '22', 'student_room': '100'},
          {'student_ID': '3', 'student_name': '索隆', 'student_sex': '男', 'student_age': '23', 'student_room': '102'},
          {'student_ID': '4', 'student_name': '娜美', 'student_sex': '女', 'student_age': '21', 'student_room': '200'},
          {'student_ID': '5', 'student_name': '罗宾', 'student_sex': '女', 'student_age': '21', 'student_room': '201'},
          {'student_ID': '6', 'student_name': '汗可', 'student_sex': '女', 'student_age': '21', 'student_room': '201'}]

if __name__ == "__main__":
    readToJson()
    show_menu()
    saveToJson()
