# 原神抽卡记录导出CSV，附IOS抓包方法（多平台可用windows、mac、linux）
参考repo：
1. https://github.com/sunfkny/genshin-gacha-export
2. https://github.com/Fidetro/genshin-impact-gachalog
仅提供数据爬取方法，供各位原神爱好者自行分析研究

# 功能  
- 导出最近6个月抽卡记录  
- 合并历史数据与当前数据，例如六月份查询到1～6月数据，七月份再次查询到2～7月数据，数据按时序进行合并
- 提供binary search合并方法，数据量大时可用（氪佬）

# 使用方式  
1. 抓包
- 安卓端或pc端
![](https://github.com/CanoeByGuitar/genshin-gacha-crwal/blob/main/AndroidorPC.jpg)

- IOS
使用抓包工具Stream,游戏内刷新抽卡记录页抓获api

2. 复制接口url后，执行脚本，目录下会生成`genshin_常驻祈愿.csv`、`genshin_角色活动祈愿.csv`、`genshin_武器活动祈愿.csv`
```shell
python3 crwal.py 'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?xxxxx'
```
3. 打开analysis.html按要求操作，预期结果如下
![](https://github.com/CanoeByGuitar/genshin-gacha-crwal/blob/main/analysis.jpg)

# 未来
数据量大之后，可能会增添更多分析及动态图，并嵌入vue-electron.

