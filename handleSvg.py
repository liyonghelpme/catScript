#coding:utf8
from xml.dom import minidom
import json
import re

svg = minidom.parse('map2.svg')
path = svg.getElementsByTagName('path')
#初始城堡属性
rect = svg.getElementsByTagName('rect')

tras = re.compile('(-?\d+(\.\d+)?),(-?\d+(\.\d+)?)')
group = svg.getElementsByTagName('g')
txy = []
print group
for node in group:
    if node.getAttributeNode('transform'):
        transform = node.getAttributeNode('transform').nodeValue
        tf = tras.findall(transform)
        print tf
        for k in tf:
            txy = [float(k[0]), float(k[2])]

print 'txy', txy
import math
pat = re.compile('(-?\d+(\.\d+)?),(-?\d+(\.\d+)?)')
allPath = []
nid = 0
#edgeId = {}
allNodes = {}
for node in path:
    if node.getAttributeNode('id'):
        pt = [0, 0]
        if node.getAttributeNode('transform'):
            ptrans = node.getAttributeNode('transform').nodeValue
            tf = tras.findall(ptrans)
            for k in tf:
                pt = [float(k[0]), float(k[2])]

        path_id = str(node.getAttributeNode('id').nodeValue)
        pnode = node.getAttributeNode('d').nodeValue
        coord = pat.findall(pnode)
        #坐标转化成绝对坐标 游戏中使用
        numCoord = []
        lastPos = [txy[0]+pt[0], txy[1]+pt[1]]
        for k in coord:
            numCoord.append((math.floor(lastPos[0]+float(k[0])), math.floor(lastPos[1]+float(k[2])), nid))
            allNodes[nid] = numCoord[-1]
            nid = nid+1
            lastPos = numCoord[-1]
        print 'path'
        print numCoord
        allPath.append(numCoord)

allCity = []
cidToCity = {}
for node in rect:
    rxy = [0, 0]
    if node.getAttributeNode('transform'):
        transform = node.getAttributeNode('transform').nodeValue
        tf = tras.findall(transform)
        for k in tf:
            rxy = [float(k[0]), float(k[2])]

    x = float(node.getAttributeNode('x').nodeValue)+txy[0]+rxy[0]
    y = float(node.getAttributeNode('y').nodeValue)+txy[1]+rxy[1]
    width = float(node.getAttributeNode('width').nodeValue)
    height = float(node.getAttributeNode('height').nodeValue)
    cid = str(node.getAttributeNode('id').nodeValue)
    cdata = (cid, x, y, width, height, nid)
    allNodes[nid] = [True, cdata]
    nid += 1
    allCity.append(cdata)
    #nid = max(nid, cid)
    cidToCity[cid] = cdata

print 'city'
print allCity
print cidToCity

#归并边

#处理的结果是
#nodeId1 -----> nodeId2----->nodeId3 邻居node
#nodeId2----> nodeId1----->nodeId3  邻居node
#得到所有node的编号
#id ---> neibor
nodeList = {}
#检测所有的path node如果属于一个
#
sameSet = {}
    
def checkIn(x, y, width, height, px, py):
    if px >= x and py >= y and px <= x+width and py <= y+height:
        return True
    return False

#邻接链表构建 
allEdge = {}
for n in allPath:
    start = n[0]
    end = n[-1]
    #for k in n:
    #    allNodes[nid] = k
    #    edgeId[k] = nid
    #    nid += 1
    for k in xrange(0, len(n)):
        nodeId = n[k][2]
        temp = allEdge[nodeId] = []
        print 'node'
        print nodeId
        #print n[k], n[k+1]
        if k > 0: 
            temp.append(n[k-1][2])
        if k < len(n)-1:
            temp.append(n[k+1][2])
print 'all edge'
for k in allEdge:
    print k, allEdge[k], allNodes[k]

#每个城市 对应的所有的node列表
#每个node 对应的 城市列表
cityToNode = {}
nodeToCity = {}
#c[0]   cid
#n    nid
for n in allNodes:
    #print n
    for c in allCity: 
        node = allNodes[n]
        if checkIn(c[1], c[2], c[3], c[4], node[0], node[1]):
            temp = cityToNode.setdefault(c[0], [])
            temp.append(n)
            nodeToCity[n] = c

print 'city to Node'
for k in cityToNode:
    print k, cityToNode[k]


print 'node to city'
for k in nodeToCity:
    print k, nodeToCity[k]




#归并边
print 'allNodes'
for k in allNodes:
    print k, allNodes[k]

#移除旧的边 加入新的边
for k in cityToNode:
    neibors = []
    for n in cityToNode[k]:
        neibors += allEdge[n] 
        allEdge.pop(n)
    cityNodeId = cidToCity[k][5]
    allEdge[cityNodeId] = neibors

print 'merge Edge'
for k in allEdge:
    print k, allEdge[k]

#dump Json allNodes 
#dump Json allEdge
dumpNode = []
for k in allNodes:
    if nodeToCity.get(k) == None:
        ndata = allNodes[k]
        if ndata[0] != True:
            dumpNode.append([k, [int(ndata[0]), int(ndata[1]), False]])
        else:
            #print ndata
            ndata = ndata[1]
            dumpNode.append([k, [int(ndata[1]+ndata[3]/2), int(ndata[2]+ndata[4]/2), True]])
print 'dump Node'
for k in dumpNode:
    print k

#替换所有allEdge 中的边中使用了 和City 重合的端点
for k in allEdge:
    neibor = []
    for n in allEdge[k]:
        #顶点属于某个city
        if nodeToCity.get(n):
            neibor.append(nodeToCity[n][5])
        #独立定点
        else:
            neibor.append(n)
    allEdge[k] = neibor

print 'merge Edge all City node'
for k in allEdge:
    print k, allEdge[k]

f = open('mapData.lua', 'w')
f.write('MapDataInitYet = false\n')
s = json.dumps(dumpNode)
f.write('MapNode = '+s.replace('[', '{').replace(']', '}')+'\n')
s = json.dumps(allEdge.items())
f.write('MapEdge = '+ s.replace('[', '{').replace(']', '}'))
f.close()

    



#寻路寻找一个定点的所有邻居  只考虑城堡之间的 直接相连接的特性 以及路径点



