"""Static public-package checks; not platform approval or human acceptance."""
from pathlib import Path
import hashlib
import json
import re
import struct

ROOT = Path(__file__).parent
for package, expected in [('tok-studio',3), ('physics-studio',7)]:
    base = ROOT / 'plugins' / package
    manifest = json.loads((base / 'plugin.json').read_text())
    legacy = json.loads((base / '.codex-plugin/plugin.json').read_text())
    assert manifest['name'] == package == legacy['name']
    assert manifest['version'] == legacy['version']
    assert manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert not (base / '.app.json').exists()
    for doc in (manifest, legacy):
        assert not doc.get('apps')
        assert not doc.get('extensions', {}).get('com.openai', {}).get('apps')
        assert not doc.get('author',{}).get('email')
    ui = manifest['extensions']['com.openai']['interface']
    assert ui == legacy['interface']
    assert len(ui['displayName']) <= 30 and len(ui['shortDescription']) <= 30
    assert len(ui['longDescription']) <= 4000
    prompts = ui['defaultPrompt']
    assert len(prompts) <= 3 and len(set(prompts)) == len(prompts)
    assert all(len(p) <= 128 and '\n' not in p for p in prompts)
    for key in ('websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL'):
        assert ui[key].startswith('https://github.com/Arnie016/education-studio-plugins/blob/main/docs/')
        assert len(ui[key]) <= 1024
    assert manifest['extensions']['com.openai']['publication']['countries'] == []
    icons = []
    for key, minimum in [('logo',256), ('composerIcon',48)]:
        file = (base / ui[key]).resolve()
        assert file.is_relative_to(base) and file.exists()
        raw = file.read_bytes()
        assert raw[:8] == b'\x89PNG\r\n\x1a\n' and len(raw) <= 5 * 1024 * 1024
        width, height = struct.unpack('>II', raw[16:24])
        assert width == height and width >= minimum and width <= 4096
        icons.append({'field':key,'width':width,'height':height})
    skills = sorted(base.glob('skills/*/SKILL.md'))
    assert len(skills) == expected
    for skill in skills:
        text = skill.read_text()
        assert text.startswith('---\n')
        assert re.search(r'^name:\s*\S', text, re.M)
        assert re.search(r'^description:\s*\S', text, re.M)
    for file in base.rglob('*'):
        assert not file.is_symlink()
        if file.is_file():
            assert file.name not in ('.env','.DS_Store')
            if file.suffix in ('.md','.json','.py','.yaml'):
                text = file.read_text()
                assert not re.search(r'-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:sk_live_|whsec_)[A-Za-z0-9]+', text)
    print(json.dumps({'package':package,'version':manifest['version'],'skills':len(skills),
                      'static_checks':'PASS','icons':icons,'directory_submission':'NOT_SUBMITTED'}))
