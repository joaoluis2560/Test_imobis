from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('urls.csv')

private_area = ResponseSchema(name='private_area', 
                                    type='int', 
                                    description='Metragem privativa do imóvel, sendo 0 se não for encontrado')

price = ResponseSchema(name='price',
                        type='int',
                        description='Preço aproximado do imóvel, sendo 0 se não for encontrado')

global_area = ResponseSchema(
    name='global_area',
    type='int',
    description='Metragem global (area total) do imóvel, sendo 0 se não for encontrado'
) 

property_type = ResponseSchema(
    name='property_type',
    type='str',
    description='O tipo de propriedade do imóvel, sendo Casa ou Apartamento sem nenhuma outra descrição'
)

bedrooms = ResponseSchema(
    name='bedrooms',
    type='int',
    description='O numero de quartos do imóvel, sendo 0 se não for encontrado'
)

bathrooms = ResponseSchema(
    name='bathrooms',
    type='int',
    description='O numero de banheiros do imóvel, sendo 0 se não for encontrado'
)

parking_lots = ResponseSchema(
    name='parking_lots',
    type='int',
    description='O numero de vagas de estacionamento (garagens) do imóvel, sendo 0 se não for encontrado'
)
neighborhood = ResponseSchema(
    name='neighborhood',
    type='str',
    description='Nome do bairro do imóvel em Passo Fundo, Rio Grande do Sul, sendo 0 se não for encontrado'
)

address = ResponseSchema(
    name='address',
    type='str',
    description='endereço completo do imóveil, sendo 0 se não for encontrado'
)

has_swimmmingpool = ResponseSchema(
    name='has_swimmmingpool',
    type='str',
    description='Informação se o imóvel conta ou não com piscina, sendo não se não for encontrado'
)

has_fireplace = ResponseSchema(
    name='has_fireplace',
    type='str',
    description='Informação se o imóvel conta ou não com lareira, sendo não se não for encontrado'
)

gym = ResponseSchema(
    name='gym',
    type='str',
    description='Informação se o imóvel conta ou não com academia ou espaço fitness, sendo não se não for encontrado'
)

laundry = ResponseSchema(
    name='laundry',
    type='str',
    description='Informação se o imóvel conta ou não com lavandereia, sendo não se não for encontrado'
)

kids_place = ResponseSchema(
    name='kids_place',
    type='str',
    description='Informação se o imóvel conta ou não com espaço para crianças ou espaço kids, sendo não se não for encontrado'
)

living_rooms = ResponseSchema(
    name='living_rooms',
    type='int',
    description='Informação se o imóvel conta ou não com salas de estar, sendo 0 se não for encontrado'
)

dinner_rooms = ResponseSchema(
    name='dinner_rooms',
    type='int',
    description='Informação se o imóvel conta ou não com salas de jantar, sendo 0 se não for encontrado'
)

party_room = ResponseSchema(
    name='party_room',
    type='str',
    description='Informação se o imóvel conta ou não com salões de festa, sendo não se não for encontrado'
)

pet_place = ResponseSchema(
    name='pet_place',
    type='str',
    description='Informação se o imóvel conta ou não com espaço para pets, sendo não se não for encontrado'
)

grill = ResponseSchema(
    name='grill',
    type='str',
    description='Informação se o imóvel conta ou não com churrasqueira ou area para churrasco, sendo não se não for encontrado'
)

balcony = ResponseSchema(
    name='balcony',
    type='str',
    description='Informação se o imóvel conta ou não com sacadas, sendo não se não for encontrado'
)

characteristics = ResponseSchema(
    name='characteristics',
    type='str',
    description='Toda e qualquer característica do imóvel anunciado no site, incluindo todas e quaisquer informações disponíveis que tenham relação com o imóvel como: piscina, churrasqueira, etc...'
)

eletrics_car_chargers = ResponseSchema(
    name='eletrics_car_chargers',
    type='str',
    description='Se o imóvel conta ou não com carregadores de carros elétricos, sendo não se não for encontrado'
)

has_furniture = ResponseSchema(
    name='has_furniture',
    type='str',
    description='Se o imóvel conta ou não com mobilia, sendo Mobiliado, Semi-mobiliado ou Não mobiliado'
)

suites = ResponseSchema(
    name='suites',
    type='int',
    description='Quantidade de suites do imóveil, sendo 0 se não for encontrado'
)

penthouse = ResponseSchema(
    name='penthouse',
    type='str',
    description='Se o imóvel é cobertura ou não, sendo não se não for encontrado'
)


condominium_price = ResponseSchema(
    name='condominium_price',
    type='str',
    description='Valor do condominio do imóvel, sendo 0 se não for encontrado'
)

response_schema = [
    neighborhood, 
    address,
    property_type,
    price,
    condominium_price,
    bedrooms,
    suites,
    bathrooms, 
    living_rooms,
    dinner_rooms,
    balcony,
    parking_lots, 
    private_area, 
    global_area, 
    penthouse,
    has_furniture,
    characteristics,
    has_swimmmingpool,
    has_fireplace,
    gym,
    laundry,
    kids_place,
    party_room,
    pet_place,
    grill,
    eletrics_car_chargers
]

def divide_lista(lista, tamanho_sublista):
    # Usando compreensão de lista para dividir a lista
    return [lista[i:i + tamanho_sublista] for i in range(0, len(lista), tamanho_sublista)]

final_urls = divide_lista(df['url'].to_list(), 10)

final_list = []
for idx_sublista,sublist in enumerate(final_urls):
    print(f"Sublista {idx_sublista + 1}:")
    sublist_data = []
    for idx_item,url in enumerate(sublist):
        print(f"  URL {idx_item + 1}: {url}")

        loader = WebBaseLoader(url)
        documentos = loader.load()
    
        output_parser = StructuredOutputParser.from_response_schemas(response_schema)
        schema_formatado = output_parser.get_format_instructions()

        template = ChatPromptTemplate.from_template("""
                                                    Para o texto a seguir, extraia as seguintes informações: 
                                                    neighborhood, 
                                                    address,
                                                    property_type,
                                                    price,
                                                    condominium_price,
                                                    bedrooms,
                                                    suites,
                                                    bathrooms, 
                                                    living_rooms,
                                                    dinner_rooms,
                                                    balcony,
                                                    parking_lots, 
                                                    private_area, 
                                                    global_area, 
                                                    penthouse,
                                                    has_furniture,
                                                    characteristics,
                                                    has_swimmmingpool,
                                                    has_fireplace,
                                                    gym,
                                                    laundry,
                                                    kids_place,
                                                    party_room,
                                                    pet_place,
                                                    grill,
                                                    eletrics_car_chargers

        Texto: {documentos}

        {schema}
        """, partial_variables={'schema': schema_formatado})

        strDoc = ''
        for doc in documentos:
            strDoc += doc.page_content
        strDoc

        chat = ChatOpenAI()
        resposta = chat.invoke(template.format_messages(documentos=strDoc))

        try:
            resposta_json = output_parser.parse(resposta.content)
            print(resposta_json) 
            
            resposta_json['url'] = url 
     
            sublist_data.append(resposta_json)

            print('Quantidade imoveis na sublista => ', len(sublist_data))
        except Exception as e:
            print("Error:", e)
    
    final_list.extend(sublist_data)
    print('Tamanho da lista final' , len(final_list))
    df_final = pd.DataFrame.from_records(final_list)
    df_final.to_csv('df_final.csv', index=False)
 


 