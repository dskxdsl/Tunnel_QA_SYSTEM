# -*- coding: utf-8 -*-


import sys
from py3process_question import Question
# 创建问题处理对象，这样模型就可以常驻内存
que=Question()
# Restorepip freeze > requirements.txt
def enablePrint():
    sys.stdout = sys.__stdout__
enablePrint()

q0 = "佛山地铁2号线的竣工验收时间是什么时候?"
q1 = "佛山地铁2号线的建设单位是哪个？"
q2 = "深圳地铁14号线的基本介绍?"
q3 = "衬砌损裂的治理措施有哪些?"

result=que.question_process(q3)
print(result)
