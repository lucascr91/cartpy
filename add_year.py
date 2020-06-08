import pandas as pd                                                                                                                                          
from geobr import read_municipality
import sys
from colorama import Fore,Style

try:
    sys.argv[1]
except:
    raise  ValueError(Fore.RED+"Please inform the year"+Style.RESET_ALL)

ano=int(sys.argv[1])
df=pd.read_csv('/home/lucas/projects/cartpy/cartpy/data/counties_1872_1991.csv')                                                                             
mun = read_municipality(code_muni="all", year=ano)                                                                                                          
mun.columns=['codigo','nome','estado_code','estado','geometry']                                                                                              
mun['ano']=ano                                                                                                                                              
new=df.append(mun)                                                                                                                                           
new['nome']=[k.title().replace('ç','c').replace('ã','a').replace('á','a').replace('à','a').replace('â','a')\
    .replace('ẽ','e').replace('é','e').replace('è','e').replace('ê','e').replace('ĩ','i').\
        replace('í','i').replace('ì','i').replace('î','i').replace('õ','o').replace('ó','o').\
            replace('ò','o').replace('ô','o').replace('ũ','u').replace('ú','u').\
                replace('ù','u').replace('û','u')\
       if isinstance(k,str) else k for k in new['nome']]

new.to_csv('/home/lucas/projects/cartpy/cartpy/data/counties_1872_1991.csv',index=False)

print("The year {} was added successfully".format(ano))