import Widget.car
import Widget.cross
import Widget.road


def MapInit(carData, crossData, roadData, carRoute):

    # 创建车辆实例
    carList = []
    for carNum in range(len(carData)):
        carInstance = Widget.car.Car(carData[carNum][0], carData[carNum][1], carData[carNum][2], carData[carNum][3], carData[carNum][4],
                          0, carRoute[carNum], 1)
        carList.append(carInstance)

    # 创建道路实例
    roadList = []
    roadIndexDict = {}
    for roadNum in range(len(roadData)):

        roadInstance = Widget.road.Road(roadData[roadNum][0], roadData[roadNum][1], roadData[roadNum][2], roadData[roadNum][3],
                                        roadData[roadNum][4], roadData[roadNum][5], roadData[roadNum][6])
        roadIndexDict.update({roadInstance.roadId : roadInstance})
        laneMatrixPositive = []
        laneMatrixNegative = []
        for row in range(roadInstance.roadChannel):
            laneMatrixPositiveTmp = []
            for column in range(roadInstance.roadLength):
                laneMatrixPositiveTmp.append(0)
            laneMatrixPositive.append(laneMatrixPositiveTmp)
        roadInstance.laneMatrixPositive = laneMatrixPositive
        if (roadInstance.roadisDuplex == 1):
            for row in range(roadInstance.roadChannel):
                laneMatrixNegativeTmp = []
                for column in range(roadInstance.roadLength):
                    laneMatrixNegativeTmp.append(0)
                laneMatrixNegative.append(laneMatrixNegativeTmp)
            roadInstance.laneMatrixNegative = laneMatrixNegative

        roadList.append(roadInstance)
    roadIndexDict.update({-1 : None})

    # 创建路口实例
    crossList = []
    for crossNum in range(len(crossData)):


        road1Id = roadIndexDict[crossData[crossNum][1]].roadId if roadIndexDict[crossData[crossNum][1]] != None else -1
        road2Id = roadIndexDict[crossData[crossNum][2]].roadId if roadIndexDict[crossData[crossNum][2]] != None else -1
        road3Id = roadIndexDict[crossData[crossNum][3]].roadId if roadIndexDict[crossData[crossNum][3]] != None else -1
        road4Id = roadIndexDict[crossData[crossNum][4]].roadId if roadIndexDict[crossData[crossNum][4]] != None else -1


        # 记录转弯优先级
        PriorDirectionDict = {road1Id : {road3Id : 3, road2Id : 2, road4Id : 1},
                         road2Id : {road4Id : 3, road3Id : 2, road1Id : 1},
                         road3Id : {road1Id : 3, road4Id : 2, road2Id : 1},
                         road4Id : {road2Id : 3, road1Id : 2, road3Id : 1}}

        crossInstance = Widget.cross.Cross(crossData[crossNum][0], roadIndexDict[crossData[crossNum][1]], roadIndexDict[crossData[crossNum][2]],
                                           roadIndexDict[crossData[crossNum][3]], roadIndexDict[crossData[crossNum][4]], PriorDirectionDict)
        crossList.append(crossInstance)

    return carList, roadList, crossList

