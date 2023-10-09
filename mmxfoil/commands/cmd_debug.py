# cmd_debug.py


class Plugin:
    """debug command plugin"""

    help = "toggle application debug flag"
    name = "debug"

    def process(self, ctx):
        """flip current debug flag setting"""
        ctx.debug = not ctx.debug
        if ctx.debug:
            flag = "on"
        else:
            flag = "off"
        print(f"debug flag is {flag}")
        ctx.argcount += 1
