# meg_voice_pt
Sistema de Voz - Semelhante a Siri, Alexa, etc

## Justificativa

Nesse sistema estamos testando em Python diversos módulos e funções que permitem ao usuário se comunicar com o sistema 
através de comandos por voz.
Nesse exemplo é possivel:
- Solicitar o nome da assistente;
- Fazer perguntas genéricas, como:
  - Porque você existe?
  - Quando você dorme?
  - Qual o seu filme favorito?
- Solicitar a cotação de Bitcoin, Ethereum
- Soliciatr a cotação do dólar
- Solicitar a situação atual do Mercado de Ações no Brasil (BOVESPA)
- Solicitar o valor de Petrobrás e Vale (Ações)
- Perguntar qual é a capital de um País
- Pedir para traduzir uma frase para o Inglês.
- Solicitar uma piada (Chuck Noris Module)
- Perguntar sobre o Clima em uma cidade
- Perguntar a distância entre duas cidades
- Fazer uma pesquisa no Wikipedia
- Solicitar as notícias do dia.
- Perguntar as horas
- Perguntar a data

O programa está utilizando como base o Português/Brasil e para alguns módulos há tradução.
A sintetização de voz é um módulo público, utilizado apenas para fins didáticos.
Fique livre para adaptar e incluir novas funcionalidades.
 
## Modulos que devem ser instalados:

### Reconhecimento de Voz
pip install speechrecognition 

### Converter texto para fala (Google Text to Speech)
pip install gtts

### Módulo para executar audio mp3
import playsound

### Acesso ao Sistema Operacional (Ativar recursos audio e outros)
pip install os

### Módulo para leitura de URLs / json
pip install requests

### Consulta ações e mercado financeiro
pip install yfinance

### Módulo que pesquisa as capitais dos Países
pip install wolframalpha

### Módulo de tradução (Vários idiomas, no projeto utilizado apenas (en) / (pt)
import translators as ts

### Módulo de acesso ao Wikipedia
pip install wikipedia

### Módulo para uso de Datas e Horas
pip install datetime
