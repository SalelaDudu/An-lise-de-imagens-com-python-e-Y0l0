from ultralytics import YOLO

# 1. Carrega o modelo base "Nano" (é o mais leve e rápido para treinarmos no seu PC)
modelo = YOLO('yolov8n.pt')

print("Iniciando o treinamento da IA...")

# 2. Inicia o processo de aprendizado
resultados = modelo.train(
    data='yolo_dataset/data.yaml', # O caminho para o "mapa" que criamos no passo anterior
    epochs=50,                     # Quantas vezes a IA vai revisar todas as fotos (50 é um ótimo começo)
    imgsz=640,                     # O tamanho padrão que ele vai redimensionar as fotos para aprender
    name='meu_modelo_maracuja',    # O nome da pasta onde ele vai salvar os resultados
    device='cpu'                   # Forçando o uso do processador (mude para 0 se você tiver uma placa de vídeo da NVIDIA configurada)
)

print("Treinamento concluído com sucesso!")