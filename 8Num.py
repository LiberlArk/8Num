#coding=utf-8

#知识点：A*搜索算法
#list的深拷贝，假拷贝
#list的排序
#class的使用方式

import copy
import time

g_GoalList = [[1,2,3],
             [4,5,6],
             [7,8,0]]
g_ListArr = []      #当前的待识别队列
g_readArr = []      #已读状态队列

class StruNum:
    myList = []
    myPreList = []
    myCost = 0
    def __init__(self, list = [], prelist = [], cost = 0):
        self.myList = list
        self.myPreList = prelist
        self.myCost = cost

    def SetPre(self, newPreList):
        self.myPreList = newPreList
        self.myCost = newPreList.mycost

    def IsSame(self, struNum1):
        if self.myList == struNum1.myList:
            return True
        else:
            return False

    def GetItsPre(self):
        global g_readArr
        for i in range(0, len(g_readArr), 1):
            if self.myPreList == g_readArr[i].myList:
                return g_readArr[i]

    def GetZeroIndex(self):
        for i in range(0, len(self.myList), 1):
            for j in range(0, len(self.myList[i]), 1):
                if self.myList[i][j] == 0:
                    return [i,j]

    def GetListIndex(self, someList):
        for i in range(0, len(someList), 1):
            if self.myList == someList[i].myList:
                return i
        return -1

    def __repr__(self):
        return repr((self.myList, self.myPreList, self.myCost))

    def GetGoalCost(self):
        sumCost = 9 * 4
        for i in range(0, len(self.myList), 1):
            for j in range(0, len(self.myList[i]), 1):
                if self.myList[i][j] == g_GoalList[i][j]:
                    sumCost -= 4
        return sumCost

def takeThr(elem):
    return elem.myCost

def checkNoAns(list):
    sum = 0
    for i in range(0, len(list), 1):
        for j in range(0, len(list[i]), 1):
            for ii in range(0, i, 1):
                for jj in range(0, len(list[i]), 1):
                    if list[ii][jj] != 0 and list[i][j] != 0 and list[ii][jj] < list[i][j]:
                        sum += 1
            for jj in range(0, j, 1):
                if list[i][jj] != 0 and list[i][j] != 0 and list[i][jj] < list[i][j]:
                    sum += 1
    if sum % 2 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    myList = [[1,3,4],
             [2,8,6],
             [5,7,0]]
    if(checkNoAns(myList) == False):
        print("No Ans!")
        exit(1)
    startNum = StruNum(myList, [], 0)
    g_ListArr.append(startNum)
    startTime = time.time()
    while(g_ListArr != []):
        nowNum = g_ListArr[0]
        g_ListArr.remove(nowNum)    #从队列头移除
        g_readArr.append(nowNum)    #添加到已读队列
        if nowNum.myList == g_GoalList:
            print("Find The Answer!")
            while(nowNum.myPreList != []):
                print(nowNum.myList)
                nowNum = nowNum.GetItsPre()
            print(nowNum.myList)
            break
        else:
            [idx, jdx] = nowNum.GetZeroIndex()
            if idx - 1 >= 0:
                upList = copy.deepcopy(nowNum.myList)
                upList[idx][jdx] = upList[idx - 1][jdx]
                upList[idx - 1][jdx] = 0
                upNum = StruNum(upList, nowNum.myList, nowNum.myCost + 1)
                #A*算法：代价 = 到达此状态代价 + 期望到达目标节点代价
                upNum.myCost += upNum.GetGoalCost()
                #如果新节点没有被走过
                if upNum.GetListIndex(g_readArr) == -1:
                    tmpIndex = upNum.GetListIndex(g_ListArr)
                    if tmpIndex != -1:
                        #当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if upNum.myCost < g_ListArr[tmpIndex].myCost:
                            g_ListArr.remove(g_ListArr[tmpIndex])
                            g_ListArr.append(upNum)
                    else:
                        g_ListArr.append(upNum)

            if idx + 1 < 3:
                downList = copy.deepcopy(nowNum.myList)
                downList[idx][jdx] = downList[idx + 1][jdx]
                downList[idx + 1][jdx] = 0
                downNum = StruNum(downList, nowNum.myList, nowNum.myCost + 1)
                downNum.myCost += downNum.GetGoalCost()
                # 如果新节点没有被走过
                if downNum.GetListIndex(g_readArr) == -1:
                    tmpIndex = downNum.GetListIndex(g_ListArr)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if downNum.myCost < g_ListArr[tmpIndex].myCost:
                            g_ListArr.remove(g_ListArr[tmpIndex])
                            g_ListArr.append(downNum)
                    else:
                        g_ListArr.append(downNum)

            if jdx - 1 >= 0:
                leftList = copy.deepcopy(nowNum.myList)
                leftList[idx][jdx] = leftList[idx][jdx - 1]
                leftList[idx][jdx - 1] = 0
                leftNum = StruNum(leftList, nowNum.myList, nowNum.myCost + 1)
                leftNum.myCost += leftNum.GetGoalCost()
                # 如果新节点没有被走过
                if leftNum.GetListIndex(g_readArr) == -1:
                    tmpIndex = leftNum.GetListIndex(g_ListArr)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if leftNum.myCost < g_ListArr[tmpIndex].myCost:
                            g_ListArr.remove(g_ListArr[tmpIndex])
                            g_ListArr.append(leftNum)
                    else:
                        g_ListArr.append(leftNum)

            if jdx + 1 < 3:
                rightList = copy.deepcopy(nowNum.myList)
                rightList[idx][jdx] = rightList[idx][jdx + 1]
                rightList[idx][jdx + 1] = 0
                rightNum = StruNum(rightList, nowNum.myList, nowNum.myCost + 1)
                rightNum.myCost += rightNum.GetGoalCost()
                # 如果新节点没有被走过
                if rightNum.GetListIndex(g_readArr) == -1:
                    tmpIndex = rightNum.GetListIndex(g_ListArr)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if rightNum.myCost < g_ListArr[tmpIndex].myCost:
                            g_ListArr.remove(g_ListArr[tmpIndex])
                            g_ListArr.append(rightNum)
                    else:
                        g_ListArr.append(rightNum)

            #按照COST排序
            g_ListArr.sort(key=takeThr)
    endTime = time.time()
    print("Finish! Time = %d" %(endTime - startTime))