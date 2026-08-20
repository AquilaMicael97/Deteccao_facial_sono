# Monitor de Sonolência em Tempo Real com Visão Computacional

Este projeto utiliza inteligência artificial e visão computacional para detectar sinais de fadiga e sonolência em motoristas ou usuários de computador. Através da análise de marcos faciais (Facial Landmarks), o sistema monitora a frequência de piscadas, o tempo de olhos fechados e os bocejos.

## 🚀 Funcionalidades

* **Detecção de EAR (Eye Aspect Ratio):** Calcula a razão de abertura dos olhos para identificar se o usuário está piscando ou com os olhos fechados por um período prolongado.
* **Detecção de MAR (Mouth Aspect Ratio):** Monitora a abertura da boca, tanto para evitar falsos positivos de piscada durante a fala quanto para identificar bocejos.
* **Contagem de Piscadas por Minuto:** Mantém uma janela deslizante de 60 segundos. Uma queda brusca nas piscadas por minuto pode indicar início de fadiga.
* **Contagem de Bocejos:** Um bocejo é contabilizado quando a boca permanece aberta (MAR ≥ `0.4`) por pelo menos 1 segundo.
* **Alertas Visuais:** Exibe na tela o status "COM SONOLENCIA" em vermelho quando algum dos critérios de fadiga é atingido.
* **Painel de Diagnóstico:** Mostra em tempo real o MAR atual, as piscadas por minuto e o total de bocejos.

## 🛠️ Tecnologias Utilizadas

* **[OpenCV](https://opencv.org/):** Processamento de imagem e exibição de vídeo.
* **[MediaPipe Tasks — Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker):** Mapeamento de 478 pontos faciais em 3D com alta performance, em modo de vídeo.
* **NumPy:** Cálculos matemáticos vetoriais para as razões de aspecto.

> O modelo `face_landmarker.task` já está incluído no repositório e é carregado automaticamente a partir da pasta do `app.py` — não é necessário baixá-lo separadamente.

## 📊 Como funciona a lógica?

1. **Mapeamento:** O MediaPipe identifica pontos específicos nos olhos e na boca a cada frame.
2. **Cálculo EAR:** É calculada a distância vertical entre as pálpebras dividida pela distância horizontal. Se o valor cair abaixo de `0.3` (com MAR abaixo de `0.1`), considera-se o olho fechado.
3. **Cálculo MAR:** Monitora a abertura da boca, para descartar falsos positivos de piscada durante a fala e para detectar bocejos.
4. **Decisão:** o alerta de sonolência é disparado se **qualquer** uma destas condições ocorrer:
* Olhos fechados por mais de **1.5 s**;
* Menos de **5 piscadas por minuto** (só avaliado depois que a janela de 60 s está completa — até lá o painel mostra `?`);
* **Bocejo** detectado nos últimos **3 s**.

## 🔧 Como instalar e rodar

1. **Clone o repositório:**
```bash
git clone https://github.com/AquilaMicael97/Deteccao_facial_sono
cd Deteccao_facial_sono

```


2. **Instale as dependências:**
```bash
pip install opencv-python mediapipe numpy

```

> Testado com Python 3.13, `mediapipe` 0.10.35, `opencv-python` 5.0.0 e `numpy` 2.5.2. É necessário um `mediapipe` recente o bastante para oferecer a API `mediapipe.tasks` e o `FaceLandmarker`.


3. **Execute o script:**
```bash
python app.py

```



> **Nota:** Certifique-se de que sua webcam está conectada. O código está configurado para o índice de câmera `0` (`cv2.VideoCapture(0)`). Se você usa uma câmera externa, pode ser necessário alterar para `1`.

## ⚙️ Ajustando os limiares

Os parâmetros ficam no topo do `app.py` e podem ser calibrados para o seu caso de uso:

| Variável | Padrão | O que faz |
| --- | --- | --- |
| `ear_limiar` | `0.3` | Abaixo disso o olho é considerado fechado |
| `mar_limiar` | `0.1` | Acima disso a boca está aberta (descarta piscadas durante a fala) |
| `mar_bocejo` | `0.4` | Abertura de boca considerada bocejo |
| `t_bocejo` | `1.0` | Segundos de boca aberta para contabilizar um bocejo |
| `alerta_bocejo` | `3.0` | Segundos de alerta após o último bocejo |
| `piscadas_limiar` | `5` | Piscadas por minuto abaixo das quais há alerta |

## ⌨️ Controles

* Pressione a tecla **'c'** para fechar a janela da câmera e encerrar o programa.

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Se você tiver sugestões de melhorias (como adicionar um alerta sonoro ou interface gráfica), sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

---
