#-*- coding: UTF-8 -*-
#连接数据库，生成查询语句，返回结果

import re
from py2neo import Graph

class Query():
    def __init__(self):
        #这里演示使用的是本地数据库
        self.graph=Graph(host="127.0.0.1",port=7687,user="neo4j",password="root")
    # 运行cql语句
    def run(self,cql):
        find_rela = self.graph.run(cql)
        return find_rela


class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0:self.get_tunnel_time,
            1:self.get_tunnel_struc,
            2:self.get_tunnel_intro,
            3:self.get_disease_rep
        }

        # 连接数据库
        self.graph = Query()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        return answer

    def get_disease_rep_name(self):
        ## 获取tdrep在原问题中的下标
        tag_index = self.question_flag.index("ndm")
        ## 获取隧道修复名称
        TDrep_name = self.question_word[tag_index]
        return TDrep_name

    # 获取隧道名字
    def get_tunnel_name(self):
        ## 获取nm在原问题中的下标
        tag_index = self.question_flag.index("nt")
        ## 获取电影名称
        Tunnel_name = self.question_word[tag_index]
        return Tunnel_name

    # 实体name名字属性
    def get_name(self,type_str):
        name_count=self.question_flag.count(type_str)
        if name_count==1:
            ## 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            ## 获取电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list=[]
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    # 评分专用的
    def get_num_x(self):
        x = re.sub(r'\D', "", "".join(self.question_word))
        return x

    # 0:Tunnel time
    def get_tunnel_time(self):
        # 获取电影名称，这个是在原问题中抽取的
        tunnel_name=self.get_tunnel_name()
        cql = f"match (x:Tunnel) where x.name='{tunnel_name}' return x.time"
        print(cql)
        answer = self.graph.run(cql)
        final_answer = tunnel_name + "的竣工验收时间为：" + answer
        return final_answer
    # 1:Tunnel 建设单位
    def get_tunnel_struc(self):
        tunnel_name=self.get_tunnel_name()

        final_answer = "建设单位尚不清楚"
        return final_answer
    # 2:Tunnel 简介
    def get_tunnel_intro(self):
        tunnel_name = self.get_tunnel_name()
        cql = f"match (x:Tunnel) where x.name='{tunnel_name}' return x.intro"
        print(cql)
        answer = self.graph.run(cql)
        final_answer = tunnel_name + "的简介为:" + str(answer)
        return final_answer

    # 3:TDrep 修复措施
    def get_disease_rep(self):
        TDrep_name = self.get_disease_rep_name()
        cql = f"match(x:TDrep) where x.name='{TDrep_name}' return x.gm"
        print(cql)
        answer = self.graph.run(cql)
        final_answer = TDrep_name + "的修复方法为:" + str(list(answer)[0][0])
        return final_answer
