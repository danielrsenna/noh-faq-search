import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

def supabase_client() -> Client:
    """Inicializa e retorna o cliente Supabase."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL ou SUPABASE_KEY não configuradas corretamente.")

    return create_client(supabase_url, supabase_key)
