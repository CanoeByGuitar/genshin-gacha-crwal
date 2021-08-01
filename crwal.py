import os
import json
import xlwt
from urllib.parse import urlparse, parse_qs
import requests
import sys
import urllib
import time
import datetime
import pandas as pd


'''
输入示例：
https://webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html
?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=71eaf9e3bf2b240122a3f78e9bbfd3e43032fd&timestamp=1626824136
&lang=zh-cn&device_type=mobile&ext=%7b%22loc%22%3a%7b%22x%22%3a1639.1116943359375%2c%22y%22%3a195.01763916015626%2c%22z%22%3a-2642.400146484375%7d%2c%22platform%22%3a%22IOS%22%7d
&game_version=CNRELiOS2.0.0_R3696781_S3788800_D3875455&region=cn_gf01
&authkey=LsK%2bcVI5w7J5KpQIUf4SOKWjwbjGrlfH%2fvU4ua0FfHNbQWUhgxtoPW3Lt（后面省略）
'''

def main():
    if len(sys.argv) != 2:
        print("请放入抓包后的接口后执行，如 python3 gacha.py 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?xxxxx'")
        return
    URL = sys.argv[1]
    parsed_url = urlparse(URL)
    params = parse_qs(parsed_url.query)
    authkey = params['authkey'][0]

            
    print_str = ""
    reuqest_param = {'size':20,
    'authkey':authkey,
    'authkey_ver':1,
    'sign_type':2,
    'auth_appid':"webview_gacha",
    'init_type':301,
    'timestamp':int(time.time()),
    'lang':"zh-cn",
    'device_type':"mobile",
    'game_biz':"hk4e_cn"
    }

    # 根据输入url更新params，主要为复制用户私有的auth_key
    for key in params:
        reuqest_param[key] = params[key][0]

    # 三个池
    configs = [{"config_type":"301","config_name":"角色活动祈愿"},{"config_type":"302","config_name":"武器活动祈愿"},{"config_type":"200","config_name":"常驻祈愿"}]

    #%%
    for config in configs : 
        df = pd.DataFrame(columns=("抽卡时间","名称","类别","星级"))
        
        
        gacha_type = config['config_type']
        endId = 0


        for page in range(1, 9999):        
            config_name = config['config_name']
            # 原神抽卡记录接口
            url = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?"                                    
            reuqest_param["gacha_type"] = gacha_type
            reuqest_param["page"] = page
            reuqest_param["end_id"] = endId        
                        
            url += urllib.parse.urlencode(reuqest_param)
            # print(url)

            print(" 正在查询"+config_name+":第"+str(page)+"页")
            request = requests.get(url)
            formatJSON = request.json()        
            if formatJSON["retcode"] != 0:
                print("发生错误："+formatJSON["message"])
                return
            if len(formatJSON["data"]["list"]) == 0:
                break
            for  data in formatJSON["data"]["list"]:    
                endId=data["id"]     
                # print(data)
                df = df.append({"抽卡时间":data["time"],"名称":data["name"],"类别":data["item_type"],"星级":data["rank_type"]},ignore_index=True)

            # 按时间戳递增排序
            df['抽卡时间'] = pd.to_datetime(df['抽卡时间'])
            df.sort_values('抽卡时间',inplace = True)
            df = df.reset_index(drop = True)

        # 写入       
        dataPath = "./genshin_"+config_name+".csv"
        if os.path.isfile(dataPath):
            # 不能去重，只能merge，因为十连出的十样东西抽取时间都是一样的
            localData = pd.read_csv(dataPath,sep='\t')
            localData['抽卡时间'] = pd.to_datetime(localData['抽卡时间'])
            localData.sort_values('抽卡时间',inplace = True)
            localData = localData.reset_index(drop = True)

            # 找到第一个比localData时间靠后的新抽卡记录
            flag = True #没找到时flag为true，对原数据不做任何更改
            index = 0
            df1_end = localData.iloc[-1]
            # # 数据量较大时可采用二分查找
            # left = 0
            # right = df.shape[0]-1
            # while(left < right):
            #     mid = int((left+right)/2)
            #     # 从左到右第一次达成条件
            #     if(df1_end["抽卡时间"]<df.iloc[index]["抽卡时间"]):
            #         right = mid
            #     else:
            #         left = mid + 1
            # index = left

            for index in range(df.shape[0]):
                if(df1_end["抽卡时间"]<df.iloc[index]["抽卡时间"]):
                    flag = False
                    break

            if(flag == False):
                localData = localData.append(df.iloc[index:],ignore_index=True)
                localData.to_csv(dataPath, sep='\t', encoding='utf-8',index=False)
        else:
            df.to_csv(dataPath, sep='\t', encoding='utf-8',index=False)
            
main()