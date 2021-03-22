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


global student_list

roomdict = {}

student_list=[]


# 新增学生函数
def new_student():
    global student_list
    print("*" * 50)
    print('新增学生')
    flag = 1
    while flag:
        ID_studnet_list = []
        ID_str = input('请输入学生学号')
        for card_dict in student_list:
            ID_studnet_list.append(card_dict['ID_str'])
        if ID_str.isnumeric()==True and ID_str in ID_studnet_list :
            print('你输入的学号已经存在')
            flag = 1
        else:
            flag = 0
    name_str = input('请输入姓名')
    while True:
        sex_str = input('请输入性别')
        if sex_str in ('男', '女'):
            break
        else:
            print('您输入的性别有误，请重新输入')
            continue
    while True:
        age_str = input('请输入年龄')
        if age_str.isnumeric():
            break
        else:
            print('您输入的年龄有误，请重新输入')
            continue
    while True:
        to_room = input('输入0，自动分配寝室号:\n输入1,手动分配寝室号:')
        if to_room in ('0'):
            room_str = automatic_room(sex_str)  #调用自动分配函数  返回值为房间号
            break
        elif to_room in ('1'):
            room_str = hand_allot_room()  #调用手动分配函数 返回值为房间号
            break
        else:
            print('输入有误请重新输入')
            continue
    card_dict = {'ID_str': ID_str, 'name_str': name_str, 'sex_str': sex_str, 'age_str': age_str, 'room_str': room_str}
    student_list.append(card_dict)
    print('添加%s的信息成功' % name_str)


# 寝室的自动分配的函数
def automatic_room(sex_str):
    flag = 1
    while flag:
        if sex_str == '男':
            key = str(random.randint(100, 102))#保存模板{key(房间号):count(房间人数)}
            count = roomdict.setdefault(key, 0)
            if count < 4:
                roomdict[key] += 1
                flag = 0
        else:
            key = str(random.randint(200, 202))
            count = roomdict.setdefault(key, 0)
            if count < 4:
                roomdict[key] += 1
                flag = 0
        return key #返回房间号被录入信息时调用


# 显示所有学生信息的函数
def show_all_student():
    print("-" * 50)
    print("显示所有学生信息")
    print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
    print("=" * 50)
    for card_dict in student_list:
        print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
        card_dict['ID_str'], card_dict['name_str'], card_dict['sex_str'], card_dict['age_str'], card_dict['room_str']))


# 搜索学号的函数
def search_card():
    print("======================我是可爱的分割线========================")
    print("[搜索学生信息]\n")
    find_id = input("请你输入想要查找的学号:")
    for card_dict in student_list:  # 打印输出这个字典的值
        if find_id in card_dict['ID_str']:
            print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
            card_dict['ID_str'], card_dict['name_str'], card_dict['sex_str'], card_dict['age_str'],
            card_dict['room_str']))
        else:
            print('你想查找的学号不存在')
            break


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
            for card_dict in student_list:  # 打印输出这个字典的值
                if find_room == card_dict['room_str']:
                    print("%s\t\t%s\t\t%s\t\t%s\t\t%s" % (card_dict['ID_str'], card_dict['name_str'], card_dict['sex_str'], card_dict['age_str'],card_dict['room_str']))
        else:
            return
    else:
        print('您输入的操作有误,请重新输入:')
        return


# 删除学生信息函数
def delete():
    print("删除学生信息界面")
    delete_ID = input('请输入您想删除的学生号是')
    for card_dict in student_list:
        if delete_ID in card_dict['ID_str']:
            print('%s号学生已经被删除' % card_dict['ID_str'])
            index = student_list.index(card_dict)
            student_list.pop(index)
            break
        else:
            print('您输入的学号有误')
            break


# 手动分配寝室函数
def hand_allot_room():
    print('学生寝室手动交换界面')
    room_choice = input('请输入您想选择的寝室号')
    room_sex = input('请输入您的性别')
    if room_choice in ('100','101','102') and room_sex == '男':
        if room_choice == '100':
            count = roomdict.setdefault('100', 0)
            if count < 4:
                roomdict['100'] += 1
                return '100'
            else:
                print('这间寝室已满，请重新选择寝室')
        elif room_choice == '101':
                count = roomdict.setdefault('101', 0)
                if count < 4:
                    roomdict['101'] += 1
                    return '101'
                else:
                    print('这间寝室已满，请重新选择寝室')
        elif room_choice == '102':
                count = roomdict.setdefault('102', 0)
                if count < 4:
                    roomdict['102'] += 1
                    return '102'
                else:
                    print('这间寝室已满，请重新选择寝室')
    elif room_choice in ('200', '201', '202') and room_sex == '女':
        if room_choice == '200':
            count = roomdict.setdefault('200', 0)
            if count < 4:
                roomdict['200'] += 1
                return '200'
            else:
                print('这间寝室已满，请重新选择寝室')
        elif room_choice == '201':
                count = roomdict.setdefault('201', 0)
                if count < 4:
                    roomdict['201'] += 1
                    return '201'
                else:
                    print('这间寝室已满，请重新选择寝室')
        elif room_choice == '202':
                count = roomdict.setdefault('202', 0)
                if count < 4:
                    roomdict['202'] += 1
                    return '202'
                else:
                    print('这间寝室已满，请重新选择寝室')
    else:
        print('您输入的寝室号或性别有误，请重新输入')


# 双方交换寝室函数
def change_room():
    print('学生寝室交换界面')
    ID_frist = input('请输入你的学号')
    ID_second = input('请输入交换对方的学号')
    ID_list = [] #存放交换双方的空列表
    for card_dict in student_list:
        if card_dict['ID_str']==ID_frist:
            ID_list.append(card_dict)   #存放第一个学生的信息去ID_list[]
        elif card_dict['ID_str']==ID_second:
            ID_list.append(card_dict)   #存放第二个学生的信息去ID_list[]
    if ID_list[0]['sex_str']==ID_list[1]['sex_str']:
        ID_list[0]['room_str'],ID_list[1]['room_str']=ID_list[1]['room_str'],ID_list[0]['room_str']  #交换寝室号码
    else:
        print('男女有别,请换间寝室')


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
            search_card()
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
            delete()
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


Nolist = [{'ID_str': '1', 'name_str': '路飞', 'sex_str': '男', 'age_str': '15', 'room_str': '100'},
          {'ID_str': '2', 'name_str': '香吉', 'sex_str': '男', 'age_str': '22', 'room_str': '100'},
          {'ID_str': '3', 'name_str': '索隆', 'sex_str': '男', 'age_str': '23', 'room_str': '102'},
          {'ID_str': '4', 'name_str': '娜美', 'sex_str': '女', 'age_str': '21', 'room_str': '200'},
          {'ID_str': '5', 'name_str': '罗宾', 'sex_str': '女', 'age_str': '21', 'room_str': '201'},
          {'ID_str': '6', 'name_str': '汗可', 'sex_str': '女', 'age_str': '21', 'room_str': '201'}]

if __name__ == "__main__":
    readToJson()
    show_menu()
    saveToJson()
