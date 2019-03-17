#-*-coding:utf-8-*-
import re

class getoutfloop(Exception):pass

class car:
    def __init__(self,id,startid,endid,max_v,start_time,pass_c):
        self.id = id
        self.startid = startid
        self.endid = endid
        self.max_v = max_v#当前可行驶最大速度
        self.self_v = max_v#自身最大速度
        self.start_time = start_time#出发时间
        self.position = [-1,-1,-1,-1]#所在道路,车道，位置,前车（这里的前车是严格的，即前一个位置是否有车，有的话保存id）
        self.nextroad = -1#下一条路
        self.pass_cross = pass_c#所走路径，保存道路ID
        self.wait_status = True#等待状态，True为等待，False为终止
        self.move_status = 0#行驶状态：0为车库，1为道路直行，2为路口直行，3为路口左转，4为路口右转，-1表示到终点。状态数值对应car_status
        self.run_time = 0#运行时间

    def update_status(self,s1,next_p,single_cross,road_list,car_list,cross_list):
        #next_p是车在下一条路应该在的位置
        #先把道路原来的位置删了
        if(self.position[0]!=-1):
            origin_road = findbyid(self.position[0],road_list)
            if (origin_road.endid == single_cross.id):
                road_sit = origin_road.situation
            elif (origin_road.startid == single_cross.id):
                road_sit = origin_road.opposite_sit
            i,j = self.position[1],self.position[2]
            road_sit[i][j] = -1

            # 更新路口信息
            origin_index = single_cross.road_id.index(self.position[0])
            single_cross.road_sit[origin_index] -= 1

        #更新自身状态

        if(len(next_p)>0):
            #过路口更新位置
            this_road_id = next_p[0]#新路id
            this_road = findbyid(this_road_id, road_list)
            self.position = next_p
            frontcar_id = next_p[3]
            #更新可行驶的最大速度
            if(frontcar_id!=-1):
                frontcar = findbyid(frontcar_id,car_list)
                self.max_v = min(self.self_v,frontcar.max_v)
            else:
                self.max_v = min(self.max_v,this_road.max_v)
            if (this_road.endid == single_cross.id):
                road_sit = this_road.opposite_sit
            elif (this_road.startid == single_cross.id):
                road_sit = this_road.situation
            #过路口的话，应该检索的路口是下一个路口（对于更新路口信息而言）
            #this_cross_id = this_road.endid if this_road.startid == single_cross.id else this_road.startid
            #this_cross = findbyid(this_cross_id,cross_list)
        else:
            #道路直行更新位置
            self.position[2] -= s1
            #
            #this_cross = single_cross

        # 更新旧道路或新道路的车辆位置
        i,j = self.position[1],self.position[2]
        road_sit[i][j] = self.id

        #更新新路的路口车况
        #this_road_index = this_cross.road_id.index(self.position[0])
        #this_cross.road_sit[this_road_index] +=1

        #判断行驶状态并更新下一条路
        #这里的frontcar不同与上面的frontcar，处于不同道路
        s1,S1,frontcar_id = count_s1(self, road_sit)
        if(frontcar_id!=-1):
            frontcar = findbyid(frontcar_id,car_list)
        if(frontcar_id!=-1 and frontcar.move_status==1):
            self.move_status = 1
        else:
            if(S1>=self.max_v):
                self.move_status = 1
            else:
                road1 = self.position[0]
                if(self.pass_cross[-1] == road1):
                    #下一步到终点，则清除状态和位置信息
                    road2 = -1
                    self.move_status = -1
                    road_sit[i][j] = -1
                else:
                    # 找出下一个路口
                    if(self.move_status == 0):
                        #车库出来的车
                        real_road1 = findbyid(road1,road_list)
                        next_cross_id = real_road1.endid if real_road1.startid == single_cross.id else real_road1.startid
                        next_cross = findbyid(next_cross_id,cross_list)
                        road2 = self.pass_cross[self.pass_cross.index(road1) + 1]
                        road1_index = next_cross.road_id.index(road1)
                        road2_index = next_cross.road_id.index(road2)
                        self.move_status = next_cross.cross_status[road1_index][road2_index]
                        print("{}号车的位置".format(self.id), self.position, self.move_status, "S1", S1)
                    else:
                        road2 = self.pass_cross[self.pass_cross.index(road1)+1]
                        road1_index = single_cross.road_id.index(road1)
                        road2_index = single_cross.road_id.index(road2)
                        self.move_status = single_cross.cross_status[road1_index][road2_index]
                self.nextroad = road2

        #更新终止状态
        self.wait_status = False

    def straight_move(self,road_sit,single_cross,road_list,car_list,cross_list):
        #道路直行
        print("{}车直走".format(self.id))
        #调用这里默认就是可走状态（即等待状态）
        s1,S1,frontcar_id = count_s1(self,road_sit)
        if(frontcar_id!=-1 and s1 == 0):
            frontcar = findbyid(frontcar_id,car_list)
            self.max_v = min(self.max_v,frontcar.max_v)
        # 注意这里要改参数
        self.update_status(s1,[],single_cross,road_list,car_list,cross_list)

    def cross_move(self,road_sit,car_list,road_list,single_cross,cross_list):
        #路口行走，默认等待状态
        #如果顺利行走并设为终止状态返回True，如果前面堵塞而且等待则返回False
        if(len(road_sit)>0):
            s1,S1,frontcar_id = count_s1(self, road_sit)
            #既然可以过路口，则前面应该没车，s1与S1应该相等
        else:
            s1 = 0
            S1 = 0
            frontcar_id=-1
        if(frontcar_id==-1):
            next_road = findbyid(self.nextroad,road_list)
            v2 = min(next_road.max_v,self.self_v)
            s2 = v2-S1 if v2>S1 else 0
            #print("s2:",s2)
            #计算下一条路的空余空间和位置，下一条路最后的车
            i,j,frontcar_id = count_insertspace(s2,single_cross.id,self.nextroad,road_list,car_list)
            if(i!=-1):
                next_p = [self.nextroad,i,j,frontcar_id]
                self.update_status(S1,next_p,single_cross,road_list,car_list,cross_list)
            else:
                if(frontcar_id!=-1):
                    return False
                else:
                    if(len(road_sit)>0):
                        #这里是给非车库的走的
                        self.update_status(S1,[],single_cross,road_list,car_list,cross_list)
                    else:
                        #这里是车库走的
                        return False
        else:
            print("s1:",s1,"出错！！现在前方有车都给判断成出路口了？？？")
        return True

class road:
    def __init__(self,id,len,v,lane_num,startid,endid,doubleway):
        self.id = id
        self.max_v = v
        self.startid = startid#开始路口
        self.endid = endid#终止路口
        self.situation = [[-1]*len for i in range(lane_num)]#保存正向整条道路情况
        self.opposite_sit = []
        if(doubleway==1):
            self.opposite_sit = [[-1]*len for i in range(lane_num)]#保存反向整条道路的情况，即endid到startid的
        #print(self.situation)

    def findthefirstcar(self,cross_id):
        #返回第一辆车的id
        if (self.endid == cross_id):
            road_sit = self.situation
        elif (self.startid == cross_id):
            road_sit = self.opposite_sit
        for i in range(len(road_sit[0])):
            for j in range(len(road_sit)):
                if(road_sit[j][i]!=-1):
                    return road_sit[j][i]
        return -1

class cross:
    # 保存路口四个道路之间的转向关系（不可变），值范围是（-1,2，3，4）,-1为无状态，其余状态数值对应car_status,例如行数x是501道(id1)，列数y是502道(id2)，值为3,则501要进502道需要左转
    cross_status = ((-1, 3, 2, 4), (4, -1, 3, 2), (2, 4, -1, 3), (3, 2, 4, -1))
    def __init__(self,cross_id,id1=-1,id2=-1,id3=-1,id4=-1):
        self.id = cross_id;
        self.road_id = [id1,id2,id3,id4]#按原文件读取顺序保存路口所有道路ID，在这里获取索引再从cross_status读取转向关系
        self.garage = []#保存在路口车库等待的车辆，格式是[(车id,出发时间),(...),(...)]
        self.road_sit = [0]*4#按道路ID1,2,3,4保存对应道路还在等待状态的车辆数量

def get_alldata():
    #读取car.txt，road.txt，cross.txt三个文件的数据，按顺序返回(车，道，路口)保存三个txt数据的字典
    try:
        with open(r'H:\华为2019比赛\SDK\SDK_python\CodeCraft-2019\config\car.txt','r')as car_f:
            result1 = re.split('\D+',car_f.read())
            del result1[0]
            del result1[-1]
            car_dict = {}
            value = []
            for i,r_line in enumerate(result1):
                j = i%5
                if (j!=0):
                    value.append(int(result1[i]))
                else:
                    if len(value)>0:
                        car_dict[key] = value
                    key = int(result1[i])
                    value = []
            car_dict[key] = value
            #print(car_dict)
    except(IOError):
        print("读取car.txt出错")
        exit()
    try:
        with open(r'H:\华为2019比赛\SDK\SDK_python\CodeCraft-2019\config\road.txt','r')as road_f:
            result2 = re.split('\D+',road_f.read())
            del result2[0]
            del result2[-1]
            road_dict = {}
            value = []
            for i,r_line in enumerate(result2):
                j = i%7
                if (j!=0):
                    value.append(int(result2[i]))
                else:
                    if len(value)>0:
                        road_dict[key] = value
                    key = int(result2[i])
                    value = []
            road_dict[key] = value
            #print(road_dict)
    except(IOError):
        print("读取road.txt出错")
        exit()
    try:
        with open(r'H:\华为2019比赛\SDK\SDK_python\CodeCraft-2019\config\cross.txt','r')as cross_f:
            result3 = re.split('\D+',cross_f.read())
            del result3[0]
            del result3[-1]
            cross_dict = {}
            value = []
            for i,r_line in enumerate(result3):
                j = i%5
                if (j!=0):
                    s_v = int(result3[i])
                    value.append(-1 if s_v == 1 else s_v)
                else:
                    if len(value)>0:
                        cross_dict[key] = value
                    key = int(result3[i])
                    value = []
            cross_dict[key] = value
            #print(cross_dict)
    except(IOError):
        print("读取cross.txt出错")
        exit()
    return (car_dict,road_dict,cross_dict)

def create_carlist(car_dict,path_list):
    #创建模拟运行中所有车的列表
    car_list = []
    i = 0
    for car_id,car_ifo in car_dict.items():
        single_car = car(car_id,car_ifo[0],car_ifo[1],car_ifo[2],car_ifo[3],path_list[i])#这里加路径
        car_list.append(single_car)
        i += 1
    return car_list

def create_roadlist(road_dict):
    # 创建模拟运行中所有道路的列表
    road_list = []
    for road_id,road_ifo in road_dict.items():
        single_road = road(road_id,road_ifo[0],road_ifo[1],road_ifo[2],road_ifo[3],road_ifo[4],road_ifo[5])
        road_list.append(single_road)
    return road_list

def create_crosslist(cross_dict):
    # 创建模拟运行中所有路口的列表
    cross_list = []
    for cross_id,cross_ifo in cross_dict.items():
        single_cross = cross(cross_id,cross_ifo[0],cross_ifo[1],cross_ifo[2],cross_ifo[3])
        cross_list.append(single_cross)
    return cross_list

def findbyid(id,list):
    #根据ID找对象列表中的对象
    for item in list:
        if(id==item.id):
            return item
    return None

def inti_gerage(car_list,cross_list):
    #初始化各路口的车库
    for s_car in car_list:
        s_car.nextroad = s_car.pass_cross[0]
        if(s_car.move_status == 0):
            s_cross = findbyid(s_car.startid,cross_list)
            s_cross.garage.append((s_car.id,s_car.start_time))
        else:
            print("初始化车库失败：有车不是车库状态")
            break
        #s_car.move_status = 2
        s_cross.garage = sorted(s_cross.garage,key=lambda x:(x[1],x[0]))#先按车辆出发时间升序，如果相同则按车辆id升序
        #print(s_cross.id,s_cross.garage)

def showtheroad(road_sit):
    print("--------------")
    for i in range(len(road_sit)):
        print(road_sit[i])
    print("--------------")

def update_road_sit(single_cross,road_list):
    #这里假设前面都没问题，这时候的road_sit应该是[0,0,0,0]
    #走完一次时间之后计数存入cross中的road_sit中
    print("更新id为{}的路口等待车辆数量前的road_sit为：".format(single_cross.id),single_cross.road_sit)
    single_cross.road_sit = [0,0,0,0]
    for index,road_id in enumerate(single_cross.road_id):
        if(road_id!=-1):
            single_road = findbyid(road_id, road_list)
            if (single_road.endid == single_cross.id):
                road_sit = single_road.situation
            elif (single_road.startid == single_cross.id):
                road_sit = single_road.opposite_sit

            #print("{}号路口的{}路车况".format(single_cross.id,road_id))
            #showtheroad(single_road.situation)
            #showtheroad(single_road.opposite_sit)

            for i in range(len(road_sit[0])):
                for j in range(len(road_sit)):
                    if (road_sit[j][i] != -1):
                        single_cross.road_sit[index] +=1

def count_insertspace(s2,cross_id,road_id,road_list,car_list):
    #计算该路可插入的位置，返回应该插入的车道和位置
    single_road = findbyid(road_id, road_list)
    if (single_road.endid == cross_id):
        road_sit = single_road.opposite_sit
    elif (single_road.startid == cross_id):
        road_sit = single_road.situation
    last = len(road_sit[0]) - 1
    for i in range(len(road_sit)):
        for j in range(last,-1,-1):
            if(road_sit[i][j]!=-1):
               if(j==last):
                   #车道最后一个位置有车
                   break
               else:
                   #在s2内有车，如果是等待状态则跳过，如果是终止状态则可以走
                   frontcar_id = road_sit[i][j]
                   frontcar = findbyid(frontcar_id,car_list)
                   if(frontcar.wait_status == True):
                       return (-1,-1,road_sit[i][j])
                   else:
                       return(i,j+1,road_sit[i][j])
            elif((last-j)>=s2):
                #在s2外有车
                if(s2==0):
                    return (-1,-1,-1)
                else:
                    return (i, last - s2 + 1,-1)
    return (-1,-1,-1)


def count_s1(s_car,road_sit):
    #返回车辆在当前道路的与前车距离s1，可行驶距离S1，和前车的id（-1表示没车），这里的前车是不严格的，即该车路上只要在本车前面的第一个都算
    #默认road_sit矩阵索引0是靠近驶出的路口方向
    last_car = 0
    ishavecar = -1
    #print("{}号车的位置".format(s_car.id),s_car.position)
    for line in road_sit:
        if (s_car.id in line):
            for i in range(len(line)):
                if(line[i]!=-1 and line[i]!=s_car.id):
                    last_car = i
                    ishavecar = line[i]
                if(line[i]==s_car.id):
                    if(i==0):
                        return (0,0,-1)
                    s1 = i-last_car-1 if ishavecar!=-1 else i
                    return (s1,i,ishavecar)
    print("求不了S1，路上根本没有这辆车" + s_car.id)

def iswaittingcar(cross_list):
    #判断所有路口所有道路是不是还有等待的车，有的话返回True
    for single_cross in cross_list:
        if(sum(single_cross.road_sit)>0):
            return True
    return False

def check_road(road_activenum,road_index,road_list,single_cross,car_list,cross_list):
    #检查道路上的车，返回值如果是-1，证明前方堵塞，不能通行，路上车辆照样是等待状态。
    #返回值是road_index本身，证明道路上全部遍历，车辆照常走完。返回值如果是其他，则跳转到优先级高的其他路，但是本道路还有可行的权力
    road_id = single_cross.road_id[road_index]
    if(road_id!=-1):
        single_road = findbyid(road_id, road_list)
        if (single_road.endid == single_cross.id):
            road_sit = single_road.situation
        elif (single_road.startid == single_cross.id):
            road_sit = single_road.opposite_sit
        print("{}号路口的{}路车况".format(single_cross.id,road_id))
        showtheroad(road_sit)
        #if (len(road_sit) > 0):
        for i in range(len(road_sit[0])):
            for j in range(len(road_sit)):
                if (road_sit[j][i] != -1):
                    car_id = road_sit[j][i]
                    print("处理{}号车".format(car_id))
                    single_car = findbyid(car_id, car_list)
                    print(single_car.wait_status,single_car.move_status)
                    if (single_car.wait_status != True):
                        # 碰到车辆是终止状态，跳出
                        road_activenum[road_index] -= 1
                        return road_index
                    else:
                        if (single_car.move_status == 1):
                            # 道路直行
                            single_car.straight_move(road_sit,single_cross,road_list,car_list,cross_list)
                        elif (single_car.move_status == 2):
                            # 路口直行
                            print("在{}路直行到下一路口".format(road_id))
                            if (single_car.cross_move(road_sit,car_list,road_list,single_cross,cross_list) == False):
                                # 如果因下路口堵塞而继续等待，则直接跳出（这种就直接不用管，让下一个路口先走）
                                print("堵塞！！！先不走")
                                road_activenum[road_index] -= 1
                                return -1
                        elif (single_car.move_status == 3):
                            # 路口左转，则先判断旁路有没有直行
                            s_road_id = single_cross.road_id[(road_index + 3) % 4]
                            if(s_road_id!=-1):
                                s_road = findbyid(s_road_id, road_list)
                                s_car_id = s_road.findthefirstcar(single_cross.id)
                                if(s_car_id!=-1):
                                    s_car = findbyid(s_car_id, car_list)
                                    if (s_car.move_status == 2 and s_car.wait_status == True):
                                        # 跳出，直接读下一条路
                                        print("等待直行车辆")
                                        return (road_index + 3) % 4
                            print("在{}路左转到下一路口".format(road_id))
                            if (single_car.cross_move(road_sit,car_list,road_list,single_cross,cross_list) == False):
                                # 如果因下路口堵塞而继续等待，则直接跳出
                                print("堵塞！！！先不走")
                                road_activenum[road_index] -= 1
                                return -1
                        elif (single_car.move_status == 4):
                            # 路口右转，先判断旁路直行，对路左转
                            s_road_id = single_cross.road_id[(road_index + 1) % 4]
                            if(s_road_id!=-1):
                                s_road = findbyid(s_road_id, road_list)
                                s_car_id = s_road.findthefirstcar(single_cross.id)
                                if (s_car_id != -1):
                                    s_car = findbyid(s_car_id, car_list)
                                    if (s_car.move_status == 2 and s_car.wait_status == True):
                                        # 跳出，直接读下一条路
                                        road_id = s_road_id
                                        print("等待直行车辆")
                                        return (road_index + 1) % 4
                            #判断对路左转
                            l_road_id = single_cross.road_id[(road_index + 2) % 4]
                            if(l_road_id!=-1):
                                l_road = findbyid(l_road_id, road_list)
                                l_car_id = l_road.findthefirstcar(single_cross.id)
                                if (l_car_id != -1):
                                    l_car = findbyid(l_car_id, car_list)
                                    if (l_car.move_status == 3 and l_car.wait_status == True):
                                        # 跳出，直接读下一条路
                                        road_id = l_road_id
                                        print("等待左转车辆")
                                        return (road_index + 2) % 4

                            print("在{}路右转到下一路口".format(road_id))
                            if (single_car.cross_move(road_sit,car_list,road_list,single_cross,cross_list) == False):
                                # 如果因下路口堵塞而继续等待，则直接跳出
                                print("堵塞！！！先不走")
                                road_activenum[road_index] -= 1
                                return -1
        # 正经全部跑完的读下一条路
        road_activenum[road_index] -= 1
        return road_index
    else:
        print("road_activatenum存储出错，id为-1的道路都可行？")
        return road_index

def check_cross(single_cross,road_list,car_list,cross_list):
    #遍历当前路口的所有道路
    print("路口车况：",single_cross.road_sit)
    road_index = 0#这个是cross的road_id里的索引，与road_id不同
    road_activenum = [0,0,0,0]#有多少个道路可行
    for i,value in enumerate(single_cross.road_sit):
        if(value!=0):
            road_activenum[i] = 1
    while(sum(road_activenum)>0):
        if(road_activenum[road_index]>0):
            wait_record = []
            next_index = check_road(road_activenum,road_index,road_list,single_cross,car_list,cross_list)
            while(next_index!=-1 and next_index!=road_index):
                #这里为了追踪优先级高的路，如果它们都堵塞，则优先级低的路直接就不能走了，遍历剩下的路然后跳到下一个路口
                wait_record.append(road_index)
                road_index=next_index
                next_index = check_road(road_activenum, road_index,road_list,single_cross,car_list,cross_list)
            if(next_index == -1 and len(wait_record)>0):
                for i in wait_record:
                    road_activenum[i] = 0
        road_index = (road_index+1)%4

def simulation_run(car_dict,road_dict,cross_dict,path_list):
    #模拟运行
    system_time =0
    limit_time = 99999999
    car_list = create_carlist(car_dict,path_list)
    road_list = create_roadlist(road_dict)
    cross_list = create_crosslist(cross_dict)

    #初始第一步
    inti_gerage(car_list,cross_list)

    #循环迭代
    while True:
        if(system_time<limit_time):
            while(iswaittingcar(cross_list)):
                print("路上的车走-------")
                # 只要还有等待的车，就从路口1开始遍历
                for single_cross in cross_list:
                    print("检查{}路口".format(single_cross.id))
                    check_cross(single_cross,road_list,car_list,cross_list)

            #还要处理车库里的车
            print("车库的车走-------------------")
            for single_cross in cross_list:
                while(len(single_cross.garage)>0):
                    car_id,start_time = single_cross.garage[0][0],single_cross.garage[0][1]
                    #print("要走的车：",car_id,"出发时间:",start_time)
                    single_car = findbyid(car_id,car_list)
                    cango = single_car.cross_move([],car_list,road_list,single_cross,cross_list)
                    if(cango ==True):
                        single_car.run_time = system_time
                        del single_cross.garage[0]
                    else:
                        #发现一辆车不走，直接跳下一个路口
                        break
            for single_cross in cross_list:
                update_road_sit(single_cross,road_list)
            #走完一次时间之后将所有车辆设为等待状态
            for single_car in car_list:
                if(single_car.move_status!=-1):
                    print("全部设为等待状态!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    single_car.wait_status = True
                else:
                    single_car.run_time = system_time - single_car.run_time
                    print("{}号车到达终点，用时:{}".format(single_car.id,single_car.run_time))
            system_time += 1

        else:
            # 超过限定时间，跳出，该路径规划取消
            break

def make_pass_list(road_dict,cross_dict):
    try:
        with open(r'H:\华为2019比赛\测试数据\测试路径1\path.txt', 'r')as f:
            path_list = []
            for line in f:
                one_path = []
                path = re.split('\D+',line)
                del path[-1]
                for p in path:
                    one_path.append(int(p))
                path_list.append(one_path)

            return path_list
    except(IOError):
        print("读路径出错")
        exit()

if __name__ == "__main__":

    car_status = ("Garage_status","road_straight","cross_straight","cross_left","cross_right")#行驶状态：0为车库，1为道路直行，2为路口直行，3为路口左转，4为路口右转
    car_dict,road_dict,cross_dict = get_alldata()#保存原始从文件读取的数据：车辆，道路，路口
    print(car_dict)
    print(road_dict)
    print(cross_dict)
    path_list = make_pass_list(road_dict,cross_dict)
    print("path_list:",path_list)

    simulation_run(car_dict,road_dict,cross_dict,path_list)