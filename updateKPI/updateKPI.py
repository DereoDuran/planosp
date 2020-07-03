import json
import pandas as pd

# Update KPI database
def updateData():

    drs_info = drsInfo()
    mun_info = munInfo()

    db = {x:{} for x in sorted(drs_info.keys())}

    # Get latest info from SEADE's github
    LEITOS_E_INTERNACOES_URL = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/plano_sp_leitos_internacoes.csv'
    leitos_e_internacoes = pd.read_csv(LEITOS_E_INTERNACOES_URL, sep=';').T

    CASOS_E_OBITOS_URL = 'https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv'
    casos_e_obitos = pd.read_csv(CASOS_E_OBITOS_URL, sep=';').T

    # Get raw indicators
    for item in leitos_e_internacoes:
        datahora, nome_drs, total_uti_mm7d, pop, leitos_pc, internacoes7d, internacoes7d_l, internacoes_7v7 = leitos_e_internacoes[item]

        db[nome_drs][datahora] = {
            'total_uti_mm7d': total_uti_mm7d,
            'pop': pop,
            'internacoes7d': internacoes7d,
            'internacoes7d_l': internacoes7d_l,
            'casos': 0,
            'casos_novos': 0,
            'obitos': 0,
            'obitos_novos': 0,
            'pop': 0,
        }

    for item in casos_e_obitos:
        nome_munic, codigo_ibge, dia, mes, datahora, casos, casos_novos, casos_pc, casos_mm7d, obitos, obitos_novos, obitos_pc, obitos_mm7d, letalidade, nome_ra, cod_ra, nome_drs, cod_drs, pop, pop_60, area, map_leg, map_leg_s, latitude, longitude, semana_epidem = casos_e_obitos[item]

        if nome_munic == 'Ignorado': continue

        if datahora in db[mun_info[nome_munic]]:
        
            dicPrev = db[mun_info[nome_munic]][datahora]
        
            dicPrev['casos'] += casos
            dicPrev['casos_novos'] += casos_novos
            dicPrev['obitos'] += obitos
            dicPrev['obitos_novos'] += obitos_novos
            dicPrev['pop'] += pop

            db[mun_info[nome_munic]][datahora] = dicPrev
    
    with open('data/db.json', 'w') as f:
        json.dump(db, f)

# Return {DRS:[List of cities]}
def drsInfo():

    drs_info = {}

    drs_info['Município de São Paulo'] = ['São Paulo']

    drs_info['Grande SP Norte'] = ['Caieiras', 'Cajamar', 'Francisco Morato', 'Franco da Rocha', 'Mairiporã']

    drs_info['Grande SP Leste'] = ['Arujá', 'Biritiba Mirim', 'Ferraz de Vasconcelos', 'Guararema', 'Guarulhos', 'Itaquaquecetuba', 'Mogi das Cruzes', 'Poá', 'Salesópolis', 'Santa Isabel', 'Suzano']

    drs_info['Grande SP Sudeste'] = ['Diadema', 'Mauá', 'Ribeirão Pires', 'Rio Grande da Serra', 'Santo André', 'São Bernardo do Campo', 'São Caetano do Sul']

    drs_info['Grande SP Sudoeste'] = ['Cotia', 'Embu das Artes', 'Embu-Guaçu', 'Itapecerica da Serra', 'Juquitiba', 'São Lourenço da Serra', 'Taboão da Serra', 'Vargem Grande Paulista']

    drs_info['Grande SP Oeste'] = ['Barueri', 'Carapicuíba', 'Itapevi', 'Jandira', 'Osasco', 'Pirapora do Bom Jesus', 'Santana de Parnaíba']

    drs_info['DRS 09 Marília'] = ['Adamantina', 'Alvinlândia', 'Assis', 'Bastos', 'Bernardino de Campos', 'Borá', 'Campos Novos Paulista', 'Chavantes', 'Cândido Mota', 'Echaporã', 'Espírito Santo do Turvo', 'Fernão', 'Flórida Paulista', 'Garça', 'Guaimbê', 'Guarantã', 'Gália', 'Herculândia', 'Iacri', 'Ibirarema', 'Inúbia Paulista', 'Ipaussu', 'Júlio Mesquita', 'Lucélia', 'Lupércio', 'Lutécia', 'Maracaí', 'Mariápolis', 'Marília', 'Ocauçu', 'Oriente', 'Oscar Bressane', 'Osvaldo Cruz', 'Ourinhos', 'Pacaembu', 'Palmital', 'Paraguaçu Paulista', 'Parapuã', 'Pedrinhas Paulista', 'Platina', 'Pompéia', 'Pracinha', 'Queiroz', 'Quintana', 'Ribeirão do Sul', 'Rinópolis', 'Sagres', 'Salmourão', 'Salto Grande', 'Santa Cruz do Rio Pardo', 'São Pedro do Turvo', 'Tarumã', 'Timburi', 'Tupã', 'Ubirajara', 'Vera Cruz', 'Álvaro de Carvalho', 'Óleo']

    drs_info['DRS 15 São José do Rio Preto'] = ['Adolfo', 'Américo de Campos', "Aparecida d'Oeste", 'Ariranha', 'Aspásia', 'Bady Bassitt', 'Bálsamo', 'Cardoso', 'Catanduva', 'Catiguá', 'Cedral', 'Cosmorama', 'Dirce Reis', 'Dolcinópolis', 'Elisiário', 'Embaúba', "Estrela d'Oeste", 'Fernando Prestes', 'Fernandópolis', 'Floreal', 'Gastão Vidigal', 'General Salgado', 'Guapiaçu', "Guarani d'Oeste", 'Ibirá', 'Icém', 'Indiaporã', 'Ipiguá', 'Irapuã', 'Itajobi', 'Jaci', 'Jales', 'José Bonifácio', 'Macaubal', 'Macedônia', 'Magda', 'Marapoama', 'Marinópolis', 'Mendonça', 'Meridiano', 'Mesópolis', 'Mira Estrela', 'Mirassol', 'Mirassolândia', 'Monte Aprazível', 'Monções', 'Neves Paulista', 'Nhandeara', 'Nipoã', 'Nova Aliança', 'Nova Granada', 'Novais', 'Novo Horizonte', 'Onda Verde', 'Ouroeste', 'Palestina', 'Palmares Paulista', "Palmeira d'Oeste", 'Paranapuã', 'Paraíso', 'Parisi', 'Paulo de Faria', 'Pedranópolis', 'Pindorama', 'Pirangi', 'Planalto', 'Poloni', 'Pontalinda', 'Pontes Gestal', 'Populina', 'Potirendaba', 'Riolândia', 'Sales', 'Santa Adélia', 'Santa Albertina', "Santa Clara d'Oeste", 'Santa Fé do Sul', 'Santa Salete', 'Santana da Ponte Pensa', 'Sebastianópolis do Sul', 'São Francisco', 'São José do Rio Preto', 'São João das Duas Pontes', 'São João de Iracema', 'Tabapuã', 'Tanabi', 'Três Fronteiras', 'Turmalina', 'Ubarana', 'Uchoa', 'União Paulista', 'Urupês', 'Urânia', 'Valentim Gentil', 'Vitória Brasil', 'Votuporanga', 'Zacarias', 'Álvares Florence']

    drs_info['DRS 14 São João da Boa Vista'] = ['Aguaí', 'Caconde', 'Casa Branca', 'Divinolândia', 'Espírito Santo do Pinhal', 'Estiva Gerbi', 'Itapira', 'Itobi', 'Mococa', 'Mogi Guaçu', 'Mogi Mirim', 'Santa Cruz das Palmeiras', 'Santo Antônio do Jardim', 'São José do Rio Pardo', 'São João da Boa Vista', 'São Sebastião da Grama', 'Tambaú', 'Tapiratiba', 'Vargem Grande do Sul', 'Águas da Prata']

    drs_info['DRS 07 Campinas'] = ['Americana', 'Amparo', 'Artur Nogueira', 'Atibaia', 'Bom Jesus dos Perdões', 'Bragança Paulista', 'Cabreúva', 'Campinas', 'Campo Limpo Paulista', 'Cosmópolis', 'Holambra', 'Hortolândia', 'Indaiatuba', 'Itatiba', 'Itupeva', 'Jaguariúna', 'Jarinu', 'Joanópolis', 'Jundiaí', 'Lindóia', 'Louveira', 'Monte Alegre do Sul', 'Monte Mor', 'Morungaba', 'Nazaré Paulista', 'Nova Odessa', 'Paulínia', 'Pedra Bela', 'Pedreira', 'Pinhalzinho', 'Piracaia', "Santa Bárbara d'Oeste", 'Santo Antônio de Posse', 'Serra Negra', 'Socorro', 'Sumaré', 'Tuiuti', 'Valinhos', 'Vargem', 'Vinhedo', 'Várzea Paulista', 'Águas de Lindóia']

    drs_info['DRS 06 Bauru'] = ['Agudos', 'Anhembi', 'Arandu', 'Arealva', 'Areiópolis', 'Avaré', 'Avaí', 'Balbinos', 'Bariri', 'Barra Bonita', 'Barão de Antonina', 'Bauru', 'Bocaina', 'Bofete', 'Boracéia', 'Borebi', 'Botucatu', 'Brotas', 'Cabrália Paulista', 'Cafelândia', 'Cerqueira César', 'Conchas', 'Coronel Macedo', 'Dois Córregos', 'Duartina', 'Fartura', 'Getulina', 'Guaiçara', 'Iacanga', 'Iaras', 'Igaraçu do Tietê', 'Itaju', 'Itaporanga', 'Itapuí', 'Itatinga', 'Itaí', 'Jaú', 'Laranjal Paulista', 'Lençóis Paulista', 'Lins', 'Lucianópolis', 'Macatuba', 'Manduri', 'Mineiros do Tietê', 'Paranapanema', 'Pardinho', 'Paulistânia', 'Pederneiras', 'Pereiras', 'Piraju', 'Pirajuí', 'Piratininga', 'Porangaba', 'Pratânia', 'Presidente Alves', 'Promissão', 'Reginópolis', 'Sabino', 'Sarutaiá', 'São Manuel', 'Taguaí', 'Taquarituba', 'Tejupá', 'Torre de Pedra', 'Torrinha', 'Uru', 'Águas de Santa Bárbara']

    drs_info['DRS 10 Piracicaba'] = ['Analândia', 'Araras', 'Capivari', 'Charqueada', 'Conchal', 'Cordeirópolis', 'Corumbataí', 'Elias Fausto', 'Engenheiro Coelho', 'Ipeúna', 'Iracemápolis', 'Itirapina', 'Leme', 'Limeira', 'Mombuca', 'Piracicaba', 'Pirassununga', 'Rafard', 'Rio Claro', 'Rio das Pedras', 'Saltinho', 'Santa Cruz da Conceição', 'Santa Gertrudes', 'Santa Maria da Serra', 'São Pedro', 'Águas de São Pedro']

    drs_info['DRS 16 Sorocaba'] = ['Alambari', 'Alumínio', 'Angatuba', 'Apiaí', 'Araçariguama', 'Araçoiaba da Serra', 'Barra do Chapéu', 'Boituva', 'Buri', 'Campina do Monte Alegre', 'Capela do Alto', 'Capão Bonito', 'Cerquilho', 'Cesário Lange', 'Guapiara', 'Guareí', 'Ibiúna', 'Iperó', 'Itaberá', 'Itaoca', 'Itapetininga', 'Itapeva', 'Itapirapuã Paulista', 'Itararé', 'Itu', 'Jumirim', 'Mairinque', 'Nova Campina', 'Piedade', 'Pilar do Sul', 'Porto Feliz', 'Quadra', 'Ribeira', 'Ribeirão Branco', 'Ribeirão Grande', 'Riversul', 'Salto', 'Salto de Pirapora', 'Sarapuí', 'Sorocaba', 'São Miguel Arcanjo', 'São Roque', 'Tapiraí', 'Taquarivaí', 'Tatuí', 'Tietê', 'Votorantim']

    drs_info['DRS 11 Presidente Prudente'] = ['Alfredo Marcondes', 'Anhumas', 'Caiabu', 'Caiuá', 'Dracena', 'Emilianópolis', 'Estrela do Norte', 'Euclides da Cunha Paulista', 'Flora Rica', 'Iepê', 'Indiana', 'Irapuru', 'João Ramalho', 'Junqueirópolis', 'Marabá Paulista', 'Martinópolis', 'Mirante do Paranapanema', 'Monte Castelo', 'Narandiba', 'Nova Guataporanga', 'Panorama', 'Paulicéia', 'Piquerobi', 'Pirapozinho', 'Presidente Bernardes', 'Presidente Epitácio', 'Presidente Prudente', 'Presidente Venceslau', 'Quatá', 'Rancharia', 'Regente Feijó', 'Ribeirão dos Índios', 'Rosana', 'Sandovalina', 'Santo Anastácio', 'Santo Expedito', "São João do Pau d'Alho", 'Taciba', 'Tarabai', 'Teodoro Sampaio', 'Tupi Paulista', 'Álvares Machado']

    drs_info['DRS 05 Barretos'] = ['Altair', 'Barretos', 'Bebedouro', 'Cajobi', 'Colina', 'Colômbia', 'Guaraci', 'Guaíra', 'Jaborandi', 'Monte Azul Paulista', 'Olímpia', 'Severínia', 'Taiaçu', 'Taiúva', 'Taquaral', 'Terra Roxa', 'Viradouro', 'Vista Alegre do Alto']

    drs_info['DRS 13 Ribeirão Preto'] = ['Altinópolis', 'Barrinha', 'Batatais', 'Brodowski', 'Cajuru', 'Cravinhos', 'Cássia dos Coqueiros', 'Dumont', 'Guariba', 'Guatapará', 'Jaboticabal', 'Jardinópolis', 'Luís Antônio', 'Monte Alto', 'Pitangueiras', 'Pontal', 'Pradópolis', 'Ribeirão Preto', 'Santa Cruz da Esperança', 'Santa Rita do Passa Quatro', 'Santa Rosa de Viterbo', 'Santo Antônio da Alegria', 'Serra Azul', 'Serrana', 'Sertãozinho', 'São Simão']

    drs_info['DRS 02 Araçatuba'] = ['Alto Alegre', 'Andradina', 'Araçatuba', 'Auriflama', 'Avanhandava', 'Barbosa', 'Bento de Abreu', 'Bilac', 'Birigui', 'Braúna', 'Brejo Alegre', 'Buritama', 'Castilho', 'Clementina', 'Coroados', 'Gabriel Monteiro', 'Glicério', 'Guararapes', 'Guaraçaí', 'Guzolândia', 'Ilha Solteira', 'Itapura', 'Lavínia', 'Lourdes', 'Luiziânia', 'Mirandópolis', 'Murutinga do Sul', 'Nova Castilho', 'Nova Luzitânia', 'Penápolis', 'Pereira Barreto', 'Rubiácea', 'Santo Antônio do Aracanguá', 'Santópolis do Aguapeí', 'Sud Mennucci', 'Suzanápolis', 'Turiúba', 'Valparaíso']

    drs_info['DRS 03 Araraquara'] = ['Américo Brasiliense', 'Araraquara', 'Boa Esperança do Sul', 'Borborema', 'Cândido Rodrigues', 'Descalvado', 'Dobrada', 'Dourado', 'Gavião Peixoto', 'Ibaté', 'Ibitinga', 'Itápolis', 'Matão', 'Motuca', 'Nova Europa', 'Porto Ferreira', 'Ribeirão Bonito', 'Rincão', 'Santa Ernestina', 'Santa Lúcia', 'São Carlos', 'Tabatinga', 'Taquaritinga', 'Trabiju']

    drs_info['DRS 17 Taubaté'] = ['Aparecida', 'Arapeí', 'Areias', 'Bananal', 'Cachoeira Paulista', 'Campos do Jordão', 'Canas', 'Caraguatatuba', 'Caçapava', 'Cruzeiro', 'Cunha', 'Guaratinguetá', 'Igaratá', 'Ilhabela', 'Jacareí', 'Jambeiro', 'Lavrinhas', 'Lorena', 'Monteiro Lobato', 'Natividade da Serra', 'Paraibuna', 'Pindamonhangaba', 'Piquete', 'Potim', 'Queluz', 'Redenção da Serra', 'Roseira', 'Santa Branca', 'Santo Antônio do Pinhal', 'Silveiras', 'São Bento do Sapucaí', 'São José dos Campos', 'São Luiz do Paraitinga', 'São Sebastião', 'Taubaté', 'Tremembé', 'Ubatuba']

    drs_info['DRS 08 Franca'] = ['Aramina', 'Buritizal', 'Cristais Paulista', 'Franca', 'Guará', 'Igarapava', 'Ipuã', 'Itirapuã', 'Ituverava', 'Miguelópolis', 'Morro Agudo', 'Nuporanga', 'Orlândia', 'Patrocínio Paulista', 'Pedregulho', 'Restinga', 'Rifaina', 'Sales Oliveira', 'São Joaquim da Barra', 'São José da Bela Vista']

    drs_info['DRS 12 Registro'] = ['Barra do Turvo', 'Cajati', 'Cananéia', 'Eldorado', 'Iguape', 'Ilha Comprida', 'Iporanga', 'Itariri', 'Jacupiranga', 'Juquiá', 'Miracatu', 'Pariquera-Açu', 'Pedro de Toledo', 'Registro', 'Sete Barras']

    drs_info['DRS 04 Baixada Santista'] = ['Bertioga', 'Cubatão', 'Guarujá', 'Itanhaém', 'Mongaguá', 'Peruíbe', 'Praia Grande', 'Santos', 'São Vicente']

    drs_info['Estado de São Paulo'] = []

    for i,v in drs_info.items():
        if i != 'Estado de São Paulo':
            drs_info['Estado de São Paulo'] += [x for x in v]

    return drs_info

# Return {City:DRS}
def munInfo():
    mun_info = {}

    for drs, mun_list in drsInfo().items():

        if drs == 'Estado de São Paulo':
            continue

        for mun in mun_list:
            mun_info[mun] = drs

    return mun_info

if __name__ == '__main__':

    updateData()