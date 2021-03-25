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

rm_dict = {}

stu_list = []

# 新增学生函数
def new_student():
    global stu_list
    print("*" * 50)
    print('新增学生')
    ID_studnet_list = []
    for stu in stu_list:
        ID_studnet_list.append(stu['stu_ID'])
    while True:
        try:
            stu_ID = int(input('请输入学生学号'))
            if str(stu_ID) not in ID_studnet_list and stu_ID != 0:
                break
            else:
                print('您输入的学号已存在')
        except ValueError:
            print('您输入的学号有误请重新输入')
    stu_name = input('请输入姓名')
    while True:
        stu_sex = input('请输入性别')
        if stu_sex in ('男', '女'):
            break
        print('您输入的性别有误，请重新输入')
    while True:
        try:
            stu_age = int(input('请输入年龄'))
            break
        except ValueError:
                print('您输入的年龄有误，请重新输入')
    while True:
        if str(len(stu_list)) == '24':
            print('寝室人员已满，无法再住进学校')
            return
        else:
            break
    while True:
        to_room = input('输入0，自动分配寝室号:\n输入1,手动分配寝室号:')
        if to_room == '0':
            stu_room = automatic_room(stu_sex)  #调用自动分配函数  返回值为房间号
            break
        elif to_room == '1':
            stu_room = hand_dormitory(stu_sex)  #调用手动分配函数 返回值为房间号
            break

        else:
            print('输入有误请重新输入')
    stu = {'stu_ID': str(stu_ID), 'stu_name': stu_name, 'stu_sex': stu_sex, 'stu_age': stu_age, 'stu_room': stu_room}
    stu_list.append(stu)
    saveToJson()
    print('添加%s的信息成功' % stu_name)


# 寝室的自动分配的函数
def automatic_room(student_sex):
    k = 1 if student_sex == "男" else 2
    while True:
        key = str(random.randint(100 * k, 100 * k + 2))  # 保存模板{key(房间号):count(房间人数)}
        count = rm_dict.setdefault(key, 0)
        if count < 4:
            rm_dict[key] += 1
            break
    return key

# 显示所有学生信息的函数
def show_all_student():
    print("-" * 50)
    print("显示所有学生信息")
    print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
    print("=" * 50)
    for student in stu_list:
        print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
        student['stu_ID'], student['stu_name'], student['stu_sex'], student['stu_age'], student['stu_room']))


# 搜索学号的函数
def search_student():
    print("======================我是可爱的分割线========================")
    print("[搜索学生信息]\n")
    while True:
        find_id = input("请你输入想要查找的学号:")
        print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
        for student in stu_list:  # 打印输出这个字典的值
            if find_id in student['stu_ID']:
                print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
                student['stu_ID'], student['stu_name'], student['stu_sex'], student['stu_age'], student['stu_room']))
                return
        print('你想查找的学号不存在')


# 显示寝室的函数
def show_room():
    print("寝室人员列表")
    id_list = []
    while True:
        find_room = input('您想要查找的寝室号是:')
        print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
        for student in stu_list:  # 打印输出这个字典的值
            if find_room == student['stu_room']:
                id_list.append(student)
        if id_list:
            for stu in id_list:
                print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
                stu['stu_ID'], stu['stu_name'], stu['stu_sex'], stu['stu_age'], stu['stu_room']))
            return
        else:
            print('您输入的寝室号有误请重新输入')


# 删除学生信息函数
def delete_student():
    print("删除学生信息界面")
    delete_ID = input('请输入您想删除的学生号是')
    for student in stu_list:
        if delete_ID in student['stu_ID']:
            index = stu_list.index(student)
            stu_list.pop(index)
            saveToJson()
            print('%s号学生已经被删除' % student['stu_ID'])
            return
    print('你输入的学号不存在')


# 手动分配寝室函数
def hand_dormitory(student_sex):
    print('手动分配寝室')
    k = 1 if student_sex == '男' else 2
    while True:
        room_choice = input('请输入您想选择的寝室号')
        if room_choice in [str(x) for x in range(k*100,k*100+3)]:
            count = rm_dict.setdefault(room_choice, 0)
            print(room_choice)
            if count < 4:
                rm_dict[room_choice] += 1
                break
            print('该寝室已满')
        else:
            print('您输入的寝室不存在')
    return room_choice

# 双方交换寝室函数
def change_room():
    print('学生寝室交换界面')
    while True:
        ID_frist = input('请输入你的学号')
        ID_second = input('请输入交换对方的学号')
        ID_list = []  # 存放交换双方的空列表
        for stduent_dict in stu_list:
            if stduent_dict['stu_ID']==ID_frist:
                ID_list.append(stduent_dict)   #存放第一个学生的信息去ID_list[]
            elif stduent_dict['stu_ID']==ID_second:
                ID_list.append(stduent_dict)   #存放第二个学生的信息去ID_list[]
        try:
            if ID_list[0]['stu_sex']==ID_list[1]['stu_sex']:
                ID_list[0]['stu_room'],ID_list[1]['stu_room']=ID_list[1]['stu_room'],ID_list[0]['stu_room']  #交换寝室号码
                saveToJson()
                print('%s同学现在的寝室为%s' % (ID_list[0]['stu_name'], ID_list[0]['stu_room']))
                return
            else:
                print('男女性别有误')
        except IndexError:
            print('学号或性别有误,请换间寝室')


#单方面选择寝室
def choice_room():
    print('学生调整到其他寝室界面')
    while True:
        ID = input('请输入您的学号')
        find_student = []
        for student in stu_list:
            if ID == student['stu_ID']:
                find_student.append(student) #第一个是学生ID
        try:
            if ID == find_student[0]['stu_ID']:
                sex = find_student[0]['stu_sex']
                break
        except IndexError:
                print('您输入的学号有误')
    k = 1 if sex == '男' else 2
    while True:
        room_choice = input('请输入您想选择的寝室号')
        if room_choice in [str(x) for x in range(k*100,k*100+3)]:
            count = rm_dict.setdefault(room_choice, 0)
            if count < 4:
                find_student[0]['stu_room'] = room_choice
                rm_dict[room_choice] += 1
                print('%s现在的寝室号为%s'%(find_student[0]['stu_name'],find_student[0]['stu_room']))
                saveToJson()
                break
            print('该寝室已满')
        else:
            print('您输入的寝室号不正确，请重新输入')


#原列表里的房间号和人数
def reset_rm_dict():
    for i in range(len(stu_list)):
        if stu_list[i]['stu_room'] not in rm_dict:
            rm_dict[stu_list[i]['stu_room']] = 0
        count = rm_dict[stu_list[i]['stu_room']]
        if count < 4:
            rm_dict[stu_list[i]['stu_room']] += 1
            i += 1
        elif count==4:
            print('%s这位学生的寝室号%s重复，请修改'%(stu_list[i]['stu_name'],stu_list[i]['stu_room']))
            break
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
        print("5.交换寝室调整")
        print("6.删除学生信息")
        print('7.选择寝室调整')
        print("0.退出管理系统")
        print("*" * 50)
        readToJson() #读取数据
        choice = input("请输入你想进行的操作是:")
        if choice == '1': #录入学生信息
            if new_student():
                print("按enter键继续：")
                input()
                continue
        elif choice == '2':#显示学生信息
            show_all_student()
            print("按enter键继续：")
            input()
            continue
        elif choice == '3':#搜索学生信息
            search_student()
            print("按enter键继续：")
            input()
            continue
        elif choice == '4': #显示寝室人员列表
            show_room()
            print("按enter键继续：")
            input()
            continue
        elif choice == '5':
            change_room()  #寝室人员交换调整
            print("按enter键继续：")
            input()
            continue
        elif choice == '6': #删除学生信息
            delete_student()
            print("按enter键继续：")
            input()
            continue
        elif choice == '7':  #单向选择寝室调整
            choice_room()
            print("按enter键继续：")
            input()
            continue
        elif choice == '0':  #保存退出学生管理系统
            print("欢迎再次使用学生管理系统！")
            saveToJson()
            break
        else:
            print("请您输入操作相对应的数字：")


# 保存数据
def saveToJson():
    with open('py.json', 'w', encoding="utf-8") as f:
        json.dump(stu_list, f, ensure_ascii=False)


# 读取数据
def readToJson():
    global stu_list
    try:
        with open("py.json", 'r', encoding="utf-8") as load_f:
            stu_list = json.load(load_f)
            if stu_list == []:  #当学生列表为空的时候 传入固定的Nolist值进去 保证永远存在学生信息模板
                stu_list = Nolist
    except:
        stu_list = Nolist


Nolist = [{'stu_ID': '1', 'stu_name': '路飞', 'stu_sex': '男', 'stu_age': '15', 'stu_room': '100'},
          {'stu_ID': '2', 'stu_name': '香吉', 'stu_sex': '男', 'stu_age': '22', 'stu_room': '100'},
          {'stu_ID': '3', 'stu_name': '索隆', 'stu_sex': '男', 'stu_age': '23', 'stu_room': '102'},
          {'stu_ID': '4', 'stu_name': '娜美', 'stu_sex': '女', 'stu_age': '21', 'stu_room': '200'},
          {'stu_ID': '5', 'stu_name': '罗宾', 'stu_sex': '女', 'stu_age': '21', 'stu_room': '201'},
          {'stu_ID': '6', 'stu_name': '汗可', 'stu_sex': '女', 'stu_age': '21', 'stu_room': '201'}]




if __name__ == "__main__":
    readToJson()
    reset_rm_dict()
    show_menu()
    saveToJson()
