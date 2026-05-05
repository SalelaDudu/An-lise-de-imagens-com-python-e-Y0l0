import cv2
import os
import shutil
from ultralytics import YOLO

# 1. Carrega o modelo treinado
modelo = YOLO('best.pt')

pasta_entrada = 'Treinar'  # Pasta com as imagens para avaliar
pasta_acertos = 'IA_Acertou'     # Para onde vão as imagclsens corretas
pasta_erros = 'IA_Errou'         # Para onde vão as imagens que precisam ser revisadas

# Cria as pastas de saída se elas não existirem
os.makedirs(pasta_acertos, exist_ok=True)
os.makedirs(pasta_erros, exist_ok=True)

print("Iniciando a Triagem! Comandos da janela:")
print("[ C ] - Correto (A IA acertou tudo)")
print("[ E ] - Errado (A IA errou ou esqueceu algo)")
print("[ Q ] - Sair (Fecha o programa)")
print("-" * 40)

# 3. Lê todas as imagens da pasta de entrada
for nome_arquivo in os.listdir(pasta_entrada):
    # Valida se é  uma imagem
    if not nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        continue

    caminho_imagem = os.path.join(pasta_entrada, nome_arquivo)
    # Analisa
    resultados = modelo(caminho_imagem, conf=0.25)
    # Desenha as caixas de identificação
    resultado = resultados[0]
    imagem_anotada = resultado.plot() 
    
    # Mostra na tela
    cv2.imshow("Triagem de Maracujas - Supervisor", imagem_anotada)
    
    # 4. Espera a sua decisão no teclado
    tecla = cv2.waitKey(0) & 0xFF
    
    if tecla == ord('c'):
        print(f"[{nome_arquivo}] -> CORRETO!")
        # Move a foto original para a pasta de acertos
        shutil.move(caminho_imagem, os.path.join(pasta_acertos, nome_arquivo))
        
    elif tecla == ord('e'):
        print(f"[{nome_arquivo}] -> ERRADO (Vai pro CVAT)")
        # Move a foto original para a pasta de erros
        shutil.move(caminho_imagem, os.path.join(pasta_erros, nome_arquivo))
        
    elif tecla == ord('q'):
        print("Triagem interrompida pelo usuário.")
        break
    else:
        print("Tecla inválida. Pressione C, E ou Q.")

cv2.destroyAllWindows()
print("\n--- Fim da Triagem ---")