# Sistemas IoT com ESP32 e comunicação via MQTT
Material da apresentação no evento Espressif Summit 2025.

## Demostração
Para demonstrar o protocolo MQTT em funcionamento, esse repositório contém um exemplo de código
que utiliza duas ESP32 para papéis distintos: uma para sensoriamento e outra para controle.

A ESP32 de sensoriamento coleta dados de um módulo joystick e de um sensor de distância ultrassônico,
enviando essas informações para o broker MQTT. Enquanto isso, a ESP32 de controle recebe os dados do broker
e utiliza um anel de LED e um servo motor para responder às informações recebidas.

A demonstração acompanha uma dashboard em React que exibe os dados em tempo real através de um websocket.


## Requisitos
Para executar o exemplo, é necessário ter instalado o MicroPython nas ESP32 e configurar o broker MQTT e ativar o listener de websockets (caso queira visualizar a dashboard).

### Configurando o hardware
Para a demonstração, você precisará dos seguintes componentes:

#### Sensoriamento
- 1 ESP32
- 1 módulo joystick
- 1 sensor de distância ultrassônico

#### Controle
- 1 ESP32
- 1 anel de LED
- 1 servo motor

O circuito de ligação dos componentes é o seguinte:

**ESP32 de sensoriamento**

Módulo joystick:
- VCC -> Fonte de alimentação (5V)
- GND -> GND
- X -> GPIO 35
- Y -> GPIO 34

Sensor ultrassônico:
- VCC -> Fonte de alimentação (5V)
- GND -> GND
- Trig -> GPIO 5
- Echo -> GPIO 18

**ESP32 de controle**

- Anel de LED:
    - VCC -> Fonte de alimentação (5V)
    - GND -> GND
    - Data -> GPIO 5
- Servo motor:
    - VCC -> Fonte de alimentação (5V)
    - GND -> GND
    - Signal -> GPIO 18


### Configurando o software
Para executar o exemplo, siga os passos abaixo:
1. Instale o MicroPython nas ESP32
2. Configure o broker MQTT (suba um broker local ou utilize um serviço online)
3. Copie os arquivos da pasta `demo/sensors` para a ESP32 de sensoriamento
4. Copie os arquivos da pasta `demo/actuators` para a ESP32 de controle
5. Edite os arquivos `boot.py` em ambas as pastas para configurar o acesso à rede Wi-Fi
6. Edite os arquivos `main.py` em ambas as pastas para configurar o broker MQTT

Para visualizar os dados em tempo real, você pode utilizar a dashboard em React. Para isso, siga os passos abaixo:
1. Navegue até a pasta `demo/dashboard`
2. Instale as dependências com `npm install`
3. Edite o arquivo `src/App.js` para configurar o endereço do broker MQTT
4. Inicie o servidor com `npm start`
