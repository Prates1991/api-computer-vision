# api-computer-vision

-----------------------------------------------------------------------------------------------
# Resumo

 Neste repositório está uma forma de aplicação da API criada para reconhecimento de padrões
 via visão computacional.

 Utilizei a API em um sistema de controle de acesso a áreas restritas.

-----------------------------------------------------------------------------------------------
# Pré requisitos para execução:

  1. Bibliotecas Python utilizadas e que precisam ser instaladas:
    
    cv2
      comando: pip install opencv-contrib-python
      dúvidas: https://pypi.org/project/opencv-python/

    PyQt5
      comando: pip install pyqt5
      dúvidas: http://pyqt.sourceforge.net/Docs/PyQt5/installation.html
      dúvidas: https://www.metachris.com/2016/03/how-to-install-qt56-pyqt5-virtualenv-python3/
 
    glob
      comando: pip install glob
      dúvidas: https://docs.python.org/2/library/glob.html

 2. Instalar aplicativo DroidCam em seu Smartphone ou algum aplicativo similar que possibilite
    conetar à câmera do Smartphone via endereço IP.
    
-----------------------------------------------------------------------------------------------
# Como inicializar:

 1. Conectar seu Smartphone na mesma rede Wi-fi de seu computador ou então rotear a internet de 
    seu computador para seu Smartphone.

 2. Abrir o aplicativo DroidCam e copiar o endereço IP e a porta de conexão constantes no 
    aplicativo para "main.py" dentro da função "ativa_camera" na linha 910.

 3. Executar "main.py"
 
 -----------------------------------------------------------------------------------------------
# Como utilizar:

 1. posicionar a o celular em uma posição fixa e com a câmera a uma distância de aproximadamente 
    10cm da superfície onde o padrão será apresentado fronte à câmera.

 2. Com a opção "cadastrar" ativa dentro do menu "Manutenção de Cadastros", clicar em "Ativar 
    Câmera" para realizar o cadastro de um grupo de usuários.

 3. Posicione o padrão condizente ao nome do grupo digitado no espaço para texto "Nome do padrão 
    de acesso" e, em seguida, clique em "Cadastrar".
    Pronto! Você tem um grupo de usuários cadastrado e está pronto para testar o controle de 
    acesso.

 4. Digite no espaço para texto "Nome do padrão" o nome cadastrado nos passos anteriores.

 5. Ao posicionar o padrão correto em frente á câmera, será disparado um Bip sonoro para indicar 
    o match.
    
-----------------------------------------------------------------------------------------------
# Detalhes do projeto:

 1. Todas as ações executadas no software são salvadas em um log que pode ser acessado na aba 
    "Log de Acesso" localizada no canto superior esquerdo da tela principal.

 2. A variação de luminosidade sobre o padrão apresentado para a câmera pode alterar a precisão 
    do reconhecimento do padrão
    Portanto, o padrão deve ser cadastrado com a câmera posicionada da mesma maneira que ficará 
    posicionada quando for utilizada para analisar os padrões apresentados para análise.
