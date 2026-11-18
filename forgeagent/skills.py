"""Minimal safe Agent Skills frontmatter reader; skill text remains untrusted data."""
from pathlib import Path
import re

NAME=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
class SkillError(ValueError): pass

def _directory(directory):
    original=Path(directory).absolute()
    current=Path(original.anchor)
    for part in original.parts[1:]:
        current=current/part
        if current.is_symlink(): raise SkillError('symlink skill path rejected')
    root=original.resolve(strict=True)
    if not root.is_dir(): raise SkillError('skill directory required')
    return root

def load_skill(directory):
    root=_directory(directory); file=root/'SKILL.md'
    if file.is_symlink() or not file.is_file(): raise SkillError('regular SKILL.md required')
    with file.open('rb') as stream: encoded=stream.read(256_001)
    if len(encoded)>256_000: raise SkillError('skill too large')
    raw=encoded.decode('utf-8')
    if not raw.startswith('---\n'): raise SkillError('frontmatter required')
    end=raw.find('\n---\n',4)
    if end<0: raise SkillError('unterminated frontmatter')
    fields={}
    for line in raw[4:end].splitlines():
        if not line or line.lstrip().startswith('#'): continue
        if line[:1].isspace() or ':' not in line: raise SkillError('unsupported frontmatter syntax')
        key,value=line.split(':',1);value=value.strip()
        if key in fields or key not in {'name','description','license','compatibility','allowed-tools'}: raise SkillError('duplicate or unsupported field')
        if value.startswith(('"',"'")):
            if len(value)<2 or value[-1]!=value[0]: raise SkillError('invalid quoted scalar')
            value=value[1:-1]
        fields[key]=value
    name=fields.get('name','');desc=fields.get('description','')
    if not NAME.fullmatch(name) or len(name)>64 or '--' in name or name!=root.name: raise SkillError('invalid skill name')
    if not desc or len(desc)>1024: raise SkillError('invalid skill description')
    return {'name':name,'description':desc,'body':raw[end+5:],'trusted':False}

def load_reference(directory,relative,max_bytes=32768):
    """Load one progressive reference by explicit relative path, without execution."""
    root=_directory(directory);rel=Path(relative)
    if type(max_bytes) is not int or not 1<=max_bytes<=256_000: raise SkillError('invalid reference byte limit')
    if rel.is_absolute() or '..' in rel.parts: raise SkillError('reference escape')
    path=root/rel;current=root
    for part in rel.parts:
        current=current/part
        if current.is_symlink(): raise SkillError('symlink reference rejected')
    resolved=path.resolve(strict=True)
    if root not in resolved.parents or not resolved.is_file(): raise SkillError('reference outside skill')
    with resolved.open('rb') as stream:data=stream.read(max_bytes+1)
    if len(data)>max_bytes: raise SkillError('reference too large')
    return data.decode('utf-8')
