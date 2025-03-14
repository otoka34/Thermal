import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load
from datetime import datetime,timedelta,timezone
import soldir

def beta_cal(es,i,o,os):
    b = np.arcsin(np.cos(es)*np.sin(i)*np.sin(o-os)+np.sin(es)*np.cos(i))
    b2 = np.degrees(b)
    return(b2)

def sunlight(beta,re,h):
    beta = np.abs(np.radians(beta))
    beta_asc = np.arcsin(re/(re+h))
    if beta >= beta_asc:
        print(beta_asc)
        sun = 1
    else:
        theta = np.pi - np.arcsin(np.sqrt(1/(np.cos(beta)**2)*((re/(re+h))**2-np.sin(beta)**2)))
        sun = theta/np.pi
    return sun


#グラフの準備
x = []
y1 = []
y2 = []

#日時の設定
now = datetime.utcnow().date()

N = 365
for n in range(0, N, 1):
    
    dt = datetime.combine(now,datetime.min.time())
    utc = dt.strftime("%Y-%m-%d") + "T12:00:00"
    now = now + timedelta(days=1)

    # 赤経と赤緯の計算
    result = soldir.soldir(utc)
    ra = result[0]
    dec = result[1]

    #定義
    os = ra #赤経
    es = dec #赤緯
    

    i = np.radians(51.6) #軌道傾斜角
    j2 =  1082.62*pow(10,-6) #扁球摂動定数
    h = 408
    re =  6378.1
    r = h + re #地球の中心と衛星の距離
    gm = 0.3986*pow(10,6) #地球の重力定数

    omega = -(3/2)*j2*((re/r)**2)*np.sqrt(gm/(r**3))*np.cos(i) #昇光点赤経の変化率

    o = -omega*n*60*60*24 #昇光点赤経（初期値は0）
    
    beta = beta_cal(es,i,o,os)
    sun = sunlight(beta,re,h)

    x.append(n)
    y1.append(beta)
    y2.append(sun)

    
#plt.plot(x,y1)
#plt.title('Beta Angle Variation')
#plt.xlabel('date')
#plt.ylabel('beta angle')

plt.plot(x,y2)
plt.title('Sunlight')
plt.xlabel('date')
plt.ylabel('sunlight')
plt.show()