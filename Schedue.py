






def MapScheduling(carList, roadList, crossList):
    AllCarInDestination = False
    AllCarInStatusEnd = False
    AllCarInStatusEndInSingleCross = False
    SchedulTime = 1

    while AllCarInDestination != True: # 全部车都到达目的地


        while AllCarInStatusEnd != True: # 一轮所有车都是终止状态

            for crossNum in range(len(crossList)):

                # 检查road1
                road1 = crossList[crossNum].crossRoad1
                road_1_Start = road1.roadOrigin if road1 != None else -1
                road_1_End = road1.roadDestination if road1 != None else -1
                CarStartInThisRoad = [] # 找要出库的车

                if road_1_Start != -1: # 这条道路存在，则开始调度

                    for roadLen in range(road1.roadLength):
                        for roadChan in range(road1.roadChannel):
                            if road_1_End - road_1_Start > 0: # 调度正向车道
                               if road1.laneMatrixPositive[road1.roadChannel - roadChan - 1][road1.roadLength - roadLen - 1] != 0:
                                    car = road1.laneMatrixPositive[road1.roadLength - roadLen - 1][roadChan]
                                    if min(car.carSpeed, road1.roadSpeed) - (road1.roadLength - roadLen - 1) > 0:
                                        print("可以出道路")
                                        nextRoadId = car.path[1]

                                    else:
                                        road1.laneMatrixPositive[min(car.carSpeed, road1.speed) + roadLen][roadChan] = car
                                        road1.laneMatrixPositive[road1.roadLength - roadLen - 1][roadChan] = 0
                                        car.waitOrStop = False
                            else:  # 反向车道
                                if road1.laneMatrixNegative[road1.roadLength - roadLen - 1][road1.roadChannel - roadChan - 1] != 0:
                                    car = road1.laneMatrixPositive[road1.roadLength - roadLen - 1][roadChan]
                                    if min(car.carSpeed, road1.roadSpeed) - (road1.roadLength - roadLen - 1) > 0:
                                        print("可以出道路")
                                    else:
                                        road1.laneMatrixPositive[min(car.carSpeed, road1.speed) + roadLen][
                                            roadChan] = car
                                        road1.laneMatrixPositive[road1.roadLength - roadLen - 1][roadChan] = 0
                                        car.waitOrStop = False

                    for carNum in range(len(carList)): # 找出需要出库的车
                        if carList[carNum].carOriginal == road_1_Start and carList[carNum].isInGarage == 0:
                            CarStartInThisRoad.append(carList[carNum])



                    for CarStartInThisRoadInstance in CarStartInThisRoad:
                        for roadLen in range(road1.roadLength):
                            if road_1_End - road_1_Start > 0:  # 调度正向车道:
                                for roadChan in range(road1.roadChannel):  # 出库调度
                                    if road1.laneMatrixPositive[roadChan][roadLen] == 0: # 如果该位置是空，判断长度
                                        if min(CarStartInThisRoadInstance.carSpeed, road1.roadSpeed) - 1 < roadLen and CarStartInThisRoadInstance.carStartTime <= SchedulTime:
                                            road1.laneMatrixPositive[roadChan][roadLen] = CarStartInThisRoadInstance
                                            CarStartInThisRoadInstance.isInGarage = 1 # 在车库状态更改
                                            CarStartInThisRoadInstance.WaitorStop = 0 # 设置为终止状态
                                            CarStartInThisRoad.remove(CarStartInThisRoadInstance)
                                            break # 该位置被占用，退出该位置的遍历，重新寻找其他位置

                                        else:
                                            continue
                                    else: # 如果该位置有车，不用判断了，直接跳出这行车道的搜索
                                        # if min(CarStartInThisRoad[0].speed, road1.speed) - 1 < roadLen:
                                        break
                    print("road1出库调度完成")

                    # 开始从道路终点往起点遍历
                else: #road1检查完成
                    print("不存在road1")
                    break


                print("debug")


