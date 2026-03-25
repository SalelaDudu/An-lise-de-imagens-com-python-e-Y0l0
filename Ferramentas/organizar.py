import os
import shutil

# Nomes das pastas padrão do YOLOv8
base_dir = 'yolo_dataset'
img_dir = os.path.join(base_dir, 'images', 'train')
lbl_dir = os.path.join(base_dir, 'labels', 'train')

# Cria a estrutura de pastas nova
os.makedirs(img_dir, exist_ok=True)
os.makedirs(lbl_dir, exist_ok=True)

print("Lendo as classes...")
with open('obj.names', 'r') as f:
    classes = [linha.strip() for linha in f.readlines() if linha.strip()]

print(f"Encontradas {len(classes)} classes: {classes}")
print("Copiando e separando arquivos... (Isso pode levar alguns segundos)")

# Copia e separa imagens e labels
pasta_origem = 'obj_train_data'
for arquivo in os.listdir(pasta_origem):
    caminho_completo = os.path.join(pasta_origem, arquivo)
    
    # Se for imagem, vai para a pasta images
    if arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        shutil.copy(caminho_completo, os.path.join(img_dir, arquivo))
    # Se for texto, vai para a pasta labels
    elif arquivo.lower().endswith('.txt'):
        shutil.copy(caminho_completo, os.path.join(lbl_dir, arquivo))

# Cria o cérebro do dataset: o arquivo data.yaml
caminho_absoluto = os.path.abspath(base_dir).replace('\\', '/')
yaml_content = f"""
path: {caminho_absoluto}
train: images/train
val: images/train  # Usando os mesmos dados para validação neste primeiro teste
nc: {len(classes)}
names: {classes}
"""

with open(os.path.join(base_dir, 'data.yaml'), 'w') as f:
    f.write(yaml_content.strip())

print("\nSUCESSO! Sua pasta 'yolo_dataset' está pronta para o treinamento.")