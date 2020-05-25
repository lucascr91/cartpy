import pandas as pd
import numpy as np
from fuzzywuzzy import process
import pkg_resources
import geopandas as gpd
from shapely.wkt import loads
import matplotlib.pyplot as plt
from descartes import PolygonPatch

DATA_PATH = pkg_resources.resource_filename('cartpy', 'data/')
DB_FILE = pkg_resources.resource_filename('cartpy', 'data/counties_1872_1991.csv')

counties=pd.read_csv(DB_FILE)
counties['estado_code']=pd.to_numeric(counties['estado_code'],errors='coerce')

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
            try:
                data_code = df[(df['nome']==self.name)&(df['estado']==state)&(df['ano']==year)].reset_index()
            except:
                print("This combination of countie, state and year doesn't exist")
            if data_code.shape[0]>1:
                print("There are more than one county with this combination of countie, state and year")
            else:
                return data_code.codigo[0]

    #List all names that share the same code
    def all_names(self,state,year,show=True):
        try:
            mun_code=self.get_code(state=state,year=year)
        except:
            raise Exception("There is no {} in the state {} and the year {}. Use the search method or get_dictionary to find the right name".format(self.name,state,year))
        df=self.data
        cases_index=[k for k in df[df['codigo']==mun_code].index]
        if show:
            for i in cases_index:
                print(df['ano'][i],': ',df['nome'][i])
        else:
            dict_nameyears={df['ano'][i]:df['nome'][i] for i in cases_index}
            return dict_nameyears

    #countie map
    def get_map(self,state,year):
        df=self.data
        user_year=Year(year=year)
        sf4=user_year.get_geodata(state=state,county=self.name)
        sf4.plot(figsize=(20,10), color='royalblue', edgecolor='k')
        plt.title('{}-{}\n{}'.format(self.name,state,year), fontsize=20)
        plt.show()
    #compare maps between years
    def compare(self,years,state,fillcolor1='w',fillcolor2='r', edgecolor1='k', edgecolor2='r',size=(20,10)):
        if (isinstance(years,list)) & (len(years)==2):
            try:
                mun_code=self.get_code(state=state,year=years[1])
            except:
                raise Exception("There is no {} in year {}. Use the search method or get_dictionary to find the right name".format(self.name,years[1]))
            sf1=Year(years[0]).get_geodata(state=state,county=mun_code)
            sf2=Year(years[1]).get_geodata(state=state,county=mun_code)
            fig, ax = plt.subplots(figsize=size)
            poly1= sf1.reset_index()['geometry'][0]
            ax.add_patch(PolygonPatch(poly1, fc=fillcolor1, ec=edgecolor1, alpha=1, zorder=2,label=str(years[0])))
            ax.axis('scaled')
            poly2= sf2.reset_index()['geometry'][0]
            ax.add_patch(PolygonPatch(poly2, fc=fillcolor2,ec=edgecolor2, alpha=0.3, zorder=2, label=str(years[1])))
            ax.axis('scaled')
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    fancybox=True, shadow=True, ncol=2)
            plt.show()
        else:
            raise Exception("years must be a list with 2 elements")

class Year:
    def __init__(self,year,data=counties):
        self.year=year
        self.data=data
    # get geopandas dataframe
    def get_geodata(self,state='all',county='all'):
        df=self.data
        df=df[df['ano']==self.year]
        #user entry two strings
        if (isinstance(state,str)) & (isinstance(county,str)):
            lista_states=[k for k in df.estado.unique()]+['all']
            lista_counties=[k for k in df.nome.unique()]+['all']
            if state not in lista_states:
                raise Exception("{} is an invalid name for state".format(state))
            elif county not in lista_counties:
                raise Exception("{} is an invalid name for a county. Use search() method to find the rightly spelled countie's name ".format(county))
            elif state=='all':
                sf_data = gpd.GeoDataFrame(df)
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
            elif (state!='all') & (county=='all'):
                sf_data = gpd.GeoDataFrame(df[df['estado']==state])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
            elif (state!='all') & (county!='all'):
                sf_data = gpd.GeoDataFrame(df[(df['estado']==state)&(df['nome']==county)])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
        #user entry state code and countie string
        elif (not isinstance(state,str)) & (isinstance(county,str)):
            lista_states=[k for k in df.estado_code.unique()]
            lista_counties=[k for k in df.nome.unique()]+['all']
            if state not in lista_states:
                raise Exception("{} is an invalid code for state".format(state))
            elif county not in lista_counties:
                raise Exception("{} is an invalid name for a county. Use search() method to find the rightly spelled countie's name ".format(county))
            elif county=='all':
                sf_data = gpd.GeoDataFrame(df[df['estado_code']==state])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
            elif county!='all':
                sf_data = gpd.GeoDataFrame(df[(df['estado_code']==state)&(df['nome']==county)])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
        #user entry state string and countie code
        elif (isinstance(state,str)) & (not isinstance(county,str)):
            lista_states=[k for k in df.estado.unique()]+['all']
            lista_counties=[k for k in df.codigo.unique()]
            if state not in lista_states:
                raise Exception("{} is an invalid name for state".format(state))
            elif county not in lista_counties:
                raise Exception("{} is an invalid name for a county. Use search() method to find the rightly spelled countie's name ".format(county))
            elif state=='all':
                sf_data = gpd.GeoDataFrame(df)
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
            elif state!='all':
                sf_data = gpd.GeoDataFrame(df[(df['estado']==state)&(df['codigo']==county)])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
        #user entry state code and countie code
        elif (not isinstance(state,str)) & (not isinstance(county,str)):
            lista_states=[k for k in df.estado_code.unique()]
            lista_counties=[k for k in df.codigo.unique()]
            if state not in lista_states:
                raise Exception("{} is an invalid name for state".format(state))
            elif county not in lista_counties:
                raise Exception("{} is an invalid name for a county. Use search() method to find the rightly spelled countie's name ".format(county))
            else:
                sf_data = gpd.GeoDataFrame(df[(df['estado_code']==state)&(df['codigo']==county)])
                sf_data['geometry'] = sf_data['geometry'].apply(lambda x: loads(x))
                return sf_data
    #get dictionary of equivalences between base year and chosen year
    def get_dictionary(self,year,state='all'):
        base=self.get_geodata(state=state)
        tocompare=Year(year).get_geodata(state=state)
        new=base.set_index('codigo').join(tocompare.set_index('codigo'),lsuffix='_base')
        new=new[~new['nome'].isna()]
        dict_names={new['nome_base'][k]:new['nome'][k] for k in new.index}

        return dict_names
    #get list of all new counties between base year and chosen year
    def get_newcounties(self,year,state='all'):
        base=self.get_geodata(state=state)
        tocompare=Year(year).get_geodata(state=state)
        new=base.set_index('codigo').join(tocompare.set_index('codigo'),lsuffix='_base')
        new=new[new['nome'].isna()]
        list_names=[new['nome_base'][k] for k in new.index]

        return list_names

if __name__ == '__main__':
    #self-test code
    jf=Municipio('Sao Carlos')
    # print(jf.search(state='SP',year=1991))
    # jf_code=jf.get_code(year=1991,state='SP')
    # print(jf.compare(years=[1872,1991], state='SP'))
    jf.all_names(state='SP',year=1991)
