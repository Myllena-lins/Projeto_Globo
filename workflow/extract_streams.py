import subprocess
import os
from dotenv import load_dotenv
from utils.Logger import Logger

logger = Logger()

load_dotenv()
ffmpeg_path = os.getenv('FFMPEG_PATH')
arquivo_mxf = os.getenv('ARQUIVO_MXF')
pasta_saida = os.getenv('PASTA_SAIDA')

# Extrai um stream de áudio específico para WAV
def extrair_audio(indice, codec, canais):
    saida_wav = os.path.join(pasta_saida, f'audio_{indice}_{canais}c_{codec}.wav')

    cmd_extract = [
        ffmpeg_path,
        '-i', arquivo_mxf,
        '-map', f'0:{indice}',
        '-c:a', 'pcm_s16le',  # Garante formato WAV compatível
        '-y',
        saida_wav
    ]

    result_extract = subprocess.run(cmd_extract, capture_output=True, text=True)
    if result_extract.returncode != 0:
        logger.registrar_erro(f"❌ Erro ao extrair stream {indice}: {result_extract.stderr}")
        return None
    else:
        logger.registrar_info(f"✅ Stream {indice} extraída com sucesso: {saida_wav}")
        return saida_wav