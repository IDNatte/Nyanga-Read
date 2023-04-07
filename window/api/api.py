import sys


class Api:
    def __init__(self):
        pass

    def ready(self):
        return {"message": f"Hello from python {sys.version_info}"}

    def getSvelteVersion(self, svelte_version):
        print(f"using svelte version {svelte_version}")
