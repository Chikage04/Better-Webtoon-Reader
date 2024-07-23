import subprocess

with open('output.log', 'w') as f:
    subprocess.run(
        ['python3', './imgur.py'],
        stdout=f,
        stderr=subprocess.STDOUT,
        check=True
    )
