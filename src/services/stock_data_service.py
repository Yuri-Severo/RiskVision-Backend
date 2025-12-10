import logging
import time
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import yfinance as yf

from database import SessionLocal
from models.historyModel import History
from schemas.historySchema import HistoryCreate
from config.settings import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class StockDataService:
    """Serviço para coletar e armazenar dados de ações do yFinance"""

    @staticmethod
    def fetch_stock_data(
        ticker: str, period: str = "1d", interval: str = "1m"
    ) -> Optional[List[dict]]:
        """
        Busca dados de ações do yFinance

        Args:
            ticker: Símbolo da ação (ex: AAPL)
            period: Período de dados (1d, 5d, 1mo, etc)
            interval: Intervalo dos dados (1m, 5m, 1h, 1d, etc)

        Returns:
            Lista de dicionários com dados da ação ou None em caso de erro
        """
        try:
            logger.info(
                f"Buscando dados para {ticker} (period={period}, interval={interval})"
            )

            # Buscar dados do ticker
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period, interval=interval)

            if hist.empty:
                logger.warning(f"Nenhum dado encontrado para {ticker}")
                return None

            # Formatar dados
            stock_data = []
            for index, row in hist.iterrows():
                try:
                    data_point = {
                        "ticker_name": ticker.upper(),
                        "date": index.to_pydatetime(),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"]),
                        "dividends": float(row["Dividends"]),
                        "stock_splits": float(row["Stock Splits"]),
                    }
                    stock_data.append(data_point)
                except (KeyError, ValueError) as e:
                    logger.error(f"Erro ao processar linha de dados para {ticker}: {e}")
                    continue

            logger.info(f"Coletados {len(stock_data)} registros para {ticker}")
            return stock_data

        except Exception as e:
            logger.error(f"Erro ao buscar dados do yFinance para {ticker}: {e}")
            return None

    @staticmethod
    def save_to_database(stock_data: List[dict], db: Session) -> tuple[int, int]:
        """
        Salva dados de ações no banco de dados

        Args:
            stock_data: Lista de dicionários com dados das ações
            db: Sessão do banco de dados

        Returns:
            Tupla (sucessos, duplicados/erros)
        """
        success_count = 0
        duplicate_count = 0

        for data in stock_data:
            try:
                # Validar com schema Pydantic
                history_create = HistoryCreate(**data)

                # Criar registro no banco
                history = History(**history_create.model_dump())
                db.add(history)
                db.commit()

                success_count += 1
                logger.debug(f"Salvo: {data['ticker_name']} em {data['date']}")

            except IntegrityError:
                # Registro duplicado (violação da constraint UNIQUE)
                db.rollback()
                duplicate_count += 1
                logger.debug(f"Duplicado: {data['ticker_name']} em {data['date']}")

            except Exception as e:
                db.rollback()
                duplicate_count += 1
                logger.error(f"Erro ao salvar registro: {e}")

        return success_count, duplicate_count

    @staticmethod
    def collect_and_display_ticker(
        ticker: str,
        period: Optional[str] = None,
        interval: Optional[str] = None,
        max_retries: Optional[int] = None,
    ) -> dict:
        """
        Coleta e EXIBE dados de um ticker específico no console (SEM SALVAR NO BANCO)

        Args:
            ticker: Símbolo da ação
            period: Período de dados (usa settings se None)
            interval: Intervalo dos dados (usa settings se None)
            max_retries: Número máximo de tentativas (usa settings se None)

        Returns:
            Dicionário com resultado da operação
        """
        period = period or settings.STOCK_COLLECTION_PERIOD
        interval = interval or settings.STOCK_DATA_INTERVAL
        max_retries = max_retries or settings.MAX_RETRY_ATTEMPTS

        result = {
            "ticker": ticker,
            "success": False,
            "records_fetched": 0,
            "error": None,
        }

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Tentativa {attempt}/{max_retries} para {ticker}")

                # Buscar dados
                stock_data = StockDataService.fetch_stock_data(ticker, period, interval)

                if not stock_data:
                    result["error"] = "Nenhum dado encontrado"
                    if attempt < max_retries:
                        time.sleep(settings.RETRY_DELAY_SECONDS)
                        continue
                    break

                # APENAS EXIBIR NO CONSOLE (NÃO SALVAR)
                logger.info(f"\n{'='*80}")
                logger.info(f"📊 DADOS COLETADOS PARA {ticker}")
                logger.info(f"{'='*80}")

                for idx, data in enumerate(stock_data, 1):
                    logger.info(f"\n[{idx}/{len(stock_data)}] {data['date']}")
                    logger.info(f"  Open:   ${data['open']:.2f}")
                    logger.info(f"  High:   ${data['high']:.2f}")
                    logger.info(f"  Low:    ${data['low']:.2f}")
                    logger.info(f"  Close:  ${data['close']:.2f}")
                    logger.info(f"  Volume: {data['volume']:,}")
                    if data["dividends"] > 0:
                        logger.info(f"  Dividends: ${data['dividends']:.4f}")
                    if data["stock_splits"] > 0:
                        logger.info(f"  Stock Splits: {data['stock_splits']}")

                logger.info(f"\n{'='*80}")
                logger.info(
                    f"✓ Total de {len(stock_data)} registros exibidos para {ticker}"
                )
                logger.info(f"{'='*80}\n")

                result["success"] = True
                result["records_fetched"] = len(stock_data)
                break

            except Exception as e:
                logger.error(f"Erro na tentativa {attempt} para {ticker}: {e}")
                result["error"] = str(e)

                if attempt < max_retries:
                    time.sleep(settings.RETRY_DELAY_SECONDS)
                    continue
                break

        return result

    @staticmethod
    def collect_and_save_ticker(
        ticker: str,
        period: Optional[str] = None,
        interval: Optional[str] = None,
        max_retries: Optional[int] = None,
    ) -> dict:
        """
        Coleta e salva dados de um ticker específico com retry logic

        Args:
            ticker: Símbolo da ação
            period: Período de dados (usa settings se None)
            interval: Intervalo dos dados (usa settings se None)
            max_retries: Número máximo de tentativas (usa settings se None)

        Returns:
            Dicionário com resultado da operação
        """
        period = period or settings.STOCK_COLLECTION_PERIOD
        interval = interval or settings.STOCK_DATA_INTERVAL
        max_retries = max_retries or settings.MAX_RETRY_ATTEMPTS

        result = {
            "ticker": ticker,
            "success": False,
            "records_saved": 0,
            "duplicates": 0,
            "error": None,
        }

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Tentativa {attempt}/{max_retries} para {ticker}")

                # Buscar dados
                stock_data = StockDataService.fetch_stock_data(ticker, period, interval)

                if not stock_data:
                    result["error"] = "Nenhum dado encontrado"
                    if attempt < max_retries:
                        time.sleep(settings.RETRY_DELAY_SECONDS)
                        continue
                    break

                # Salvar no banco
                db = SessionLocal()
                try:
                    success, duplicates = StockDataService.save_to_database(
                        stock_data, db
                    )

                    result["success"] = True
                    result["records_saved"] = success
                    result["duplicates"] = duplicates

                    logger.info(
                        f"✓ {ticker}: {success} salvos, {duplicates} duplicados"
                    )
                    break

                finally:
                    db.close()

            except Exception as e:
                logger.error(f"Erro na tentativa {attempt} para {ticker}: {e}")
                result["error"] = str(e)

                if attempt < max_retries:
                    time.sleep(settings.RETRY_DELAY_SECONDS)
                    continue
                break

        return result

    @staticmethod
    def collect_all_tickers(save_to_db: bool = True) -> List[dict]:
        """
        Coleta dados de todos os tickers configurados

        Args:
            save_to_db: Se True, salva no banco. Se False, apenas exibe no console.

        Returns:
            Lista com resultados de cada ticker
        """
        tickers = settings.get_tickers_list()

        if not tickers:
            logger.warning("Nenhum ticker configurado em STOCK_TICKERS")
            return []

        mode = "salvar no banco" if save_to_db else "exibir no console"
        logger.info(
            f"Iniciando coleta para {len(tickers)} ticker(s): {', '.join(tickers)} (modo: {mode})"
        )

        results = []
        for ticker in tickers:
            if save_to_db:
                result = StockDataService.collect_and_save_ticker(ticker)
            else:
                result = StockDataService.collect_and_display_ticker(ticker)
            results.append(result)

        # Resumo
        successful = sum(1 for r in results if r["success"])

        if save_to_db:
            total_saved = sum(r.get("records_saved", 0) for r in results)
            total_duplicates = sum(r.get("duplicates", 0) for r in results)
            logger.info(
                f"Coleta finalizada: {successful}/{len(tickers)} tickers bem-sucedidos, "
                f"{total_saved} registros salvos, {total_duplicates} duplicados"
            )
        else:
            total_fetched = sum(r.get("records_fetched", 0) for r in results)
            logger.info(
                f"Coleta finalizada: {successful}/{len(tickers)} tickers bem-sucedidos, "
                f"{total_fetched} registros exibidos (NÃO SALVOS)"
            )

        return results


# Função auxiliar para uso rápido
def collect_stock_data(save_to_db: bool = True):
    """
    Função helper para executar coleta de todos os tickers

    Args:
        save_to_db: Se True (padrão), salva no banco. Se False, apenas exibe.
    """
    return StockDataService.collect_all_tickers(save_to_db=save_to_db)
