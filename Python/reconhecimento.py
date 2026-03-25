import cv2
from ultralytics import YOLO

# 1. Carrega o modelo treinado (o arquivo best.pt)
modelo = YOLO('best.pt')

# 2. Define qual imagem vamos testar
imagem_teste = 'teste.jpg' # Troque para o nome da sua foto se for diferente

print("Analisando a imagem...")

# 3. Pede para a IA analisar a imagem
# O conf é a porcentagem mínima de certeza
resultados = modelo(imagem_teste, conf=0.1)

# 4. Desenha as caixas na imagem e mostra na tela
for resultado in resultados:
    # Desenha na tela o resultado
    imagem_anotada = resultado.plot() 
    
    # Mostra a imagem numa janela do Windows
    cv2.imshow("Análise de Maracujás", imagem_anotada)
    
    print("\n--- Analise Concluida! ---")
    print("Pressione qualquer tecla na janela da imagem para fechar.")
    
    # Espera você apertar qualquer tecla para fechar a janela
    cv2.waitKey(0) 
    cv2.destroyAllWindows()