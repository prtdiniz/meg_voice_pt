'''
Rotinas principais de consultas e diálogos
'''
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import requests
import yfinance as yf
import wolframalpha
import translators as ts
import wikipedia
import datetime

# Carga de Dados Externos
# Crypto Currency
crypto_api='https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cdogecoin%2Cstoriqa%2Ctokia%2Cucash&vs_currencies=usd%2Cbrl'
# Wolframalpha API
wolfram_api = '4Y8TR4-GVHLK6R9GL'
# Chuck Noris API
chuck_noris_api = 'https://api.chucknorris.io/jokes/random'
# News API Key
news_api_key = 'db22936c541c47d4a473d2e4a8395417'
# Weatherbit.io API
clima_api_key = '3cffcd6c00d2454e9e894ceb6893c8d4'
#Mapquest API
mapquest_api_key='bEZIHaYGwD2M35M2l4A3oP5KvhKWCiIm'
#Set language for Wikipedia
wikipedia.set_lang("pt")

def wolfram_alpha_capitais(text):
    client = wolframalpha.Client(wolfram_api)
    result = client.query(text)
    answer = next(result.results).text
    answer_split = answer.split()
    print(answer_split)
    capital_result = 'A capital de  '+ answer_split[-1] + ' é '+answer_split[0]
    meg_talk(capital_result)

def meg_listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        text = ''

        try:
            text = r.recognize_google(audio, language='pt-BR')
        except sr.RequestError as re:
            print(re)
        except sr.UnknownValueError as uve:
            print(uve)
        except sr.WaitTimeoutError as wte:
            print(wte)
    text = text.lower()
    return text

# Convert text to speech
def meg_talk_en(text):
    #create audio data
    file_name = 'audio_data.mp3'
    #convert text to speech
    tts = gTTS(text=text,lang='en')
    #save the file
    tts.save(file_name)
    # play file
    playsound.playsound(file_name)
    # remove file
    os.remove(file_name)

def meg_talk(text):
    #create audio data
    file_name = 'audio_data.mp3'
    #convert text to speech
    tts = gTTS(text=text,lang='pt-BR', tld='com.br')
    #save the file
    tts.save(file_name)
    # play file
    playsound.playsound(file_name)
    # remove file
    os.remove(file_name)

def translator(text):
    meg_talk_en(ts.google(text, from_language='pt', to_language='en'))

def translator_en(text):
    meg_talk(ts.google(text, from_language='en', to_language='pt'))

def chuck_noris():
    cn_data = requests.get(chuck_noris_api)
    cn_json = cn_data.json()
    translator_en(cn_json['value'])

def get_news():
    news_url = 'https://newsapi.org/v2/top-headlines?country=br&apiKey=' + news_api_key
    news = requests.get(news_url).json()
    articles = news['articles']
    contador = 0
    for art in articles:
        contador +=1
        meg_talk('notícia '+ str(contador))
        meg_talk(art['title'])
        if contador % 5 == 0:
            meg_talk('Diga fechar notícias para parar')
            retorno = meg_listen()
            if 'fechar' in retorno:
                meg_talk('Ok. Encerrando notícias. Diga o que deseja agora.')
                break

def consulta_clima():
    meg_talk('Qual cidade você quer saber a situação do clima?')
    cidade = meg_listen()
    clima_url = "https://api.weatherbit.io/v2.0/current?city="+cidade+"&lang=pt&key="+ clima_api_key
    clima = requests.get(clima_url).json()
    #print(clima)
    print(cidade)
    temperatura = clima['data'][0]['temp']
    status = clima['data'][0]['weather']['description']
    visibilidade = clima['data'][0]['vis']
    resultado = cidade+' apresenta '+status+' com '+str(temperatura)+' graus e visibilidade de '+str(visibilidade)+' quilômetros'
    meg_talk(resultado)

def distancia_cidades():
    meg_talk('Qual é a cidade de origem?')
    cidade_1= meg_listen()
    meg_talk('Qual é a cidade de destino?')
    cidade_2= meg_listen()
    meg_talk('Por favor, aguarde. Vou consultar a distância.')
    consulta='http://www.mapquestapi.com/directions/v2/route?key='+mapquest_api_key+'&from='+cidade_1+'&to='+cidade_2+'&unit=k'
    consulta_req = requests.get(consulta).json()
    distancia = round(consulta_req['route']['distance'],1)
    tempo = consulta_req['route']['formattedTime']
    comb = consulta_req['route']['fuelUsed']
    meg_talk('A distância entre '+cidade_1+' e '+cidade_2+' é de '+str(distancia)+'km.')
    meg_talk('O tempo de viagem previsto é de '+str(tempo)+ ' e deve consumir '+str(round(comb*3.8,2))+ ' litros de combustível')

def wikipedia_pesq():
    meg_talk('Sobre o que você deseja que eu pesquise?')
    tema = meg_listen()
    wiki_result = wikipedia.summary(tema, sentences = 2)
    meg_talk(wiki_result)
    meg_talk('Pesquisa concluida. Caso queira uma nova pesquisa, só solicitar')

def dizer_horas():
    agora = datetime.datetime.now()
    hora = agora.strftime("%I")
    minuto = agora.strftime("%M")
    ampm = agora.strftime("%p")
    periodo = ' da tarde '
    if ampm == 'am':
        periodo = " da manhã "
    plural = 's e '
    if hora == 1:
        plural = ' e '
    meg_talk('Agora são '+hora+' hora'+plural+minuto+' minutos'+periodo)
    #meg_talk('Agora são '+hora+':'+minuto)

def dizer_data():
    diasemana = ['segunda feira','terceira feira','quarta feira',
             'quinta feira','sexta feira','sabado','domingo']
    meses=['janeiro','fevereiro','março','abril','maio','junho',
            'julho','agosto','setembro','outubro','novembro','dezembro']
    agora = datetime.date.today()
    mes=(agora.month-1)
    diadoano=(agora.strftime('%d'))
    diadasemana = datetime.date.weekday(agora)
    meg_talk('hoje é '+diadoano+ ' de '+meses[mes]+' '+diasemana[diadasemana])

#create a function which will give us back a reply based on the input text
def meg_reply(text):
    # smalltalk - what is your name
    if 'qual' in text and 'nome' in text:
        meg_talk('Meu nome é Meg e eu sou a sua assistente pessoal')
    elif 'porque' in text and 'existe' in text:
        meg_talk('Eu fui criada para lhe ajudar. Eu não preciso de descanso, nem de férias')
    elif 'quando' in text and 'dorme' in text:
        meg_talk('Eu nunca durmo .Eu fui criada para lhe ajudar 24 horas por dia')
    elif 'você'in text and 'estúpida' in text:
        meg_talk('Me desculpe, mas não posso ser estúpida. Essa é uma característica humana e eu sou uma máquina')
    elif 'favorito'in text and 'filme' in text:
        meg_talk('Oh... Eu amo Ghost! Sempre que posso assisto com meus amigos aqui no mundo virtual')
    elif 'pare' in text or 'parar' in text or 'sair' in text or 'encerrar' in text:
        meg_talk('Sempre é um prazer lhe ajudar, Te desejo um dia maravilhoso')
    elif 'bitcoin' in text:
        response = requests.get(crypto_api)
        crypto_json = response.json()
        price = crypto_json['bitcoin']['usd']
        preco = crypto_json['bitcoin']['brl']
        meg_talk('Nesse momento, um Bitcoin está valendo '+ str(price) + ' Dólares Amerianos ou '+ str(preco) + ' Reais'  )
    elif 'ethereum' in text:
        response = requests.get(crypto_api)
        crypto_json = response.json()
        price = crypto_json['ethereum']['usd']
        preco = crypto_json['ethereum']['brl']
        meg_talk('Nesse momento, um Ethereum está valendo '+ str(price) + ' Dólares Americanos ou '+ str(preco) + ' Reais'  )
    elif 'doge' in text:
        response = requests.get(crypto_api)
        crypto_json = response.json()
        price = crypto_json['dogecoin']['usd']
        preco = crypto_json['dogecoin']['brl']
        meg_talk('Nesse momento, um Doge Cóin está valendo '+ str(price) + ' Dólares Americanos ou '+ str(preco) + ' Reais'  )
    elif 'cotação' in text and 'dólar' in text:
        response = requests.get(crypto_api)
        crypto_json = response.json()
        price = crypto_json['bitcoin']['usd']
        preco = crypto_json['bitcoin']['brl']
        centavos = round(preco/price,2) - int(preco/price)
        meg_talk('Nesse momento, um Dólar Americano está valendo '+ str(int(preco/price)) + ' Reais e ' + str(round(centavos,2)) + ' Centavos')
    elif 'mercado' in text or 'ações' in text:
        meg_talk('Aguarde um momento que preciso consultar')
        bovespa = yf.Ticker('^BVSP')
        cotacao_bov = bovespa.info['regularMarketPrice']
        diferenca = cotacao_bov - bovespa.info['previousClose']
        status = ' subindo '
        if diferenca < 0:
            status = ' caindo '
        porcentagem = (diferenca / bovespa.info['previousClose'])*100
        meg_talk('O índice Bovespa está em '+ str(int(cotacao_bov)) + status + str(round(porcentagem,2)) + ' porcento')
    elif 'petrobras' in text:
        meg_talk('Aguarde um momento que preciso consultar')
        bovespa = yf.Ticker('PETR4.SA')
        agora = bovespa.info['regularMarketPrice']
        diferenca = agora - bovespa.info['regularMarketPreviousClose']
        porcentagem = round((diferenca / bovespa.info['regularMarketPreviousClose'])*100,2)
        status = ' subindo '
        if diferenca < 0:
            status = ' caindo '
        meg_talk('A petrobrás está ' + status + ' em ' + str(porcentagem) + ' porcento a ' + str(bovespa.info['regularMarketPrice']) + ' Reais')
    elif 'vale' in text:
        meg_talk('Aguarde um momento que preciso consultar')
        bovespa = yf.Ticker('VALE3.SA')
        agora = bovespa.info['regularMarketPrice']
        diferenca = agora - bovespa.info['regularMarketPreviousClose']
        porcentagem = round((diferenca / bovespa.info['regularMarketPreviousClose'])*100,2)
        status = ' subindo '
        if diferenca < 0:
            status = ' caindo '
        meg_talk('A vale está ' + status + ' em ' + str(porcentagem) + ' porcento a ' + str(bovespa.info['regularMarketPrice']) + ' Reais')
    elif 'cogna' in text:
        meg_talk('Aguarde um momento que preciso consultar')
        bovespa = yf.Ticker('COGN3.SA')
        agora = bovespa.info['regularMarketPrice']
        diferenca = agora - bovespa.info['regularMarketPreviousClose']
        porcentagem = round((diferenca / bovespa.info['regularMarketPreviousClose'])*100,2)
        status = ' subindo '
        if diferenca < 0:
            status = ' caindo '
        meg_talk('A cogna está ' + status + ' em ' + str(porcentagem) + ' porcento a ' + str(bovespa.info['regularMarketPrice']) + ' Reais')
    elif 'capital' in text:
        wolfram_alpha_capitais(text)
    elif 'traduza'in text or 'traduzir' in text:
        meg_talk('Claro, diga o que você quer que eu traduza para o Inglês')
        while True:
            text_to_translate = meg_listen()
            if "fechar traduções" not in text_to_translate:
                translator(text_to_translate)
                meg_talk('Fale outra frase ou fechar traduções.')
            else:
                meg_talk('Encerrando traduções. O que gostaria de fazer agora?')
                break
    elif 'piada' in text:
        chuck_noris()
    elif 'notícias' in text:
        meg_talk('Vamos as notícias de hoje.')
        get_news()
    elif 'clima' in text or 'temperatura' in text:
        consulta_clima()
    elif 'distância' in text:
        distancia_cidades()
    elif 'pesquise'in text or 'pesquisa' in text or 'o que é' in text:
        wikipedia_pesq()
    elif 'horas'in text:
        dizer_horas()
    elif 'dia' in text or 'data' in text:
        dizer_data()
    else:
        meg_talk('Me desculpe, não entendi. Você poderia repetir?')
