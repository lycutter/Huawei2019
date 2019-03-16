import dataProcess
import SeekForPath
import init
import Schedue
carPath = './map/config_10/car.txt'
crossPath = './map/config_10/cross.txt'
roadPath = './map/config_10/road.txt'



if __name__ == "__main__":


    carData, crossData, roadData = dataProcess.dataProcess(carPath, crossPath, roadPath)
    carRoute = SeekForPath.Seek(carData, crossData, roadData)
    carList, roadList, crossList = init.MapInit(carData, crossData, roadData, carRoute)

    print("Initialize finish, ready to Scheduling......")

    Schedue.MapScheduling(carList, roadList, crossList)


