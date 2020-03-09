import jieba
import re
import time
class FC(object):
    def __init__(self, filename):
        self.data = None
        with open(filename, "r") as f:
            self.data = f.read()
            self.data = re.sub("[。、“，\s：”。.．？\-\"]","",self.data)
            self.data = jieba.cut(self.data, cut_all=False)  #分词
            self.data = list(self.data)
        self.excludes = ["众人","他们","自己","起来","说道","知道","我们","自己","你们","如今","只见","怎么","那里","太太", "只见","怎么","不是","两个","这个","一个","姑娘","咱们",
        "进来","这里","一面","奶奶","没有","这样","不知","什么","大家","老爷","只得","回来","告诉","东西","就是","只是","大家","这些","不敢","出去","所以","不过","的话","丫头","出来",
        "不好","姐姐","鸳鸯","不能","一时","一时","心里","听见","几个","答应","过来","今日","银子","如此","二人","还有","只管","这么","这么","一回","外头","这话","那边","那些","罢了",
        "今儿","听说","屋里","那些","看见","自然","打发","说话","不得","原来","不用","人家","问道","如何","丫头","一句","一声","家里","这会子","媳妇","小丫头","妹妹","进去","进来"]
    
    def search(self, keyword):
        count = 0
        for item  in self.data:
            if keyword in item:
                count = count+1
        return count
    
    def statistics(self, limit=30):
        res = {}
        for item in self.data:
            if len(item) == 1 or item in self.excludes:
                continue
            if "黛玉" in item:
                item = "黛玉"
            res[item] = res.get(item, 0) + 1

        res = list(res.items())
        res = sorted(res, key=lambda key: key[1], reverse=True)
        res = res[:limit]
        return res
  
    
fc = FC("1.txt")
print(fc.search("黛玉"))
res = fc.statistics()
print(res)