import json, subprocess
from pathlib import Path
plan=json.loads(Path('content/attention-trap-v3-scenes.json').read_text(encoding='utf-8'))
narration='. '.join(scene['narration'] for scene in plan)
out=Path('renders/comic/narration.wav')
out.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['espeak-ng','-v','en-us','-s','132','-w',str(out),narration],check=True)
print(f'Generated narration for {len(plan)} JSON scenes: {out}')
