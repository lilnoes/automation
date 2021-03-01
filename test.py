import subprocess
d = subprocess.run("ls -t /home/leon | grep '.png'", capture_output=True, shell=True, encoding="utf-8")
d = d.stdout.split("\n")
print(d[0])