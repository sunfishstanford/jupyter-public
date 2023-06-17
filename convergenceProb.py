import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


numn=100
numomega=100
xval = np.array(range(1,numomega+1))
omega = np.zeros((numomega,numn)) # 100 sample points, each has an error value for one of numn n_t values
factor = np.array([np.exp(-x/numomega) for x in range(numomega)])

for i in range(omega.shape[0]):
    omega[i,0]=np.random.rand()
omega[:,0]=-np.sort(-omega[:,0])
for j in range(1,omega.shape[1]):
    omega[:,j] = omega[:,j-1]*factor


maxf=40
gridsize = (14, 2)
fig = plt.figure(num=1, clear=True, figsize=(6, 6))
axfig = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=10)
axfig.set_ylim(bottom=0,top=1)

epsilon = 0.4
n=0
dropep = True

lepsilon, =axfig.plot([1,100],[epsilon,epsilon],marker='',color='blue')
l2, = axfig.plot(xval,omega[:,n],marker='.', linestyle='none',color='g')

wm=0
for i in range(omega.shape[0]):
    wm = i
    if omega[i,n]<epsilon:
        break
l3, = axfig.plot([wm],[omega[wm,n]],marker='o',color='purple')
tx1 = axfig.text(20, 0.9, "", fontsize = 8)

def animate(k):
    global n, dropep, epsilon
    if k==0:
        epsilon=0.4
        n=0
        dropep = True
    if dropep:
        epsilon *= 0.8
        lepsilon.set_data([1,100],[epsilon,epsilon])
        dropep = False
        wm=0
        for i in range(omega.shape[0]):
            wm = i
            if omega[i,n]<epsilon:
                break
        l3.set_data([wm],[omega[wm,n]])
        tx1.set_text(str(k)+"  Epsilon = "+'{0:.2f}'.format(epsilon)+". n = "+str(n)+"  Probability = "+'{0:.2f}'.format(wm/numomega))
    else:
        n = (n+1) % numomega
        l2.set_data(xval,omega[:,n])
        wm=0
        for i in range(omega.shape[0]):
            wm = i
            if omega[i,n]<epsilon:
                break
        l3.set_data([wm],[omega[wm,n]])
        tx1.set_text(str(k)+"  Epsilon = "+'{0:.2f}'.format(epsilon)+", n = "+str(n)+", Probability = "+'{0:.2f}'.format(wm/numomega))
        if wm/numomega < 0.1:
            dropep = True
    return lepsilon, l2, l3

ani = FuncAnimation(fig, animate, frames=maxf,
                              interval=2000, blit=True)

ani.save("convergenceProb.gif", dpi=300, writer=PillowWriter(fps=0.5))

