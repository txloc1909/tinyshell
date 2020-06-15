import os
import sys
import signal
import subprocess
import getpass, platform

class TinyShell:

    def __init__(self):
        self.builtin_func = {
            "cd": self.tsh_cd,
            "help": self.tsh_help,
            "exit": self.tsh_exit,
            "runbg": self.tsh_runbg,
            "runfg": self.tsh_runfg,
            "killbg": self.tsh_kill,
            "runsh": self.tsh_runsh
        }

        self.builtin_helps = {
            "cd": "change current working directory",
            "help": "print help",
            "exit": "exit the shell",
            "runbg": "run a binary executional file background",
            "runfg": "run a binary executional file foreground",
            "killbg": "kill current background process",
            "runsh": "run a shell script"
        }

        self.current_bg_pid = -1;
        self.home_dir = os.getenv("HOME")
        self.username = getpass.getuser()
        self.hostcomputer = platform.node()
    
    
    def welcome(self):
        print("\t\t--- TINY SHELL ---")
        print("\tA simple shell named Tinyshell (TSh)\n")


    def tsh_help(self, args):
        if len(args) > 1:
            print("TSh: help() takes at most 1 argument (%d given)" % len(args))
            return


        if len(args) > 0 and args[0] in builtin_helps:
            print("%-10s: %s\n" % (args[0], self.builtin_helps[args[0]]))
        else:
            print("Support common bash command")
            print("These commands are builtin:")
            for command in self.builtin_helps:
                print("%-10s: %s\n" % (command, self.builtin_helps[command]))
    

    def tsh_cd(self, args):
        if len(args) > 1:
            print("TSh: cd() takes 1 argument (%d given)" % len(args))
            return
        
        try:
            path = self.home_dir if not args else args[0]
            
            os.chdir(os.path.abspath(path))
        except FileNotFoundError:
            print("TSh: cd: %s: No such file or directory" % path)
        except NotADirectoryError:
            print("TSh: cd: %s: Not a directory" % path)
    

    def tsh_exit(self, args):
        if len(args) > 0:
            print("TSh: exit() takes no argument (%d given)" % len(args))
            return
        
        exit(0)
        

    def tsh_kill(self, args):
        if len(args) > 0:
            print("TSh: kill() takes no argument (%d given)" % len(args))
            return
        
        os.kill(self.current_bg_pid, signal.SIGINT)
        

    def tsh_runfg(self, args):
        args[0] = "./" + args[0]
        pid = os.fork()

        if pid == 0: 
            # inside child process
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            try:
                os.execv(args[0], args)
            except FileNotFoundError:
                print("%s: file not found!" % args[0])
            finally:
                exit(1)
        elif pid > 0:
            # inside parent process
            try:
                while True:
                    child_id, _ = os.wait()
                    if child_id == pid:
                        break
            except KeyboardInterrupt:
                os.kill(pid, signal.SIGINT)
        else:
            print("TSh: fork() failed")


    def tsh_runbg(self, args):
        args[0] = "./" + args[0]

        pid = os.fork()
        if pid == 0: 
            # inside child process
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            try:
                os.execv(args[0], args)
            except FileNotFoundError:
                print("%s: file not found!" % args[0])
            finally:
                self.current_bg_pid = -1;
                exit(1)
        elif pid > 0:
            # inside parent process
            self.current_bg_pid = pid
        else:
            print("TSh: fork() failed")

    
    def tsh_runsh(self, args):
        if len(args) > 1:
            print("TSh: runsh() takes 1 argument (%d given)" % len(args))
            return
        
        if not args[0].endswith(".sh"):
            print("%s: not a shell script!" % args[0])
            return
        
        try:
            f = open(args[0], "r")
        except FileNotFoundError:
            print("%s: file not found!", args[0])
            return
        
        commands = [cmd.strip() for cmd in f.readlines()]
        for command in commands:
            self.execute(command)


    def execute(self, command):
        if not command:
            pass
        elif command.strip().split()[0] in self.builtin_func:
            self.execute_builtin(command)
        else:
            try:
                subprocess.run(command.split())
            except KeyboardInterrupt:
                return
            except FileNotFoundError:
                print("TSh: command not found: %s" % command)
            except Exception:
                print("TSh: cannot execute command: %s" % command)
    

    def execute_builtin(self, command):
        parsed = command.strip().split()
        cmd = parsed[0]
        args = parsed[1:]
        func = self.builtin_func.get(cmd)
        return func(args)
    

    def loop(self):
        self.welcome();

        # os.chdir(self.home_dir)
        while (True):
            cwd = os.getcwd().replace(self.home_dir, "~")
            sys.stdin.flush()
            try:
                command = input("%s@%s:%s$ " % (self.username, self.hostcomputer, cwd))
            except EOFError: # Ctr-D received
                break
            except KeyboardInterrupt: # Ctr-C received
                break
            
            self.execute(command)



if __name__ == "__main__":
    shell = TinyShell()
    shell.loop()
