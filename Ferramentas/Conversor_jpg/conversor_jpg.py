import os
import cv2
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from tqdm import tqdm

# ================= CONFIGURAÇÕES =================
PASTA_ENTRADA = "C:/Users/ProjetoFapesIfes/Downloads/www.google.com/maracuja verde/" # Substitua pelo caminho da sua pasta de entrada
PASTA_SAIDA = "C:/Users/ProjetoFapesIfes/Downloads/www.google.com/maracuja_verde/"  # Substitua pelo caminho da sua pasta de saída
PREFIXO_NOME = "maracuja_verde_"

# Extensões suportadas
EXTENSOES_IMAGEM = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff'}
EXTENSOES_VIDEO = {'.mp4', '.webm', '.avi', '.mov', '.mkv', '.flv'}
# =================================================

def obter_proximo_caminho(pasta_saida, prefixo, contador_atual):
    """Garante que o arquivo não será sobrescrito, buscando o próximo número livre."""
    while True:
        nome_arquivo = f"{prefixo}{contador_atual}.jpg"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        if not os.path.exists(caminho_completo):
            return caminho_completo, contador_atual
        contador_atual += 1

def processar_imagem(caminho_entrada, caminho_saida):
    """Abre uma imagem, converte para RGB (removendo transparências) e salva como JPG."""
    with Image.open(caminho_entrada) as img:
        # Converte para RGB para garantir compatibilidade com JPG 
        # (necessário para PNGs com fundo transparente ou GIFs)
        img_rgb = img.convert('RGB')
        img_rgb.save(caminho_saida, 'JPEG', quality=100)

def processar_video(caminho_entrada, caminho_saida):
    """Extrai o primeiro frame válido de um vídeo e salva como JPG."""
    cap = cv2.VideoCapture(caminho_entrada)
    if not cap.isOpened():
        raise ValueError("Não foi possível abrir o arquivo de vídeo.")
    
    # Tenta ler até encontrar um frame válido
    sucesso, frame = cap.read()
    cap.release()
    
    if sucesso:
        # O OpenCV já salva no formato correto e lida com a conversão de cores internamente no imwrite
        cv2.imwrite(caminho_saida, frame)
    else:
        raise ValueError("Não foi possível extrair nenhum frame do vídeo.")

def main():
    # Garante que a pasta de saída exista
    Path(PASTA_SAIDA).mkdir(parents=True, exist_ok=True)

    # Lista todos os arquivos da pasta de entrada
    if not os.path.exists(PASTA_ENTRADA):
        print(f"Erro: A pasta de entrada '{PASTA_ENTRADA}' não existe.")
        return

    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if os.path.isfile(os.path.join(PASTA_ENTRADA, f))]
    
    # Filtra apenas arquivos com extensões suportadas
    arquivos_suportados = []
    for f in arquivos:
        ext = os.path.splitext(f)[1].lower()
        if ext in EXTENSOES_IMAGEM or ext in EXTENSOES_VIDEO:
            arquivos_suportados.append(f)

    if not arquivos_suportados:
        print("Nenhuma imagem ou vídeo suportado encontrado na pasta de entrada.")
        return

    print(f"Encontrados {len(arquivos_suportados)} arquivos de mídia para conversão./n")

    contador_nome = 1
    arquivos_convertidos = []
    erros = []

    # Barra de progresso com tqdm
    for nome_arquivo in tqdm(arquivos_suportados, desc="Convertendo mídias", unit="arquivo"):
        caminho_entrada = os.path.join(PASTA_ENTRADA, nome_arquivo)
        extensao = os.path.splitext(nome_arquivo)[1].lower()

        # Descobre qual será o próximo nome disponível para evitar sobrescrever
        caminho_saida, contador_nome = obter_proximo_caminho(PASTA_SAIDA, PREFIXO_NOME, contador_nome)
        nome_arquivo_saida = os.path.basename(caminho_saida)

        try:
            if extensao in EXTENSOES_IMAGEM:
                processar_imagem(caminho_entrada, caminho_saida)
            elif extensao in EXTENSOES_VIDEO:
                processar_video(caminho_entrada, caminho_saida)
            
            arquivos_convertidos.append(f"[OK] {nome_arquivo} -> {nome_arquivo_saida}")
            contador_nome += 1 # Incrementa para a próxima iteração
            
        except Exception as e:
            erros.append(f"[ERRO] Falha ao converter {nome_arquivo}: {str(e)}")

    # ================= RESUMO FINAL =================
    print("/n--- RESUMO DA OPERAÇÃO ---")
    for msg in arquivos_convertidos:
        print(msg)
        
    if erros:
        print("/n--- ERROS ENCONTRADOS ---")
        for err in erros:
            print(err)

    print(f"/nProcesso concluído! {len(arquivos_convertidos)} arquivo(s) convertido(s) com sucesso e {len(erros)} erro(s).")

if __name__ == "__main__":
    main()