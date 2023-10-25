#!/usr/bin/python3
"""implementing the console"""

import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.messages import Message
from models.notifications import Notification
from models.tasks import Task
from models.users import User


class TaskHubCommand(cmd.Cmd):
    """a command processor for the TaskHub"""
    prompt = "(TaskHub) " if sys.__stdin__.isatty() else ""
    __classes = {"BaseModel": BaseModel, "Message": Message,
               "Notification": Notification, "Task": Task,
               "User": User}

    def precmd(self, line: str) -> str:
        """checks line for basic syntax"""
        args = line.split(" ")
        length = len(args)
        commands = ["create", "update", "show",
                    "destroy", "count"]
        try:
            if args[0] not in commands:
                return line
            if length < 2:
                print("** class name missing **")
                return super().cmdloop()
            if args[1] not in self.__classes:
                print("** class doesn't exist **")
                return super().cmdloop()
            return line
        except KeyboardInterrupt:
            exit()


    def do_EOF(self, line: str):
        """exit console"""
        exit()
    
    def help_EOF(self):
        """help documentation fro EOF"""
        print("Exit console from SIGINT")
    
    def do_quit(self, line: str):
        """exit program with with EOF(ctrl + d)"""
        exit()
    
    def help_quit(self):
        """help documentation for quit"""
        print("Exit console")
    
    def emptyline(self) -> bool:
        """overwrites default method emptyline"""
        return False

    def do_create(self, line: str):
        """create a new instance of particular class"""
        args = line.split(" ")
        kwargs = {}
        length = len(args)
        i = 0
        while i < length:
            if ('"' in args[i]) and (args[i].count('"') != 2):
                j = i
                i += 1
                index = args[j].find('"')
                args[j] = args[j][:index] + args[j][(index + 1):]
                while (i < length) and (args[i].endswith('"') is False):
                    args[j] += " " + args[i]
                    args.pop(i)
                    length -= 1
                    i += 1
                if i < length and args[i].endswith('"'):
                    args[j] += " " + args[i]
                    args[j] = args[j][:-1]
                    args.pop(i)
                    length -= 1
            else:
                i += 1
        if length > 1:
            for i in range(1, length):
                pair = args[i].partition("=")
                if len(pair) < 3:
                    kwargs[pair[0]] = ""
                else:
                    kwargs[pair[0]] = pair[2]
            new_instance = self.__classes[args[0]](**kwargs)
        else:
            new_instance = self.__classes[args[0]]()
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """help documentation for create command"""
        print("Create a new instance of a class")
        print("[Usage] create <class name> <kwargs.key>=<kwargs.value>")

    def do_show(self, line: str):
        """prints a string representation of an instance"""
        args = line.split(" ")
        if len(args) < 2:
            print("** instance id missing **")
            return
        stored_instance = storage.all(args[0])
        instance = stored_instance.get(f"{args[0]}.{args[1]}")
        if instance is None:
            print("** no instance found **")
            return
        print(instance)

    def help_show(self):
        """help documentation for show command"""
        print("Prints the string representation of an instance")
        print("[Usage] show <class name> <instance id>")

    def do_update(self, line):
        """update an instance"""
        args = line.split(" ")
        length = len(args)
        if length < 2:
            print("** instance id missing **")
            return
        stored_instance = storage.all(args[0])
        instance = stored_instance.get(f"{args[0]}.{args[1]}")
        if instance is None:
            print("** no instance found **")
            return
        if length < 3:
            print("** value missing **")
            return
        i = 2
        while i < length:
            if ('"' in args[i]) and (args[i].count('"') != 2):
                j = i
                i += 1
                index = args[j].find('"')
                args[j] = args[j][:index] + args[j][(index + 1):]
                while (i < length) and (args[i].endswith('"') is False):
                    args[j] += " " + args[i]
                    args.pop(i)
                    length -= 1
                    i += 1
                if i < length and args[i].endswith('"'):
                    args[j] += " " + args[i]
                    args[j] = args[j][:-1]
                    args.pop(i)
                    length -= 1
            else:
                i += 1
        for i in range(2, length):
            pair = args[i].partition("=")
            if len(pair) < 3:
                instance[pair[0]] = ""
            else:
                instance[pair[0]] = pair[2]
        storage.save()

    def help_update(self):
        """help documentation for update command"""
        print("Updates instance key values")
        print("[Usage] update <class name> <class id> <key>=<value>")

    def do_count(self, line):
        """counts number of class instances"""
        stored_instance = storage.all(line)
        print(len(stored_instance))

    def help_count(self):
        """help documnentation for count command"""
        print("Counts the number of created instance of a class")
        print("[Usage] count <class name>")

    def do_all(self, line):
        """prints all saved instance"""
        saved_instance = {}
        if line:
            if line in self.__classes:
                saved_instance = storage.all(line)
            else:
                print("** class doesn't exist **")
        else:
            saved_instance = storage.all()
        for i in saved_instance:
            print(saved_instance[i])

    def help_all(self):
        """help documentation for all command"""
        print("Prints all saved instances")
        print("[Usage] all <class name>")

    def do_destroy(self, line):
        """delete a saved instance"""
        args = line.split(" ")
        stored_instance = storage.all()
        if len(args) < 2:
            hold = stored_instance.copy()
            for i in hold:
                if "User" in i:
                    del stored_instance[i]
            storage.save()
        else:
            instance = stored_instance.get(f"{args[0]}.{args[1]}")
            if instance is None:
                print("** no instance found **")
                return
            del stored_instance[f"{args[0]}.{args[1]}"]
            storage.save()

    def help_destroy(self):
        """help documentation for destroy command"""
        print("Delete a saved instance")
        print("[Usage] destroy <class name> <class id>")


if __name__ == "__main__":
    TaskHubCommand().cmdloop()