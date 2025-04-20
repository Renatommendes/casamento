from django.shortcuts import render
from django.http import JsonResponse
import os
import time
import tempfile
import psutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

FOLDER_ID = '1wBUCgc5hGkSbhfbbeNhAURCIEcEdpQrl'

def wait_for_file_release(filepath, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_file_in_use(filepath):
            return True
        time.sleep(0.5)
    return False

def is_file_in_use(filepath):
    for proc in psutil.process_iter(['open_files']):
        try:
            if proc.info['open_files']:
                for file in proc.info['open_files']:
                    if file.path == filepath:
                        return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return False

def remove_file_safely(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"[DEBUG] Arquivo removido: {filepath}")
    else:
        print(f"[DEBUG] Arquivo não encontrado para remoção: {filepath}")

def upload_view(request):
    if request.method == 'POST' and request.FILES.getlist('arquivos'):
        arquivos = request.FILES.getlist('arquivos')
        mensagens = []

        try:
            print("[DEBUG] Iniciando upload de múltiplos arquivos")
            creds = service_account.Credentials.from_service_account_file('credencial.json')
            service = build('drive', 'v3', credentials=creds)

            for arquivo in arquivos:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in arquivo.chunks():
                        temp_file.write(chunk)
                    caminho_temp = temp_file.name

                print(f"[DEBUG] Arquivo temporário criado: {caminho_temp}")

                file_metadata = {
                    'name': arquivo.name,
                    'parents': [FOLDER_ID]
                }

                media = MediaFileUpload(caminho_temp, resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"[DEBUG] Upload realizado para o Google Drive. ID: {file.get('id')}")

                mensagens.append(f'{arquivo.name} enviado com sucesso!')

                if wait_for_file_release(caminho_temp):
                    remove_file_safely(caminho_temp)
                else:
                    print(f"[DEBUG] Arquivo {arquivo.name} ainda está em uso após o tempo limite.")

            return JsonResponse({
                'mensagem': 'Arquivos enviados com sucesso!',
                'detalhes': mensagens
            })

        except Exception as e:
            print(f"[ERRO] Durante o upload: {str(e)}")
            return JsonResponse({'erro': f'Erro no upload: {str(e)}'}, status=500)

    return render(request, 'upload_form.html')
