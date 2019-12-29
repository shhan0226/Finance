#/usr/bin/python
# -*- coding:utf-8 -*-
# 작성자 : 한석현

import numpy as np




if __name__ == '__main__':

    a1 = np.array([1, 2, 3])
    print('1D -----\n', a1)

    #2D array [[]]
    a2 = np.array([[1, 2, 3], [4, 5, 6]])
    print('\n2D -----\n', a2)

    #3D array [[[]]]
    a3 = np.array([[[1, 2, 3], [4, 5, 6]],[[1, 2, 3],[4, 5, 6]]])
    print('\n3D -----\n', a3)

    #array range 0~15
    c = np.arange(15)
    print(c)

    #(행,렬) 1D ==> 2D
    c = c.reshape(3, 5)
    print(c)

    #0~100, 5씩
    d = np.arange(0, 100, 5)
    print(d)

    #1D ==> 3D
    d = d.reshape(2, 2, 5)
    print(d)

    #Scala, nd operation
    n1 = np.array([[1, 0],     #2x2 array
                   [0, 1]])
    
    n2 = np.array([[1, 2],     #2x2 array
                   [3, 4]])

    print('\n', n1 + n2 )
    print('\n', n1 - n2 )

    #Scala Mul, No Matirx Mul
    print('\n', n1 * n2 )
    print('\n', n1 / n2 )

    #do not Zero div
#    print('\n', n2 / n1 )

    
    print('\n', n1 + 1 )
    print('\n', n1 * 2 )
    
    #Vector Mul
    print('\n', np.dot(n1, n2))
    print('\n', n1.dot(n2))

    #range 0~11, Matrix (3,4)
    n3=np.arange(12).reshape(3,4)
    print('\n\n', n3)

    # sum열, 세로
    print('\n', n3.sum(axis=0))

    # sum행, 가로
    print('\n', n3.sum(axis=1))

    #Max
    print('\n', n3.max(axis=1))
    
    #Mean
    print('\n', n3.mean(axis=0))

    print('\n\n', n3)
    print('\n', n3.max())
    print('\n', n3.min())
    print('\n', n3.sum())
    print('\nmean', n3.mean())
    print('\n', n3.std()) #표준편차
    print('\n', n3.var()) #분산
    print('\n', n3.cumsum()) #각 원소의 누적 합
    print('\n', n3.cumprod()) #각 원소의 누적 곱


    print('\nSlicing!') 
    v = np.array([  [11, 12, 13, 14, 15],
                    [21, 22, 23, 24, 25],
                    [31, 32, 33, 34, 35],
                    [41, 42, 43, 44, 45] ])
    print(v)
    print(v[1, 2])
    print(v[1][2])
    print(v[:, 1])      #열 0부터 시작
    print(v[1:3, 1])    #2~3행, 2열 데이터 추출
    print(v[1, :])      #2행, 전체절



