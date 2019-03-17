from collections import defaultdict
from heapq import *

import dataProcess
import SeekForPath

carPath = './map/config_10/car.txt'
crossPath = './map/config_10/cross.txt'
roadPath = './map/config_10/road.txt'
carData, crossData, roadData = dataProcess.dataProcess(carPath, crossPath, roadPath)


def dijkstra(edges, f, t):

    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))



    return float("inf")

def Seek(carData, crossData, roadData):

    edges = []

    # 生成地图（双向图）
    for i in range(len(roadData)):
        if (roadData[i][-1] == 1):
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            edges.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))

    # 生成地图（单向图）
    # for i in range(len(roadData)):
    #     if (roadData[i][-1] == 1):
    #         edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))

    # print("ok")

    carRoute = []
    # print(dijkstra(edges, "22", "2"))


    result = dijkstra(edges, "2", "31")
    # result = dijkstra(edges, str(carData[carNum][1]), str(carData[carNum][2]))
    sumarize = []
    while result[1] != ():
        sumarize.append(int(result[0]))
        if result[1] != ():
            result = result[1]
    sumarize.append(int(result[0]))
    # print(sumarize)

    # 可用折半查找法优化
    lengthSumarize = len(sumarize)
    carRouteTmp = []
    for i in range(1, lengthSumarize):
        for j in range(len(roadData)):
            if ((roadData[j][-3] == sumarize[lengthSumarize - i] and roadData[j][-2] == sumarize[lengthSumarize - i -1]) or (roadData[j][-2] == sumarize[lengthSumarize - i] and roadData[j][-3] == sumarize[lengthSumarize - i -1])):
                carRouteTmp.append(roadData[j][0])
    carRoute.append(carRouteTmp)
    print("OK")

if __name__ == "__main__":
    Seek(carData, crossData, roadData)