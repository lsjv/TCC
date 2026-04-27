import os
for key in ['PGPASSWORD', 'PGUSER', 'PGHOST', 'PGDATABASE', 'PGPASSFILE', 'APPDATA', 'USERPROFILE']:
    val = os.environ.get(key)
    if val:
        print(f'{key} = {val}')
        encoded = val.encode('latin-1', errors='replace')
        print(f'  bytes: {encoded}')
        print(f'  len: {len(val)}')