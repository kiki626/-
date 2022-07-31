import random
import time
MAX = 2 ** 32
vi = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
t = [0x79cc4519, 0x7a879d8a]

def Int2Bin(a, k):
    res = list(bin(a)[2:])      #把整数a转化为二进制列表
    return ''.join(['0'] * (k - len(res)) + res)    #在a的二进制列表前补0补到k位，返回字符串


def LoopLeftShift(a, k):
    res = list(Int2Bin(a, 32))      #得到整数a的32位列表
    return int(''.join(res[k:] + res[:k]), 2)       #左移k位，返回整数

def fillFunction(message):      #信息填充
    message = bin(message)[2:] 
    length = len(message)
    message = '0' * (length % 4) + message
    k = (448 - length - 1) % 512
    message += '1' + '0' * k + Int2Bin(length, 64)
    return message

def IterFunction(message):      #消息分组
    n = int(len(message) / 512)
    v = []
    v.append(Int2Bin(vi, 256))
    for i in range(n):
        w, w1 = msgExten(message[512 * i:512 * (i + 1)])
        temp = CF(v[i], message[512 * i:512 * (i + 1)], w, w1)
        temp = Int2Bin(temp, 256)
        v.append(temp)
    return v[n]


def msgExten(b):
    w = []
    w1 = []
    for i in range(16):
        temp = b[i * 32:(i + 1) * 32]
        w.append(int(temp, 2))
    for j in range(16, 68, 1):
        factor1 = LoopLeftShift(w[j - 3], 15)
        factor2 = LoopLeftShift(w[j - 13], 7)
        factor3 = P1(w[j - 16] ^ w[j - 9] ^ factor1)
        factor4 = factor3 ^ factor2 ^ w[j - 6]
        w.append(factor4)
    for j in range(64):
        factor1 = w[j] ^ w[j + 4]
        w1.append(factor1)
    return w, w1

def un(a):      #二进制码取补码
    return 2**32 - 1 - a

def P0(X):
    return X ^ LoopLeftShift(X, 9) ^ LoopLeftShift(X, 17)

def P1(X):
    return X ^ LoopLeftShift(X, 15) ^ LoopLeftShift(X, 23)

def T(j):
    if j <= 15:
        return t[0]
    else:
        return t[1]

def FF(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)


def GG(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (un(X) & Z)




def CF(vi, bi, w, w1):      #压缩函数
    A = []
    for i in range(8):
        temp = vi[32 * i:32 * (i + 1)]
        A.append(int(temp, 2))
    for j in range(64):
        factor1 = LoopLeftShift(A[0], 12)
        factor2 = LoopLeftShift(T(j), j % 32)
        SS1 = LoopLeftShift((factor1 + A[4] + factor2) % MAX, 7)
        factor3 = LoopLeftShift(A[0], 12)
        SS2 = SS1 ^ factor3
        TT1 = (FF(A[0], A[1], A[2], j) + A[3] + SS2 + w1[j]) % MAX
        TT2 = (GG(A[4], A[5], A[6], j) + A[7] + SS1 + w[j]) % MAX
        A[3] = A[2]
        A[2] = LoopLeftShift(A[1], 9)
        A[1] = A[0]
        A[0] = TT1
        A[7] = A[6]
        A[6] = LoopLeftShift(A[5], 19)
        A[5] = A[4]
        A[4] = P0(TT2)
    temp = Int2Bin(A[0], 32) + Int2Bin(A[1], 32) + Int2Bin(A[2], 32) + \
           Int2Bin(A[3], 32) + Int2Bin(A[4], 32) + Int2Bin(A[5], 32) + \
           Int2Bin(A[6], 32) + Int2Bin(A[7], 32)
    temp = int(temp, 2)
    return temp ^ int(vi, 2)

def SM3(msg):
    msg_1=fillFunction(msg)
    hex(int(msg_1,2))
    res=IterFunction(msg_1)
    result=hex(int(res,2))
    return result[2:]

def Birthday_Attck(n):
    print("开始Birthday_Attck")
    for i in range(2**(int(n))):
        a1=random.randint(0,2**n)
        a2 = random.randint(0,2**n)
        if(SM3(a1)[:int(n/4)]==SM3(a2)[:int(n/4)]):
            print('攻击成功')
            print(a1,'和',a2,'的hash为',SM3(a1)[:int(n/4)])
            return
    print('攻击失败')

def Rho_Attck(n):
    print("开始Rho_Attck")
    msg = random.randint(0, 0xffffff)
    res = []
    for i in range(0xffffff):
        res.append(SM3(msg)[:n // 4])
        msg = (2 * msg + 1)
        if SM3(msg)[:n // 4] in res:
            print("攻击成功")
            print('碰撞成功的msg为',msg)
            return
    print("攻击失败")

if __name__ == '__main__':
    time_start = time.time()
    Birthday_Attck(16)
    time_end = time.time()
    time_c = time_end - time_start
    print('耗时', time_c, 's')

    time_start = time.time()
    Rho_Attck(16)
    time_end = time.time()
    time_c = time_end - time_start
    print('耗时', time_c, 's')

