# -*- coding: utf-8 -*-
'''
将csv文件导入neo4j数据库
import文件夹是neo4j默认的数据导入文件夹
所以首先要将data文件夹下所有csv文件拷贝到neo4j数据库的根目录import文件夹下，没有则先创建import文件夹
然后运行此程序
'''


from py2neo import Graph
graph = Graph(host="127.0.0.1",port=7687,user="neo4j",password="root")

"""
#测试
cql='''
MATCH (p:Person)
where p.name="张柏芝"
return p
'''
"""

#导入节点 隧道类型  == 注意类型转换
cql = '''
LOAD CSV WITH HEADERS  FROM "file:///tunnel.csv" AS line
MERGE (p:Tunnel{Tid:toInteger(line.id),name:line.name,intro:line.intro,R:line.tunnelR,scanlen:line.tunnelL,method:line.ShiGongMethod})
'''
result = graph.run(cql)
print(result,"隧道类型 存储成功")

#导入节点 病害类型  == 注意类型转换
cql = '''
LOAD CSV WITH HEADERS  FROM "file:///disease.csv" AS line
MERGE (p:TDisease{Did:toInteger(line.id),name:line.name,attrib:line.attrib,time:line.time,locate:line.locate,Mid:toInteger(line.MeasureID),Tid:toInteger(line.tunnelID)})
'''
result = graph.run(cql)
print(result,"病害类型 存储成功")

#导入节点 病害治理类型  == 注意类型转换
cql = '''
LOAD CSV WITH HEADERS  FROM "file:///measure.csv" AS line
MERGE (p:TDrep{Mid:toInteger(line.id),name:line.name,def:line.def,influnce:line.influnce,reason:line.reason,gm:line.gm})
'''
result = graph.run(cql)
print(result,"病害治理类型 存储成功")

#导入关系 Happen  隧道发生的病害 1对多
cql='''
match (x:Tunnel),(y:TDisease) where x.Tid = y.Tid
merge (x)-[r:Happen{type:"发生病害"}]->(y)
'''
result = graph.run(cql)
print(result,"隧道<-->隧道病害 存储成功")

# 导入关系 IsRelated  病害治理方案 1对1
cql='''
match (x:TDisease),(y:TDrep) where x.Mid = y.Mid
merge (x)-[r:IsRelated{type:"病害治理"}]->(y)
'''
result = graph.run(cql)
print(result,"隧道病害<-->病害治理 存储成功")




