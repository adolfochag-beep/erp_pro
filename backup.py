import shutil
import os

from datetime import datetime


def gerar_backup():

    os.makedirs(
        "backups",
        exist_ok=True
    )

    data = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    origem = "databases"

    destino = (
        f"backups/backup_{data}"
    )

    shutil.copytree(
        origem,
        destino
    )

    return destino