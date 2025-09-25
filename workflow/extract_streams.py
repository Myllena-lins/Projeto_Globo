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


# Separa áudio em stems usando Demucs
def separar_com_demucs(audio_path):
    logger.registrar_info(f"🎶 Separando fontes com Demucs: {audio_path}")

    # Demucs gera saída em ./separated/<modelo>/<arquivo>
    cmd = ["demucs", "-o", pasta_saida, audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.registrar_erro(f"❌ Erro ao rodar Demucs: {result.stderr}")
        return None

    # Caminho de saída do Demucs
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_dir = os.path.join(pasta_saida, "htdemucs", base_name)

    vocals = os.path.join(output_dir, "vocals.wav")
    drums = os.path.join(output_dir, "drums.wav")
    bass = os.path.join(output_dir, "bass.wav")
    other = os.path.join(output_dir, "other.wav")

    logger.registrar_info(f"🎤 Voz: {vocals}")
    logger.registrar_info(f"🥁 Bateria: {drums}")
    logger.registrar_info(f"🎸 Baixo: {bass}")
    logger.registrar_info(f"🎼 Outros: {other}")

    return {
        "vocals": vocals,
        "drums": drums,
        "bass": bass,
        "other": other
    }


# Decide se usa ffmpeg direto ou Demucs
def processar_streams(streams):
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    if len(audio_streams) > 1:
        logger.registrar_info("📡 Mais de uma stream encontrada → usando ffmpeg normal.")
        for stream in audio_streams:
            indice = stream["index"]
            codec = stream["codec_name"]
            canais = stream.get("channels", "desconhecido")
            extrair_audio(indice, codec, canais)

    elif len(audio_streams) == 1:
        logger.registrar_info("🎧 Apenas 1 stream encontrada → usando ffmpeg + Demucs.")
        stream = audio_streams[0]
        indice = stream["index"]
        codec = stream["codec_name"]
        canais = stream.get("channels", "desconhecido")

        wav_extraido = extrair_audio(indice, codec, canais)
        if wav_extraido:
            separar_com_demucs(wav_extraido)

    else:
        logger.registrar_erro("❌ Nenhuma stream de áudio encontrada!")
