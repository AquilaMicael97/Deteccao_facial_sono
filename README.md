# Monitor de Sonolência em Tempo Real com Vision Computacional

Este projeto utiliza inteligência artificial e visão computacional para detectar sinais de fadiga e sonolência em motoristas ou usuários de computador. Através da análise de marcos faciais (Facial Landmarks), o sistema monitora a frequência de piscadas e o tempo de olhos fechados.

## 🚀 Funcionalidades

* **Detecção de EAR (Eye Aspect Ratio):** Calcula a razão de abertura dos olhos para identificar se o usuário está piscando ou com os olhos fechados por um período prolongado.
* **Detecção de MAR (Mouth Aspect Ratio):** Monitora a abertura da boca para identificar bocejos ou inconsistências na face.
* **Contagem de Piscadas por Minuto:** Monitora a frequência cardíaca ocular. Uma queda brusca nas piscadas por minuto pode indicar início de fadiga.
* **Alertas Visuais:** Exibe na tela o status "COM SONOLÊNCIA" caso o tempo de olhos fechados exceda 1.5 segundos ou a frequência de piscadas caia abaixo do nível seguro.

## 🛠️ Tecnologias Utilizadas

* **[OpenCV](https://www.google.com/search?q=https://opencv.org/):** Processamento de imagem e exibição de vídeo.
* **[MediaPipe (Face Mesh)](https://www.google.com/search?q=https://google.github.io/mediapipe/solutions/face_mesh.html):** Mapeamento de 468 pontos faciais em 3D com alta performance.
* **NumPy:** Cálculos matemáticos vetoriais para as razões de aspecto.

## 📊 Como funciona a lógica?

1. **Mapeamento:** O MediaPipe identifica pontos específicos nos olhos e na boca.
2. **Cálculo EAR:** É calculada a distância vertical entre as pálpebras dividida pela distância horizontal. Se o valor cair abaixo de `0.3`, considera-se o olho fechado.
3. **Cálculo MAR:** Monitora a abertura da boca para evitar falsos positivos de piscadas durante bocejos ou falas.
4. **Decisão:**
* Se o olho ficar fechado por $> 1.5s$ $\rightarrow$ **Alerta de Sonolência**.
* Se a média de piscadas por minuto for $< 10$ $\rightarrow$ **Alerta de Sonolência**.



## 🔧 Como instalar e rodar

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

```


2. **Instale as dependências:**
```bash
pip install opencv-python mediapipe numpy

```


3. **Execute o script:**
```bash
python nome_do_seu_arquivo.py

```



> **Nota:** Certifique-se de que sua webcam está conectada. O código está configurado para o índice de câmera `1` (`cv2.VideoCapture(1)`). Se não funcionar, altere para `0`.

## ⌨️ Controles

* Pressione a tecla **'c'** para fechar a janela da câmera e encerrar o programa.

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Se você tiver sugestões de melhorias (como adicionar um alerta sonoro ou interface gráfica), sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

---

Desenvolvido por [Seu Nome]