import numpy as np
import matplotlib.pyplot as plt

def random(nr):
    buy,sell=0,0
    num = np.random.normal(0,3,size=(nr,1))
    for i in num:
        if i > 0:
            buy+=1
        elif i < 0:
            sell+=1

    dr = buy-sell
    return dr

def momentum(d,labuda,nm,nr):
    num=d/(nr**0.5)
    if num >= labuda:
        dm = nm
    elif num <= -labuda:
        dm = -nm
    else:
        dm = 0
    return dm

nm = 30
nr = 100
labuda=40
lnp=0
dr = random(nr)
n_lnp=lnp+dr
d=dr
arry_lnp=[0,n_lnp]

for i in range(59998):
    dm = momentum(d,labuda,nm,nr)
    dr = random(nr)
    d=dr+dm
    n_lnp = n_lnp + d
    arry_lnp.append(n_lnp)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
plt.plot(arry_lnp,'r-',label='line 1',linewidth=1)
plt.xlabel('days')
plt.ylabel('Ln(price/P0)')
plt.savefig('pic.png')
