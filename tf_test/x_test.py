#coding:utf8
import numpy as np
from numpy.random import choice
from random import sample
import sys
import random

"""
例子：
组合优化问题「背包问题」。比如，你准备要去野游1个月，但是你只能背一个限重50公斤的背包。现在你有不同的必需物品，
它们每一个都有自己的「生存点数」（具体在下表中已给出）。
因此，你的目标是在有限的背包重量下，最大化你的「生存点数」。
"""
MAX_WEIGHT=80
TEST_TIMES=100
def solve_package_problem():
    a=np.array([15,25,35,45,55,70])
    w=np.array([10,15,20,25,30,35])
    count=0

    #初始化变量
    z_max=0
    x_right=[]
    a_right=0

    while count<TEST_TIMES:
        num=a.shape[0]
        x=[choice([0,1]) for _ in range(num)]
        s=w*x
        z=a*x
        count+=1

        if np.linalg.norm(s, 1) <= MAX_WEIGHT:
            z_value=np.linalg.norm(z,1)
            if z_value>z_max:
                z_max=z_value
                x_right=x
                a_right=np.linalg.norm(s, 1)

    print('survival points:'+str(z_max))
    print('choice matrix:'+str(x_right))
    print(u'最佳个体是：'+str([i for i in range(len(x_right)) if x_right[i]==1]))
    print('total weight:'+str(a_right))


#商旅问题，求最短路径

def solve_tsp_problem():
    file_name = './test_data.txt'
    raw_data = open(file_name, 'r').readlines()
    point_info=[]
    for line in raw_data[6:-1]:
        point=line.strip()[-6:].strip().split(' ')
        point=[x for x in point if x!='']
        point_info.append(np.array(map(lambda x:int(x),point)))
    # print(point_info)
    num=len(point_info)
    print(num)
    # dest_point=np.array([np.linalg.norm(point_info[i]-point_info[j]) for i in range(num) for j in range(num)]).reshape(num,num)
    # print(dest_point.shape)
    dest_point=np.zeros((num,num))
    for i in range(num):
        for j in range(num):
            dest_point[i][j]=dest_point[j][i]=0 if i==j else np.linalg.norm(point_info[i]-point_info[j])
    # dest_point=np.triu(np.matrix(dest_point),0)
    print(dest_point.shape)
    count=0
    n=1000
    min_value=sys.maxint
    test_mat = np.zeros((num, num))
    num_list=[]
    while count<n:
        x = np.zeros((num, num))
        # s=0
        # while s<num:
        #
        #     m,k=choice([i for i in range(num)]),choice([i for i in range(num)])
        #     if m!=k:
        #         x[m][k]=1
        #         s+=1
        for i in range(num):
            x_index=sample([j for j in range(num) if j!=i],1)[0]
            x[i][x_index]=1
            num_list.append(x_index)
        count+=1
        min_dest=x*dest_point
        dest_value=min_dest.sum()
        # print(dest_value)
        if dest_value<min_value and dest_value>0:
            min_value=dest_value
            test_mat=x
            # print(num_list)
    print(min_value)
    # print(test_mat)
    # print(test_mat[0])


"""
使用遗传算法，求解y=x**2在[0,31]上x最大数，x为整数。
"""
def x_pow_2_problem():
    s_list=[i for i in range(32)]
    [s1,s2,s3,s4]=random.sample(s_list,4)
    print(s1,s2,s3,s4)
    p_total=reduce(lambda x,y:x+y,map(lambda s:s**2,[s1,s2,s3,s4]))
    print(p_total)
    p_s1=round(float(s1**2)/p_total,2)
    p_s2 = round(float(s2 ** 2) / p_total,2)
    p_s3 = round(float(s3 ** 2) / p_total,2)
    p_s4 = round(float(s4 ** 2) / p_total,2)
    print(p_s1,p_s2,p_s3,p_s4)
    r1=p_s1
    r2=r1+p_s2
    r3=r2+p_s3
    r4=r3+p_s4
    print(r1,r2,r3,r4)
    random_num=[random.random() for _ in range(4)]
    print(random_num)



if __name__ == '__main__':
    solve_package_problem()
    # solve_tsp_problem()
    # x_pow_2_problem()
