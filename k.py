import numpy as np
import scipy.integrate as sci
import matplotlib.pyplot as plt

class theory(object):

    ###precision是alpha与lmd每次增长的的值,默认0.03###
    ###c_precision是k时的取值范围应与###draw_k(self)###中for循环中i取值间隔相同默认为3###
    ###len_alpha, len_lmd是求k的两个轴区间,默认为8,5####

    def __init__(self,k_num=3.19,p_num=0.06,precision = 0.03,c_precision = 3,len_alpha=8,len_lmd=5):
        self.p_num = p_num
        self.len_alpha = len_alpha
        self.len_lmd = len_lmd
        self.k_num = k_num
        self.precision = precision
        self.c_precision = c_precision

    def f(self,x):
        return (1 / (np.sqrt(2 * np.pi))) * (np.e ** (-(x ** 2) / 2))


    def pin(self,alpha, lmd):
        # p(act -> inact)#
        a = -lmd - alpha
        b = lmd - alpha
        c = -lmd + alpha
        d = lmd + alpha
        p1 = sci.romberg(self.f, a, b)
        p2 = sci.romberg(self.f, c, d)
        p = 0.5 * p1 + 0.5 * p2
        return p


    def pact(self,lmd):
        # p(inact -> act)#
        p1 = sci.quad(self.f, -np.inf, -lmd)[0]
        p2 = sci.quad(self.f, lmd, np.inf)[0]
        p = 0.5 * p1 + 0.5 * p2
        return p


    def tact(self,alpha, lmd):
        con = self.pact(lmd) / (self.pact(lmd) + self.pin(alpha, lmd))
        return con


    def tin(self,alpha, lmd):
        con = self.pin(alpha, lmd) / (self.pin(alpha, lmd) + self.pact(lmd))
        return con


    def k(self,alpha, lmd):
        top = (alpha ** 4 + 6 * alpha ** 2 + 3) * self.tact(alpha, lmd) + 3 * self.tin(alpha, lmd)
        down = ((alpha ** 2 + 1) * self.tact(alpha, lmd) + self.tin(alpha, lmd)) ** 2
        k = top / down
        return k


    def result_k(self):

        arry = []
        lmd = 0
        while lmd <= self.len_lmd:
            alpha = 0
            while alpha <= self.len_alpha:
                k_arry = []
                xy_arry = []
                result = self.k(alpha, lmd)
                new_result = round(result, 2)
                k_arry.append(new_result)
                xy_arry.append(alpha)
                xy_arry.append(lmd)
                k_arry.append(xy_arry)
                arry.append(k_arry)
                alpha += self.precision
            lmd += self.precision
            print(lmd/self.len_lmd*100,'%')
        return arry


    def chick_k(self, check_num,arry):

        low_check = check_num - self.c_precision
        high_chick = check_num + self.c_precision
        alpha = []
        lmd = []
        len_arry = len(arry)
        for i in range(0, len_arry):
            k = arry[i][0]
            if k <= high_chick and k >= low_check:
                alpha.append(arry[i][1][0])
                lmd.append(arry[i][1][1])
        return alpha, lmd


    def draw_k(self):

        arry = self.result_k()
        plt.figure(figsize=(7, 7))
        colors = ['w','b', 'c', 'g', 'r', 'm']
        for i in range(0, 16, self.c_precision):
            new_k = self.k_num + i
            alpha, lmd = self.chick_k(new_k,arry)
            plt.plot(alpha, lmd, 'k.', color=colors[int(i / self.c_precision)], label=str(round(new_k, 2)))
        plt.legend(loc='best')
        plt.grid(True)
        plt.xlim([0, 8])
        plt.ylim([0, 5])
        plt.title('K')
        plt.xlabel('Alpha')
        plt.ylabel('Lambda')
        plt.savefig('t.png')
        plt.show()

    def p0(self,alpha,lmd):
        r =  sci.quad(self.f, alpha, np.inf)[0]
        p0 = self.tin(alpha,lmd)*(1-self.pact(lmd))*0.5+self.tin(alpha,lmd)*self.pact(lmd)*r+0.5*self.tact(alpha,lmd)*self.pin(alpha,lmd)+r*self.tact(alpha,lmd)*(1-self.pin(alpha,lmd))
        return p0

    def result_p(self):
        arry = []
        lmd = 0
        while lmd <= self.len_lmd:
            alpha = 0
            while alpha <= self.len_alpha:
                p0_arry = []
                xy_arry = []
                result = self.p0(alpha, lmd)
                new_result = round(result, 3)
                p0_arry.append(new_result)
                xy_arry.append(alpha)
                xy_arry.append(lmd)
                p0_arry.append(xy_arry)
                arry.append(p0_arry)
                alpha += self.precision
            lmd += self.precision
            print(lmd / self.len_lmd * 100, '%')
        return arry

    def chick_p(self,check_num,arry):
        low_check = check_num - 0.05
        high_chick = check_num + 0.05
        alpha = []
        lmd = []
        len_arry = len(arry)
        for i in range(0, len_arry):
            q = arry[i][0]
            if q <= high_chick and q >= low_check:
                alpha.append(arry[i][1][0])
                lmd.append(arry[i][1][1])
        return alpha, lmd

    def draw_p(self):
        arry = self.result_p()
        plt.figure(figsize=(7, 7))
        colors = ['silver', 'b', 'c', 'g', 'yellow', 'r','violet','m','k','w']
        for i in range(0, 10):
            new_p = self.p_num + 0.05*i
            alpha, lmd = self.chick_p(new_p, arry)
            plt.plot(alpha, lmd, 'k.', color=colors[i], label=str(round(new_p, 3)))
        plt.legend(loc='best')
        plt.grid(True)
        plt.xlim([0, 8])
        plt.ylim([0, 5])
        plt.title('1-p_opp')
        plt.xlabel('Alpha')
        plt.ylabel('Lambda')
        plt.savefig('p.png')
        plt.show()