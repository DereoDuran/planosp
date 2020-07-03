import json
import pandas as pd
from datetime import datetime
from datetime import timedelta

def toggleDate(date):
    if isinstance(date, str):
        return datetime.strptime(date, '%Y-%m-%d')
    else:
        return datetime.strftime(date, '%Y-%m-%d')

class Dashboard():

    def __init__(self, db):
        self.db = db

    def getKPIs(self, date, drs_list = None):

        if isinstance(drs_list, str):
            drs_list = [drs_list]

        if not drs_list:
            drs_list = [x for x in self.db.keys()]

        kpi_list = []

        for drs in drs_list:
            kpi_list.append(self.getKPI(date, drs))

        if not isinstance(date, str):
            date = toggleDate(date)

        return {date:{i:v for i,v in kpi_list}}

    def getKPI(self, date, drs):
        
        if not date in self.db[drs]:
            return [drs, 'Not found']

        info = self.db[drs][date]

        indicador_internacoes = self.getInternacoes(info)
        indicador_ocupacao_de_leitos = self.getOcupacao(date, drs)
        indicador_total_de_leitos = self.getTotalDeLeitos(info)
        indicador_casos = self.getCasos(date, drs)
        indicador_obitos = self.getObitos(date, drs)
        
        try:
            fase_capacidade_sistema = int((4*indicador_ocupacao_de_leitos['indicador'] + indicador_total_de_leitos['indicador'])/5)
        except:
            fase_capacidade_sistema = 'Erro'
        try:
            fase_evolucao_da_pandemia = int((indicador_internacoes['indicador']*3+indicador_casos['indicador']+indicador_obitos['indicador'])/5)
        except:
            fase_evolucao_da_pandemia = 'Erro'
        try:
            fase_final = min(fase_capacidade_sistema, fase_evolucao_da_pandemia)
        except:
            fase_final = 'Erro'


        return [drs, {
            'ocupacao_de_leitos': indicador_ocupacao_de_leitos,
            'total_de_leitos': indicador_total_de_leitos,
            'internacoes': indicador_internacoes,
            'casos': indicador_casos,
            'obitos': indicador_obitos,
            'fase': {
                'fase_capacidade_sistema': fase_capacidade_sistema,
                'fase_evolucao_da_pandemia': fase_evolucao_da_pandemia,
                'fase_final': fase_final,
            }
        }]

    def getInternacoes(self, info):
        try:
            antes = info['internacoes7d_l']
            depois = info['internacoes7d']

            if antes == 0:
                var = 'NaN'
                Ni = 1
            else:
                var = depois/antes
                if var >= 1.5:
                    Ni = 1
                elif var >= 1:
                    Ni = 2
                elif var >= 0.5:
                    Ni = 3
                else:
                    Ni = 4
            return {
                'antes': antes,
                'depois': depois,
                'var': var,
                'indicador': Ni
            }
        except:
            return 'Erro'

    def getTotalDeLeitos(self, info):
        try:
            total_leitos_uti = float(info['total_uti_mm7d'].replace(',','.'))
            populacao = int(info['pop'])

            leitos_por_100k = 100000*total_leitos_uti/populacao

            if leitos_por_100k >= 5:
                indicador = 4
            elif leitos_por_100k >= 3:
                indicador = 2
            else:
                indicador = 1
            return {
                'total_leitos_uti': total_leitos_uti,
                'populacao': populacao,
                'leitos_por_100k': leitos_por_100k,
                'indicador': indicador
            }
        except:
            print(info)
            return 'Erro'

    def getCasos(self, data, drs):

        try:
            data = toggleDate(data)
            casos_semana = sum(self.db[drs][toggleDate(data-timedelta(x))]['casos_novos'] for x in range(7))
            casos_semana_anterior = sum(self.db[drs][toggleDate(data-timedelta(x))]['casos_novos'] for x in range(7,14))

            if casos_semana_anterior == 0:
                var = 'NaN'
                if casos_semana == 0:
                    indicador = 0
                else:
                    indicador = 1
            else:
                var = casos_semana/casos_semana_anterior
                if var >= 2:
                    indicador = 1
                elif var >= 1:
                    indicador = 3
                else:
                    indicador = 4
            return {
                'casos_semana': casos_semana,
                'casos_semana_anterior': casos_semana_anterior,
                'var': var,
                'indicador': indicador
            }
        except:
            return 'Erro'

    def getObitos(self, data, drs):

        try:
            data = toggleDate(data)
            obitos_semana = sum(self.db[drs][toggleDate(data-timedelta(x))]['obitos_novos'] for x in range(7))
            obitos_semana_anterior = sum(self.db[drs][toggleDate(data-timedelta(x))]['obitos_novos'] for x in range(7,14))

            if obitos_semana_anterior == 0:
                var = 'NaN'
                if obitos_semana == 0:
                    indicador = 0
                else:
                    indicador = 1
            else:
                var = obitos_semana/obitos_semana_anterior
                if var >= 2:
                    indicador = 1
                elif var >= 1:
                    indicador = 2
                elif var >= 0.5:
                    indicador = 3
                else:
                    indicador = 4
            return {
                'obitos_semana': obitos_semana,
                'obitos_semana_anterior': obitos_semana_anterior,
                'var': var,
                'indicador': indicador
            }
        except:
            return 'Erro'

    def getOcupacao(self, data, drs):

        var = None

        dic = {}

        dic['2020-06-25'] = {
            'DRS 02 Araçatuba': 47.2,
            'DRS 03 Araraquara': 36.3,
            'DRS 04 Baixada Santista': 58.6,
            'DRS 05 Barretos': 71.6,
            'DRS 06 Bauru': 52.5,
            'DRS 07 Campinas': 75.2,
            'DRS 08 Franca': 69.9,
            'DRS 09 Marília': 34.8,
            'DRS 10 Piracicaba': 66.3,
            'DRS 11 Presidente Prudente': 59.8,
            'DRS 12 Registro': 26.5,
            'DRS 13 Ribeirão Preto': 78.0,
            'DRS 14 São João da Boa Vista': 40.7,
            'DRS 15 São José do Rio Preto': 44.8,
            'DRS 16 Sorocaba': 75.5,
            'DRS 17 Taubaté': 52.0,
            'Estado de São Paulo': 65.5,
            'Grande SP Leste': 64.6,
            'Grande SP Norte': 59.6,
            'Grande SP Oeste': 70.3,
            'Grande SP Sudeste': 64.2,
            'Grande SP Sudoeste': 57.0,
            'Município de São Paulo': 69.4,
        }

        dic['2020-06-18'] = {
            'DRS 02 Araçatuba': 39,
            'DRS 03 Araraquara': 35,
            'DRS 04 Baixada Santista': 61,
            'DRS 05 Barretos': 68,
            'DRS 06 Bauru': 53,
            'DRS 07 Campinas': 72,
            'DRS 08 Franca': 47,
            'DRS 09 Marília': 33,
            'DRS 10 Piracicaba': 60,
            'DRS 11 Presidente Prudente': 63,
            'DRS 12 Registro': 17,
            'DRS 13 Ribeirão Preto': 75,
            'DRS 14 São João da Boa Vista': 35,
            'DRS 15 São José do Rio Preto': 40,
            'DRS 16 Sorocaba': 75,
            'DRS 17 Taubaté': 54,
            'Estado de São Paulo': 67,
            'Grande SP Leste': 67,
            'Grande SP Norte': 65,
            'Grande SP Oeste': 71,
            'Grande SP Sudeste': 66,
            'Grande SP Sudoeste': 66,
            'Município de São Paulo': 72,
        }

        dic['2020-06-08'] = {
            'DRS 02 Araçatuba': 24,
            'DRS 03 Araraquara': 34,
            'DRS 04 Baixada Santista': 70,
            'DRS 05 Barretos': 27,
            'DRS 06 Bauru': 56,
            'DRS 07 Campinas': 69,
            'DRS 08 Franca': 48,
            'DRS 09 Marília': 21,
            'DRS 10 Piracicaba': 63,
            'DRS 11 Presidente Prudente': 52,
            'DRS 12 Registro': 31,
            'DRS 13 Ribeirão Preto': 60,
            'DRS 14 São João da Boa Vista': 24,
            'DRS 15 São José do Rio Preto': 34,
            'DRS 16 Sorocaba': 68,
            'DRS 17 Taubaté': 50,
            'Estado de São Paulo': 69,
            'Grande SP Leste': 74,
            'Grande SP Norte': 78,
            'Grande SP Oeste': 73,
            'Grande SP Sudeste': 68,
            'Grande SP Sudoeste': 78,
            'Município de São Paulo': 78,
        }

        if isinstance(data, str):
            data = toggleDate(data)

        datas_disponiveis = [toggleDate(x) for x in dic.keys()]
        if data in datas_disponiveis:
            var = dic[toggleDate(data)][drs]
        else:
            min_list = [x for x in datas_disponiveis if x < data]
            if len(min_list) == 0:
                var = dic[toggleDate(min(datas_disponiveis))][drs]
            else:
                min_date = max(min_list)

            max_list = [x for x in datas_disponiveis if x > data]
            if len(max_list) == 0:
                var = dic[toggleDate(max(datas_disponiveis))][drs]
            else:
                max_date = min(max_list)

            if not var:
                date_range = (max_date - min_date).days
                position = (data - min_date).days
                var_range = dic[toggleDate(max_date)][drs] - dic[toggleDate(min_date)][drs]
                var = dic[toggleDate(min_date)][drs] + var_range*position/date_range

        if var >= 80:
            indicador = 1
        elif var >= 70:
            indicador = 2
        elif var >= 60:
            indicador = 3
        else:
            indicador = 4
        return {
            'ocupacao_leitos_uti': var,
            'indicador': indicador
        }

if __name__ == '__main__':

    with open('./data/db.json') as f:
        db = json.load(f)

    dash = Dashboard(db)

    date = toggleDate('2020-05-19')
    max_date = max(toggleDate(x) for x in db['Estado de São Paulo'].keys())
    
    info = []

    while date <= max_date:

        info.append(dash.getKPIs(toggleDate(date)))
        date += timedelta(1)

    with open('data/kpi.json', 'w') as f:
        json.dump(info, f)