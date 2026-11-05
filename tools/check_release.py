"""Check repository links, CAD/viewer freshness, export inventory and checksums."""
from pathlib import Path
import sys,json,re,hashlib,base64,struct,argparse
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--skip-checksums',action='store_true')
args=parser.parse_args()
report=json.loads((ROOT/'docs/validation.json').read_text(encoding='utf-8'))
p=json.loads((ROOT/'cad/parameters.json').read_text(encoding='utf-8'))
assert all(report['checks'].values()),'Failed CAD check'
assert len(report['meshes'])==12
digest=hashlib.sha256(b''.join((ROOT/'cad'/n).read_text(encoding='utf-8').replace('\r\n','\n').encode('utf-8') for n in ['model.py','build.py','parameters.json'])).hexdigest()
assert digest==report['source_sha256'],'CAD report stale; run cad/build.py'
html=(ROOT/'viewer/index.html').read_text(encoding='utf-8')
match=re.search(r'<script type="application/json" id="scene">(.*?)</script>',html,re.S)
assert match,'Viewer scene missing'
scene=json.loads(match.group(1))
assert scene['version']==p['version'] and scene['source_sha256']==digest,'Viewer stale'
assert len(scene['parts'])==26
for part in scene['parts']:
    raw=base64.b64decode(part['geometry'],validate=True)
    assert len(raw)>0 and len(raw)%(8*3*4)==0
    assert all(abs(v)<1e6 for v in struct.unpack('<'+'f'*(len(raw)//4),raw))
assert '__SCENE__' not in html
template=(ROOT/'viewer/template.html').read_text(encoding='utf-8')
assert html==template.replace('__SCENE__',match.group(1)),'Viewer template stale'
publication=json.loads((ROOT/'publication.json').read_text(encoding='utf-8'))
assert publication['geometry_revision']==p['version'],'Publication geometry revision mismatch'
assert not re.search(r'<script[^>]+src=',html,re.I),'Viewer must work offline'
assert len(list((ROOT/'models/stl').glob('*.stl')))==12
assert len(list((ROOT/'models').glob('*.3mf')))==2
assert (ROOT/'docs/GUIA_MONTAJE_ES.pdf').stat().st_size>10000

def local_link(source,target):
    target=target.split('#')[0].split('?')[0]
    if not target or re.match(r'(https?:|mailto:|data:|javascript:)',target):return
    assert '%' not in target,'Encoded local path needs explicit checking'
    resolved=(source.parent/target).resolve()
    assert resolved.is_relative_to(ROOT),f'Link escapes repo: {source}:{target}'
    assert resolved.exists(),f'Broken link: {source.relative_to(ROOT)} -> {target}'

links=0
for source in ROOT.rglob('*.md'):
    if '.git' in source.parts:continue
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',source.read_text(encoding='utf-8')):
        local_link(source,target);links+=1
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for name,value in attrs:
            if name in ('src','href'):local_link(self.source,value)
for source in [ROOT/'index.html',ROOT/'viewer/index.html']:
    check=Links();check.source=source;check.feed(source.read_text(encoding='utf-8'))

def files():
    return sorted(q for q in ROOT.rglob('*') if q.is_file()
       and not any(n in q.parts for n in ['.git','__pycache__','.venv'])
       and q.suffix!='.pyc' and q.name!='SHA256SUMS.txt')
if not args.skip_checksums:
    manifest=ROOT/'SHA256SUMS.txt'
    assert manifest.exists(),'Run tools/package_release.py to create checksums'
    indexed={}
    for line in manifest.read_text(encoding='ascii').splitlines():
        sha,name=line.split('  ',1);indexed[name]=sha
    assert set(indexed)=={q.relative_to(ROOT).as_posix() for q in files()},'Manifest inventory mismatch'
    for q in files():assert hashlib.sha256(q.read_bytes()).hexdigest()==indexed[q.relative_to(ROOT).as_posix()],q
print(json.dumps(dict(status='PASS',version=p['version'],stl=12,layouts=2,
    viewer_parts=len(scene['parts']),markdown_links=links,
    source_and_viewer_fresh=True,checksums_checked=not args.skip_checksums),indent=2))
