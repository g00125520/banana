import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
from os import path

def t_first():
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)
    z = np.cos(x**2)
    
    plt.figure(figsize=(8,4))
    plt.plot(x, y, label="$sin(x)$", color="red", linewidth=2)
    plt.plot(x, z, "b--", label="$cos(x^2$")

    plt.xlabel("Times(s)")
    plt.ylabel("volt")

    plt.title("pyplot")

    plt.ylim(-1.2, 1.2)
    plt.legend()
    plt.show()
    

def t_conf():
    from matplotlib.font_manager import fontManager
    
    #print(path.abspath(matplotlib.get_configdir()))
    #print(matplotlib.style.available)
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111)
    plt.subplots_adjust(0, 0, 1, 1, 0, 0)
    plt.xticks([])
    plt.yticks([])
    x, y = 0.05, 0.05
    fonts = [font.name for font in fontManager.ttflist 
             if path.exists(font.fname) and os.stat(font.fname).st_size>1e6]
    font = set(fonts)
    dy = (1.0 -y) / (len(fonts) // 4 + (len(fonts) % 4 != 0))

    for font in fonts:
        ax.text(x, y + dy / 2, u"中文字体", 
                    {'fontname': font, 'fontsize': 14}, 
                    transform=ax.transAxes)
        ax.text(x, y, font, {'fontsize': 12}, transform=ax.transAxes)
        x += 0.25
        if x >= 1.0:
            y += dy
            x = 0.05
    plt.show()

def t_trans():
    
    def fc1(x):
        return 0.6*x + 0.3
        
    def fc2(x):
        return 0.4*x*x + 0.1*x + 0.2
    
    def find_curve_intersects(x, y1, y2):
        d = y1 -y2
        idx = np.where(d[:-1] * d[1:] <= 0)[0]
        x1, x2 = x[idx], x[idx+1]
        d1, d2 = d[idx], d[idx+1]

        return -d1*(x2 -x1)/(d2 - d1) + x1
    
    x = np.linspace(-3, 3, 100)
    f1 = fc1(x)
    f2 = fc2(x)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(x, f1)
    ax.plot(x, f2)
    
    x1, x2 = find_curve_intersects(x, f1, f2)
    ax.plot(x1, f1(x1), "o")
    ax.plot(x2, f1(x2), "o")

    ax.fill_between(x, f1, f2, where=f1>f2, facecolor="green", alpha=0.5)

    from matplotlib import transforms
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    ax.fill_between([x1, x2], 0, 1, transform=trans, alpha=0.1 )
    
    a = ax.text(0.05, 0.95, u"直线和二次曲线", 
                transform=ax.transAxes,
                verticalalignment="top",
                fontsize=18,
                bbox={"facecolor":"red", "alpha":0.4,"pad":10})
    arrow = {"arrowstyle":"fancy, tail_width=0.6", 
             "facecolor":"gray", 
             "connectionstyle": "arc3, rad=-0.3"}
    
    ax.annotate(u"交点", 
                xy = (x1, fc1(x1)),
                xycoords="data", 
                xytext=(0.05, 0.5), 
                textcoords="axes fraction", 
                arrowprops=arrow)
    
    ax.annotate(u"交点", 
                xy = (x2, fc1(x2)), 
                xycoords="data", 
                xytext=(0.05, 0.5), 
                textcoords="axes fraction",
                arrowprops=arrow)
    
    xm = (x1 + x2) / 2 
    ym = (fc1(xm) - fc2(xm))/2 + fc2(xm)

    o = ax.annotate(u"直线大于曲线区域", 
                    xy = (xm, ym), 
                    xycoords="data", 
                    xytext=(30, -30), 
                    textcoords="offset points",
                    bbox={"boxstyle":"round", "facecolor":(1.0, 0.7, 0.7), "edgecolor":"none"},
                    fontsize=16, 
                    arrowprops={"arrowstyle":"->"})

    plt.show()

if __name__ == '__main__':
    t_trans()
    
    
