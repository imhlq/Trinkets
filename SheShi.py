# 22/4/16
# 揲蓍法
# 文章：https://xhou.me/2022/04/%E8%AE%BA%E7%AE%97%E5%91%BD%E4%B8%8E%E8%AF%81%E6%98%8E%E4%B9%8B/

import random

class ShiShe:
    def OneYao(self):
        # Init
        LeftFig = [0] * 4
        RightFig = [0] * 4
        Bian = [0] * 3
        SiShi = 0
        # 0. 大衍之數五十，其用四十有九
        Yan_Num = 50
        Yan_Use = Yan_Num - 1
        
        for i in range(3):
            # 1. 分而為二以象兩
            Left = random.randint(1, Yan_Use-1)
            Right = Yan_Use - Left

            # 2. 掛一以象三，揲之以四以象四時，歸奇於扐以象閏
            Right -= 1
            LeftFig[0] = 1
            # ,
            SiShi = Left % 4
            if SiShi == 0: SiShi = 4
            Left -= SiShi
            LeftFig[1] = SiShi

            # 五歲再閏，故再扐而後掛。
            SiShi = Right % 4
            if SiShi == 0: SiShi = 4
            Right -= SiShi
            LeftFig[2] = SiShi

            Bian[i] = sum(LeftFig)
            Yan_Use = Left + Right
        
        Bian_Num = Yan_Use // 4 # 6 G-, 7 L+, 8 L-, 9 G+
        return Bian_Num
        if Bian_Num == 6:
            isPositive = 0
            isGreat = 1
        elif Bian_Num == 7:
            isPositive = 1
            isGreat = 0
        elif Bian_Num == 8:
            isPositive = 0
            isGreat = 0
        elif Bian_Num == 9:
            isPositive = 1
            isGreat = 1
        return isPositive, isGreat

    def OneGua(self, count = 6):
        Gua = []
        Bian_Count = 0
        for _ in range(count):
            Yao, Bian = self.OneYao()
            Gua.append(Yao)
            Bian_Count += Bian
        return Gua, Bian_Count

day = ShiShe()
stat = [0] * 10
stat_yao = [0] * 2
stat_bian =[0] * 2
for i in range(100000000):
    # yao, bian = day.OneYao()
    # stat_yao[yao] += 1
    # stat_bian[bian] += 1
    if i%1000000 == 0:
        print(i)
    yao = day.OneYao()
    stat[yao] += 1

print('RawYao', stat)
print('Yao', stat_yao)
print('Bian', stat_bian)