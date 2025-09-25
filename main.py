from dotenv import load_dotenv
load_dotenv()
from utils.Logger import Logger
from workflow.get_streams import get_streams
from workflow.extract_streams import *
import pymsgbox
import os


def main():
    logger = Logger()

    # Carrega variáveis de ambiente
    arquivo_mxf = os.getenv("ARQUIVO_MXF")

    try:
        # Obter streams do arquivo MXF
        streams = get_streams(arquivo_mxf)

        if not streams:
            logger.registrar_erro("❌ Nenhum stream encontrado no arquivo MXF.")
            return

        logger.registrar_info(f"📊 Encontradas {len(streams)} streams no MXF.")

        # Processar streams de áudio
        extrair_audio(streams)

    except Exception as e:
        logger.registrar_erro(f"❌ Erro inesperado: {e}")
        pymsgbox.alert("Erro ao tentar executar o processo.")
        return

    # Finalização
    logger.registrar_info("\n✅ Processamento concluído!")
    pymsgbox.alert("Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()
