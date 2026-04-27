import psycopg2._psycopg as ext
import ctypes, os

# Verifica o caminho do libpq.dll que está sendo usado
import psycopg2
print('psycopg2 path:', psycopg2.__file__)

# Tenta pegar o diretório de dados do postgres
for key in sorted(os.environ.keys()):
    if 'PG' in key or 'POST' in key.upper():
        print(f'{key} = {os.environ[key]}')