import csv
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib as mpl
from pylab import *

def T(n):
    if n==0:
        return '10<'
    else:
        return n
    
h1=[]
h2=[]
h3=[]
h4=[]

apellido='Mansilla'

with open('/home/def/Descargas/apellidos_cantidad_personas_provincia.csv', 'r') as f_object:
    data = list(csv.reader(f_object))
    for data_i in data:
        if data_i[0]=="Mansilla":
            h1.append(int(data_i[1]))
            h2.append(data_i[3])
        if data_i[0]==apellido:
            h3.append(int(data_i[1]))
            h4.append(data_i[3])
    f_object.close()

R=list(set(h2)^set(h4))
Rn=np.zeros(len(R))
hh4=list(np.concatenate((h4,R)))
hh3=list(np.concatenate((h3,Rn)))

total=sum(h3)

Hn=hh3
Hs=hh4

Hs=list([('Provincia de '+i) for i in Hs])
Hs[Hs.index('Provincia de Ciudad de Buenos Aires')]='Ciudad Autónoma de Buenos Aires'
Hs[Hs.index('Provincia de Chaco')]='Provincia del Chaco'
Hs[Hs.index('Provincia de Chubut')]='Provincia del Chubut'
Hs[Hs.index('Provincia de Tierra del Fuego')]='Provincia de Tierra del Fuego, Antártida e Islas del Atlántico Sur'
Hs[Hs.index('Provincia de Neuquén')]='Provincia del Neuquén'

pais = gpd.read_file('/home/def/Descargas/Provincia/ign_provincia.shp')
fig, ax = plt.subplots()
inset_ax = ax.inset_axes([.63, .18, .3, .3])
fig.set_size_inches([7,7])

f1=[]
for str1 in pais['FNA']:
    for str2 in Hs:
        if str2==str1:
            f1.append(Hn[Hs.index(str2)])
        else:
            pass

cmap1=cm.Blues(np.array(f1)/np.mean(f1))
cmap2=list([(mpl.colors.rgb2hex(i)) for i in cmap1])
pais['color'] = cmap2

ax.set_ylim([-57,-21])
ax.set_xlim([-75,-50])
inset_ax.set_ylim([-34.75,-34.50])
inset_ax.set_xlim([-58.55,-58.30])

ax.set_xticks([])
ax.set_yticks([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

pais.plot(color=pais['color'], ax=ax, edgecolor="black", linewidth=0.3, legend=True)
pais.plot(color=pais['color'], ax=inset_ax, edgecolor="black", linewidth=0.3)

pais.apply(lambda x: ax.annotate(text=str(T(int(f1[list(pais['FNA']).index(x['FNA'])]))), xy=x.geometry.centroid.coords[0], ha='center', size=11), axis=1)
pais.apply(lambda x: inset_ax.annotate(text=str(T(int(f1[list(pais['FNA']).index(x['FNA'])]))), xy=x.geometry.centroid.coords[0], ha='center', size=12), axis=1)

ax.set_aspect('equal', adjustable='box')
inset_ax.set_aspect('equal', adjustable='box')

plt.text(-63,-55, f'Total registrado: {total}', fontsize=11)
plt.text(-59.4,-41, f'Ciudad de Buenos Aires', fontsize=8)
plt.text(-68,-54.5, T(f1[16]), fontsize=11)

plt.title(f"Distribución del apellido {apellido} (2022)")
plt.show()
