from importlib import import_module
from threading import Thread

threads = [
    Thread(target=import_module, args=(a,), daemon=True)
    for a in ['send', 'recv']
]

[t.start() for t in threads]
[t.join() for t in threads]
