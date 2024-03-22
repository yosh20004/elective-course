import requests
import re
import time

url = "http://219.216.96.4/eams/stdElectCourse!batchOperator.action?profileId=2552"  # 替换成自己选课页面的url

time_gap = 0.49  # 请设置大于0.49s的睡眠时间

data = {
    "optype": "true",
    "operator0": "375184:true:0",  # 课程编号 似乎与前端展示编号没有明显联系 必须在网络活动中获取
    "lesson0": "375184",
    "schLessonGroup_375184": "undefined",
    #"virtualCost": "50"  # 投放的权重值
}

# 进入选课系统后打开f12 选中课程点击选课并找到表单数据


cookies = {
    "semester.id": "72",
    "JSESSIONID": "ACC0FAD1D914DAB918F8BDF41AE67071.std17",  # 注意这里有两个JSESSIONID，通常应该使用最新的一个
    "SERVERNAME": "xk3",
    "GSESSIONID": "ACC0FAD1D914DAB918F8BDF41AE67071.std17"
}

# 进入教务系统后打开f12 在 '我的' 栏中切换 找到dataquery等任意表头中含有cookie的网络活动 记录cookie并以以上格式填写

time_ = 0

while True:

    response = requests.post(url, data=data, cookies=cookies)  # 向服务器发送post指令

    if '已投放权重值' in response.text:
        print('success')
        break  # 成功后结束程序执行

    if '请不要过快点击' in response.text:
        print('alart')
        time_gap += 0.05  # 如果出现 '请不要过快点击' 请适当增加睡眠时间

    
    else:
        html = response.text
        pattern_fail = re.compile(r'失败:(.*?)</br>')

        try:
            print(pattern_fail.findall(html)[0])  # 打印抢课失败原因
        except:
            if '当前选课不开放' in html:
                time_ += 1

                print('当前选课不开放', time_)
  

            else:
                print('未知错误')  # 未知错误请打印html并联系我

        
        # print(html)  #打印捕获html页面(可选)


    # break  # 仅供实验时使用单次循环 多次执行请删除该句

    time.sleep(time_gap)  # 学校服务器访问限制应该是0.5s 请设置大于0.49s的睡眠时间

    # 添加sleep语句否则会报 '请不要过快点击'




