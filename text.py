import pandas as pd
import numpy as np
from k import theory
import matplotlib.pyplot as plt

chunker = pd.read_csv('SZ#300003.csv')
price = chunker['p']
def popp(price,precision = 21):
    pre_month = 0
    counter = 0
    popp = 0
    for i in range(0,len(price)-1,precision):
            counter+=1
            new_price=price[i]
            if float(new_price) < float(pre_month) :
                popp += 1

            pre_month = new_price
    return popp/counter

def caculate_k(price,precision = 21):
    p0 = float(price[0])
    s_k_s = 0
    s_v_s = 0
    counter = 0
    s_all = 0

    for i in range(1, len(price) - 1, precision):
        price2 = float(price[i])
        s = np.log(price2/p0)
        s_all += s
        p0 = price2
        counter += 1
    u = s_all/counter
    p0 = float(price[0])

    for n in range(1,len(price)-1,precision):
        price1 = float(price[n])
        s = np.log(price1/p0)
        s_k = (s-u)**4
        s_v = (s-u)**2
        s_k_s += s_k
        s_v_s += s_v
        p0 = price1
    k=(s_k_s/(np.sqrt(s_v_s)**4))*counter
    return k


def chick_p( check_num, arry):
    alpha = []
    lmd = []
    len_arry = len(arry)
    for i in range(0, len_arry):
        p = arry[i][0]
        if p <= check_num+0.001 and p >= check_num-0.001:
            alpha.append(round(arry[i][1][0],3))
            lmd.append(round(arry[i][1][1],3))
    return alpha, lmd

def chick_k(check_num,arry):

    alpha = []
    lmd = []
    len_arry = len(arry)
    for i in range(0, len_arry):
        k = arry[i][0]
        if k <= check_num+0.08 and k >= check_num-0.08:
            alpha.append(round(arry[i][1][0],3))
            lmd.append(round(arry[i][1][1],3))
    return alpha, lmd

z=[]
p = popp(price)
k = caculate_k(price)
print(k,p)
draw = theory(k,p)
k_reslt = draw.result_k()
k_alpha,k_lmd = chick_k(k,k_reslt)
p_result = draw.result_p()
p_alpha,p_lmd = chick_p(p,p_result)
for i in range(len(p_alpha)):
   if p_alpha[i] in k_alpha:
       for n in range(len(p_lmd)):
           if p_lmd[n] in k_lmd:
               al = []
               lm = []
               alm = []
               al.append(p_alpha[i])
               lm.append(p_lmd[n])
               alm.append(al)
               alm  .append(lm)
               z.append(alm)
print('min:',min(z))
plt.figure(figsize=(7, 7))
plt.plot(k_alpha, k_lmd,'k.', color='b', label=k)
plt.plot(p_alpha, p_lmd, color='r', label=p)
plt.legend(loc='best')
plt.grid(True)
plt.xlim([0, 8])
plt.ylim([0, 5])
plt.title('Real')
plt.xlabel('Alpha')
plt.ylabel('Lambda')
plt.savefig('SZ#300003    _21.png')
plt.show()
