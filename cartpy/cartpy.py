import pandas as pd
import numpy as np
from fuzzywuzzy import process
import pkg_resources

DATA_PATH = pkg_resources.resource_filename('cartpy', 'data/')

counties=pd.read_csv('data/counties_1872_1991.csv')

def name_to_code(name,state,year):
    df=counties[(counties['ano']==year)&(counties['estado']==state)]
    match=process.extract(name, df.nome.unique(),limit=1)[0][0]
    return df[df['nome']==match].reset_index().codigo[0]


class Municipio:
    def __init__(self,name,data=counties):
        self.name=name.title()
        self.data=data

    #search for a name in database
    def search(self,state='all',year='all',n_cases=5):
        df=self.data
        lista_states=[k for k in df.estado.unique()]+['all']
        if state not in lista_states:
            raise Exception("{} is an invalid name for state".format(state))
        elif (state=='all') & (year=='all'):
            for ano in df.ano.unique():
                df_year=df[df['ano']==ano]
                search_dict={}
                matches=[k[0] for k in process.extract(self.name, df_year.nome.unique(),limit=n_cases)]
                for match in matches:
                    search_dict.update({match:list(df_year[df_year['nome']==match].estado.unique())})
                print("{}".format(ano))
                for county,state in search_dict.items():
                    print(county +': ',state)   
        elif (state=='all'):
            df_year=df[df['ano']==year]
            search_dict={}
            matches=[k[0] for k in process.extract(self.name, df_year.nome.unique(),limit=n_cases)]
            for match in matches:
                search_dict.update({match:list(df_year[df_year['nome']==match].estado.unique())})
            print("{}".format(year))
            for county,state in search_dict.items():
                print(county +': ',state)
        else:
            df_year=df[(df['ano']==year)&(df['estado']==state)]
            search_dict={}
            matches=[k[0] for k in process.extract(self.name, df_year.nome.unique(),limit=n_cases)]
            for match in matches:
                search_dict.update({match:list(df_year[df_year['nome']==match].estado.unique())})
            print("{}".format(year))
            for county,state in search_dict.items():
                print(county +': ',state)

    #get county code
    def get_code(self,state,year):
        df=self.data
        lista_counties=list(df.nome.unique())
        lista_states=list(df.estado.unique())
        lista_years=list(df.ano.unique())
        if self.name not in lista_counties:
            raise Exception("{} is an invalid name for a county. Use search() method to find the rightly spelled countie's name ".format(self.name))
        elif state not in lista_states:
            raise Exception("{} is an invalid name for a state".format(state))
        elif year not in lista_years:
            raise Exception("{} is an invalid entry for year".format(year))
        else:
            data_code = df[(df['nome']==self.name)&(df['estado']==state)&(df['ano']==year)].reset_index()
            if data_code.shape[0]>1:
                print("There are more than one county with this informations")
            else:
                return data_code.codigo[0]
    #methods to be create                
    # def all_names(self)
    # def plot(self)
    # def get_geodata(self)


if __name__ == '__main__':
    #self-test code
    jf=Municipio('Juiz de Fora')
    # print(    jf.search(state='MG',year=1991))
    print(jf.get_code(year=1991,state='MG'))