def rayCasting(p, poly):
    # p是需要判断的点，ploy是多边形的顶点
    px = p['x']  # 取值
    py = p['y']
    flag = 0  # 射线穿过多边形边界的次数为奇数时点在多边形内

    i = 0
    l = len(poly)  # 获取多边形顶点的数量
    j = l - 1
    # for(i = 0, l = poly.length, j = l - 1; i < l; j = i, i++):
    while i < l:
        # 取两个顶点，顶点是顺时针排列的，两个顶点方便后面形成线段
        sx = poly[i]['x']
        sy = poly[i]['y']
        tx = poly[j]['x']
        ty = poly[j]['y']

        # 点与多边形顶点重合
        if (sx == px and sy == py) or (tx == px and ty == py):
            return px, py

        # 判断线段两端点是否在射线两侧
        if (sy < py <= ty) or (sy >= py > ty):
            # 线段上与射线 Y 坐标相同的点的 X 坐标
            x = sx + (py - sy) * (tx - sx) / (ty - sy)
            # 点在多边形的边上
            if x == px:
                return px, py
            # 射线穿过多边形的边界
            if x > px:
                flag = 1 - flag  # 以第一次为例，false变成了true，代表flag为true的时候点在多边形内
        j = i
        i += 1

    return flag


'''定义了一个把字符串中的点转化为列表的函数'''
def getpoint(a):
    i = 0
    p = []
    while i < len(a[1::2]):  # 除去','以后的元素，并且步长为2
        p.append({'x': float(a[::2][i]), 'y': float(a[1::2][i])})  # x为从0开始，step=2；y为从1开始，step=2
        i += 1
    
    print(p)

    return p


# 根据输入的点循环判断芝麻是否在多边形里面，如果全部在外面则输出no,否则输出芝麻的坐标
def judege(point, dbx):
    point_in = []
    point_in_index = []
    point = getpoint(point)
    dbx = getpoint(dbx)
    count = 0
    for p in point:
        count = count + 1
        if rayCasting(p, dbx) == 1:
            point_in.append(p)
            point_in_index.append(count)
            print(p, count)

    return point_in, point_in_index


zhima = [8, 8, 6, 4, 9, 9]
duobianxing = [1, 1, 7, 3, 5, 7]

a = judege(zhima, duobianxing)