"""Build a clean ZIP and SHA256SUMS.txt. Excludes local Git and Python caches.
Run after regenerating CAD/viewer/docs. Uses only the Python standard library.
"""
from pathlib import Path
import hashlib,zipfile,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def sources():
    return sorted(q for q in ROOT.rglob('*') if q.is_file()
       and not any(n in q.parts for n in ['.git','__pycache__','.venv'])
       and q.suffix!='.pyc' and q.name!='SHA256SUMS.txt')
# Normalize tracked text to LF so the manifest survives Git checkout on Linux.
for q in sources():
    if q.suffix in ['.py','.json','.md','.txt','.html','.svg','.yml'] or q.name in ['LICENSE','.gitignore','.gitattributes']:
        q.write_bytes(q.read_bytes().replace(b'\r\n',b'\n'))
manifest='\n'.join(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+q.relative_to(ROOT).as_posix() for q in sources())+'\n'
(ROOT/'SHA256SUMS.txt').write_bytes(manifest.encode('ascii'))
subprocess.run([sys.executable,str(ROOT/'tools/check_release.py')],check=True)
version=json.loads((ROOT/'cad/parameters.json').read_text(encoding='utf-8'))['version']
dest=ROOT.parent/f'Doggie_House_v{version}_Git.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for q in [*sources(),ROOT/'SHA256SUMS.txt']:z.write(q,('doggie-house/'+q.relative_to(ROOT).as_posix()))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert not any('/.git/' in n or '__pycache__' in n for n in z.namelist())
print(json.dumps(dict(package=str(dest),files=len(sources())+1,bytes=dest.stat().st_size,integrity='PASS'),indent=2))
