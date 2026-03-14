# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:10:08 2025

@author: DELL
"""

import random
import matplotlib.pyplot as plt
import numpy as np
 
 
class schellingModel:
    def __init__(self, size, threshold, kindNum):
        # 初始化谢林模型所需的参数
        self.size = size
        self.threshold = threshold
        self.matrix = np.zeros((size, size))
        self.kindNum = kindNum
        self.population = 0
        if kindNum == 2:
            self.red = 1
            self.white = 0
            self.blue = 2
        elif kindNum == 3:
            self.red = 1
            self.white = 0
            self.blue = 2
            self.yellow = 3
        elif kindNum == 4:
            self.red = 1
            self.white = 0
            self.blue = 2
            self.yellow = 3
            self.purple = 4
        else:
            print("输入的种群数量要小于4,大于2")
        # 初始化谢林模型参数——种群矩阵、人口数
        for i in range(size):
            for j in range(size):
                self.matrix[i][j] = random.randint(0, kindNum)
                if self.matrix[i][j] != 0:
                    self.population += 1
 
    # 判断（i，j）点是否满意————判断（i，j）点周围有多少个相似的邻居
    def is_satisfied(self, i, j, kind):
        same_neighbour = -1  # 要把自己除去
        neighbour_matrix = self.matrix[i - 1 if i - 1 > 0 else 0:i + 2 if i + 2 <= self.size else self.size,
                           j - 1 if j - 1 > 0 else 0:j + 2 if j + 2 <= self.size else self.size]
        for x in range(len(neighbour_matrix)):
            for y in range(len(neighbour_matrix[x])):
                if neighbour_matrix[x][y] == kind:
                    same_neighbour += 1
        if same_neighbour >= self.threshold:
            return True
        else:
            return False
 
    # 随机获取一个位置作为搬家地点
    def random_find_place(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        while self.matrix[i][j] != 0:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
        return (i, j)  # 返回i、j构成的元组
 
    # 集体完成一次搬家
    def move(self):
        for i in range(self.size):
            for j in range(self.size):
                kind = self.matrix[i][j]
                judge = self.is_satisfied(i, j, kind)
                if judge == 0:  # 不满意
                    (x, y) = self.random_find_place()
                    self.matrix[x][y] = kind
                    self.matrix[i][j] = self.white  # 把原本的家庭住址变为空
 
    # 计算当前的满意家庭数
    def satisfy_num(self):
        satisfy = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    kind = self.matrix[i][j]
                    judge = self.is_satisfied(i, j, kind)
                    if judge == 1:
                        satisfy += 1
        #print(self.matrix)
        return satisfy
 
    # 画图谢林模型图
    def draw(self, time, satisfy):
        if self.kindNum == 2:
            redx = []
            bluex = []
            redy = []
            bluey = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == self.blue:
                        bluex.append(i)
                        bluey.append(j)
                    elif self.matrix[i][j] == self.red:
                        redx.append(i)
                        redy.append(j)
            plt.scatter(redx, redy, c='r', marker='.', linewidths=0)
            plt.scatter(bluex, bluey, c='b', marker='.', linewidths=0)
            if satisfy == 0:
                plt.title('Initial')
                plt.show()
                return 0
            else:
                title = str(time) + ' times satisfy:' + str(float(satisfy) / float(self.population)*100) + "%"
                satisfy_rate = float(satisfy) / float(self.population)*100
                plt.title(title)
                plt.show()
                return satisfy_rate
        elif self.kindNum == 3:
            redx = []
            bluex = []
            redy = []
            bluey = []
            yellowx = []
            yellowy = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == self.blue:
                        bluex.append(i)
                        bluey.append(j)
                    elif self.matrix[i][j] == self.red:
                        redx.append(i)
                        redy.append(j)
                    elif self.matrix[i][j] == self.yellow:
                        yellowx.append(i)
                        yellowy.append(j)
            plt.scatter(redx, redy, c='r', marker='.', linewidths=0)
            plt.scatter(bluex, bluey, c='b', marker='.', linewidths=0)
            plt.scatter(yellowx, yellowy, c='y', marker='.', linewidths=0)
            if satisfy == 0:
                plt.title('Initial')
                plt.show()
                return 0
            else:
                title = str(time) + ' times satisfy:' + str(float(satisfy) / float(self.population)*100) + "%"
                satisfy_rate = float(satisfy) / float(self.population)*100
                plt.title(title)
                plt.show()
                return satisfy_rate
        elif self.kindNum == 4:
            redx = []
            bluex = []
            redy = []
            bluey = []
            yellowx = []
            yellowy = []
            purplex = []
            purpley = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == self.blue:
                        bluex.append(i)
                        bluey.append(j)
                    elif self.matrix[i][j] == self.red:
                        redx.append(i)
                        redy.append(j)
                    elif self.matrix[i][j] == self.yellow:
                        yellowx.append(i)
                        yellowy.append(j)
                    elif self.matrix[i][j] == self.purple:
                        purplex.append(i)
                        purpley.append(j)
            plt.scatter(redx, redy, c='r', marker='.', linewidths=0)
            plt.scatter(bluex, bluey, c='b', marker='.', linewidths=0)
            plt.scatter(yellowx, yellowy, c='y', marker='.', linewidths=0)
            plt.scatter(purplex, purpley, c='p', marker='.', linewidths=0)
            if satisfy == 0:
                plt.title('Initial')
                plt.show()
                return 0
            else:
                title = str(time) + ' times satisfy:' + str(float(satisfy) / float(self.population)*100) + "%"
                satisfy_rate = float(satisfy) / float(self.population)*100
                plt.title(title)
                plt.show()
                return satisfy_rate
 
 
if __name__ == '__main__':
    s = schellingModel(36, 4, 2)  # 150户人家、阙值点为4，两类人群
    s.draw(0, 0)  # 画出初始图
    i = 1
    satisfy_num = 0
 
    while(1):
        # 两次move计算聚合层度变化率
        s.move()
        satisfy_num1 = s.satisfy_num()
        satisfy_rate1 = s.draw(i, satisfy_num1)
        i += 1
        s.move()
        satisfy_num2 = s.satisfy_num()
        satisfy_rate2 = s.draw(i, satisfy_num2)
        cluster_rate = (satisfy_rate2-satisfy_rate1)/satisfy_rate1
        if cluster_rate < 0.000001:  # 什么时候停止算法迭代
            break
        i += 1
