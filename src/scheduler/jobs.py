import logging
from services.stock_data_service import collect_stock_data

logger = logging.getLogger(__name__)


def collect_stock_data_job(save_to_db: bool = True):
    """
    Job para coletar dados de ações periodicamente

    Args:
        save_to_db: Se True, salva no banco. Se False, apenas exibe no console.
    """
    try:
        mode = "salvando no banco" if save_to_db else "exibindo no console"
        logger.info(f"=== Iniciando job de coleta de dados de ações ({mode}) ===")
        results = collect_stock_data(save_to_db=save_to_db)

        # Log do resultado
        success_count = sum(1 for r in results if r["success"])
        logger.info(
            f"=== Job finalizado: {success_count}/{len(results)} tickers bem-sucedidos ==="
        )

        return results

    except Exception as e:
        logger.error(f"Erro crítico no job de coleta: {e}", exc_info=True)
        return []
