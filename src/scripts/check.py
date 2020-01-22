import sys
from filelock import FileLock, Timeout
from pathlib import Path

root_dir= Path(sys.path[0]).absolute()
p = Path("gpu.lock")
lock = FileLock(p)

try:
    with lock.acquire(1):
        #print('finalizado')
        sys.stdout.write('finalizado')
except Timeout:
    # print('processando')
    sys.stdout.write('processando')


# if r == 0:
#     sys.stdout.write('processando')
# elif r == 1:
#     sys.stdout.write('finalizado')
# elif r == 2:
#     sys.stdout.write('error')