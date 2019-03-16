import random
import math
tasks = [] # 任务数组，数组的下标表示任务的编号，数组的值表示任务的长度。比如：tasks[0]=10表示第一个任务的任务长度是10.
taskNum = 100

nodes = [] # 处理节点的数组。数组的下标表示处理节点的编号，数组值表示节点的处理速度。比如：nodes[0]=10表示第1个处理节点的处理速度为10.
nodeNum = 10

iteratorNum = 1000
antNum = 100

timeMatrix = [] # 它是一个二维矩阵。比如：timeMatrix[i][j]就表示第i个任务分配给第j个节点所需的处理时间。

pheromoneMatrix = []
maxPheromoneMatrix = []
criticalPointMatrix = []

randomCount = 0

p = 0.5
q = 2


def init():
    for i in range(taskNum):
        tasks.append(random.randint(10, 100))
        maxPheromoneMatrix.append(random.randint(0, 9))
        criticalPointMatrix.append(random.randint(0, 9))
    for i in range(nodeNum):
        nodes.append(random.randint(10, 100))


def initMatrix(taskNum, nodeNum, defaultVal):
    matrix = []
    for i in range(taskNum):
        matrix_i = []
        for j in range(nodeNum):
            matrix_i.append(defaultVal)
        matrix.append(matrix_i)
    return matrix

def assignOnetask(antCount, taskCount, nodes, pheromoneMatrix):
    if (antCount <= criticalPointMatrix[taskCount]):
        return maxPheromoneMatrix[taskCount]
    else:
        return random.randint(0, nodeNum - 1)


def calTime_oneIt(pathMatrix_allAnt):
    time_allAnt = []
    for antIndex in range(antNum): # 计算每个蚂蚁所调度的节点处理任务的时间总和
        pathMatrix = pathMatrix_allAnt[antIndex]
        maxTime = -1
        for nodeIndex in range(nodeNum): # 计算所有节点要处理的任务的时间总和
            time = 0
            for taskIndex in range(taskNum): # 计算一个节点要处理的任务的时间总和
                if (pathMatrix[taskIndex][nodeIndex] == 1):
                    time += timeMatrix[taskIndex][nodeIndex]
            if time > maxTime:
                maxTime = time
        time_allAnt.append(maxTime)
    return time_allAnt

def updatePheromoneMatrix(pathMatrix_allAnt, pheromoneMatrix, timeArray_oneIt):
    for i in range(taskNum):
        for j in range(nodeNum):
            pheromoneMatrix[i][j] *= p # 信息素减少
    minTime = timeArray_oneIt[0]
    minIndex = 0
    for antIndex in range(antNum): # 找出能调度出最小时间的蚂蚁的编号
        if timeArray_oneIt[antIndex] < minTime:
            minTime = timeArray_oneIt[antIndex]
            minIndex = antIndex
    for taskIndex in range(taskNum): # 原来的信息素增加
        for nodeIndex in range(nodeNum):
            if pathMatrix_allAnt[minIndex][taskIndex][nodeIndex] == 1:
                pheromoneMatrix[taskIndex][nodeIndex] *= q

    maxPheromoneMatrix = []
    criticalPointMatrix = []
    for taskIndex in range(taskNum):
        maxPheromone = pheromoneMatrix[taskIndex][0]
        maxIndex = 0
        sumPheromone = pheromoneMatrix[taskIndex][0]
        isAllSame = True

        for nodeIndex in range(1, nodeNum):
            if (pheromoneMatrix[taskIndex][nodeIndex] > maxPheromone):
                maxPheromone = pheromoneMatrix[taskIndex][nodeIndex]
                maxIndex = nodeIndex
            if (pheromoneMatrix[taskIndex][nodeIndex] != pheromoneMatrix[taskIndex][nodeIndex-1]):
                isAllSame = False
            sumPheromone += pheromoneMatrix[taskIndex][nodeIndex]
        if (isAllSame == True):
            maxIndex = random(0, nodeNum-1)
            maxPheromone = pheromoneMatrix[taskIndex][nodeIndex]
        maxPheromoneMatrix.append(maxIndex)
        criticalPointMatrix.append(round(antNum * (maxPheromone / sumPheromone)))

def initTimeMatrix(tasks, nodes):
    for i in range(taskNum):
        timeMatrix_i = []
        for j in range(nodeNum):
            timeMatrix_i.append(tasks[i] / nodes[j])
        timeMatrix.append(timeMatrix_i)

def initPheromoneMatrix(taskNum, nodeNum):
    for i in range(taskNum):
        pheromoneMatrix_i = []
        for j  in range(nodeNum):
            pheromoneMatrix_i.append(1)
        pheromoneMatrix.append(pheromoneMatrix_i)

def acaSearch(iteratorNum, antNum):
    resultData = []
    for itCount in range(iteratorNum):
        pathMatrix_allAnt = []   # 三维矩阵:蚂蚁数*任务数*节点数
        for antCount in range(antNum):
            pathMatrix_oneAnt = initMatrix(taskNum, nodeNum, 0) # 初始化全为0
            for taskCount in range(taskNum):
                nodeCount = assignOnetask(antCount, taskCount, nodes, pheromoneMatrix) # 返回第taskCount行最大信息素那一列
                pathMatrix_oneAnt[taskCount][nodeCount] = 1 # 重新规划路径
            pathMatrix_allAnt.append(pathMatrix_oneAnt)

        timeArray_oneIt = calTime_oneIt(pathMatrix_allAnt) # 计算每个蚂蚁本次调度所得到的节点处理任务的时间总和
        resultData.append(timeArray_oneIt)
        updatePheromoneMatrix(pathMatrix_allAnt, pheromoneMatrix, timeArray_oneIt)
    return resultData

def aca():
    initTimeMatrix(tasks, nodes)

    initPheromoneMatrix(taskNum, nodeNum)

    timeArray = acaSearch(iteratorNum, antNum)
    return timeArray

if __name__ == "__main__":
    init()
    timeArray = aca()
    print(timeArray)
