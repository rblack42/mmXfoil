import sys
import os
import importlib

from .Context import Context


class CLI(object):
    """Primitive event loop for commandline"""

    app_debug = False

    def __init__(self, debug):
        """Load plugins and set command loop"""
        self.plugins = {}
        self.ctx = Context()
        self.ctx.argcount = 0
        self.ctx.debug = debug

        # scan the plugins directory for commands ---------------
        f = []
        cwd = os.path.abspath(os.path.dirname(__file__))
        ppath = os.path.join(cwd, "commands")
        sys.path.append(ppath)
        if self.ctx.debug:
            print("added:", ppath)
        for (dirpath, dirnames, filenames) in os.walk(ppath):
            f.extend(filenames)
            break  # stop loop after files are available

        # import found plugins, save in plugins dict
        for p in f:
            if not p.startswith("cmd_"):
                continue
            pname = p[:-3]
            if self.ctx.debug:
                print("checking", pname)
            # import cmd file, skip if import fails
            try:
                m = importlib.import_module(pname)
                self.plugins[pname[4:]] = m
                if self.ctx.debug:
                    print("added", pname)
            except ImportError:
                if self.ctx.debug:
                    print("import failed")
        if self.ctx.debug:
            print("Active plugins:", self.plugins)

        # configure command loop -----------------------------
        self.running = True

    def run(self):
        while self.running:
            print(">", end=" ")
            command = input()
            self.process_command(command)

        print("Program terminating...")
        sys.exit()

    def process_command(self, cmd):
        if self.ctx.debug:
            print(f"processing cmd {cmd}")
        if cmd == "quit":
            self.running = False
            return
        if cmd == "help":
            print("help - available commands:")
            for c in self.plugins:
                p = self.plugins[c].Plugin()
                help = p.help
                print("\t", p.name, "-", help)
                print("\t", "quit - terminate program")
            return

        if cmd in self.plugins:
            m = self.plugins[cmd].Plugin()
            if self.ctx.debug:
                p = self.plugins[cmd].Plugin()
                print(f"calling cmd plugin: {cmd}")
            m.process(self.ctx)
            if self.ctx.debug:
                print("completed cmd:", self.ctx.argcount)
        else:
            print(f"{cmd} not recognized - try 'help'")


if __name__ == "__main__":
    cli = CLI(False)
    cli.run()
