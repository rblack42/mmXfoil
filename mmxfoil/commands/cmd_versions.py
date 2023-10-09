# cmd_versions.py
from mmqprop import version


class Plugin:
    """version command plugin"""

    help = "display dependency versions"
    name = "versions"

    def process(self, ctx):
        """fetch and display dependency versions"""
        v = version()
        print(f"Dependency versions for mmqprop {v}")
        ctx.argcount += 1
