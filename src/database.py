from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os
import sys

# Carregar variáveis de ambiente
load_dotenv()

# Ler e sanitizar DATABASE_URL
raw = os.getenv("DATABASE_URL", "")
DATABASE_URL = raw.strip().strip('"').strip("'")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no arquivo .env")

# Debug: mostrar a URL lida (mascarando senha)
masked_url = DATABASE_URL
if "@" in DATABASE_URL and ":" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    if len(parts) == 2:
        user_pass = parts[0].split("//")[-1]
        if ":" in user_pass:
            user = user_pass.split(":")[0]
            masked_url = DATABASE_URL.replace(user_pass, f"{user}:***")

print(f"DATABASE_URL lida: {masked_url}", file=sys.stderr)

def _make_engine(url_str: str):
    """
    Cria engine do SQLAlchemy com fallback para problemas de encoding
    """
    try:
        engine = create_engine(
            url_str, 
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
        # Testa a conexão de forma mais simples
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco estabelecida com sucesso!", file=sys.stderr)
        except Exception as test_err:
            print(f"⚠️  Aviso: Não foi possível testar conexão: {test_err}", file=sys.stderr)
            print("   Mas prosseguindo... a conexão será testada quando necessário.", file=sys.stderr)
            
        return engine
        
    except UnicodeDecodeError as e:
        print(f"❌ UnicodeDecodeError no DSN: {e}", file=sys.stderr)
        print("🔄 Tentando fallback com URL.create()...", file=sys.stderr)
        
        # Fallback: reconstruir URL usando variáveis individuais
        host = os.getenv("POSTGRES_HOST", "localhost")
        port_str = os.getenv("POSTGRES_PORT", "5432")
        
        # Validar porta
        try:
            port = int(port_str)
        except ValueError:
            print(f"⚠️  POSTGRES_PORT inválida: {port_str}, usando 5432", file=sys.stderr)
            port = 5432
            
        user = os.getenv("POSTGRES_USER", "postgres")
        pwd = os.getenv("POSTGRES_PASSWORD", "")
        db = os.getenv("POSTGRES_DB", "postgres")
        
        safe_url = URL.create(
            drivername="postgresql+psycopg2",
            username=user,
            password=pwd,
            host=host,
            port=port,
            database=db,
        )
        
        print(f"🔧 URL reconstruída: postgresql://{user}:***@{host}:{port}/{db}", file=sys.stderr)
        
        engine = create_engine(
            safe_url, 
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
        # Testa a conexão do fallback
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Conexão estabelecida via fallback!", file=sys.stderr)
        except Exception as test_err:
            print(f"⚠️  Aviso: Não foi possível testar conexão do fallback: {test_err}", file=sys.stderr)
            
        return engine
        
    except Exception as e:
        print(f"❌ Erro ao criar engine: {e}", file=sys.stderr)
        print("ℹ️  Continuando... A conexão será testada quando a API for usada.", file=sys.stderr)
        # Não lance a exceção aqui para permitir que a API suba
        return create_engine(url_str, pool_pre_ping=True)

# Criar engine
engine = _make_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
)

# Base para modelos
Base = declarative_base()

def get_db():
    """
    Dependency para obter sessão do banco
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()