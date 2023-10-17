#!/usr/bin/python3
"""implementing the console"""

import cmd


class TaskHubCommand(cmd.Cmd):
    """a command processor for the TaskHub"""
    prompt = "(TaskHub) "

    def do_EOF(self, line) -> bool:
        """exit console with """
        return True
    
    def do_quit(self, line) -> bool:
        """exit program with with EOF(ctrl + d)"""
        return True
    
    def emptyline(self) -> bool:
        """overwrites default method emptyline"""
        return False
    
if __name__ == "__main__":
    TaskHubCommand().cmdloop()