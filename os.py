import os, shlex, subprocess, shutil, platform, sys

#izin tes 
username = os.getlogin()
device = platform.node()
is_interactive = sys.stdin.isatty()

def main():
    while True:
        try:
            cwd = os.getcwd()
            if is_interactive: 
                prompt = f"\33[1m\33[35m{username} ~ {device}@{cwd}:~$ \33[0m"
                user_input = input(prompt).strip()
            else: 
                user_input = input().strip()

            if user_input == "exit":
                if is_interactive:
                    print('\33[5mdadahh\33[0m')
                break

            if not user_input.strip():
                if not is_interactive:
                    continue
                print('\33[5memptyy oooo\33[0m')
                continue

        except KeyboardInterrupt:
            print()
            if not is_interactive:
                break
            continue

        except EOFError:
            print()
            if not is_interactive:
                break
            continue

        # print(user_input)

        pipe_cmds = [cmd.strip() for cmd in user_input.split('|')]

        if len(pipe_cmds) == 1:
            try:
                input_args = shlex.split(pipe_cmds[0])
            except:
                print("\n\33[1m\33[91mUnknown error occured while parsing arguments.\33[0m")
                continue
            
            if not input_args:
                continue
            
            # for i, token in enumerate(input_args):
            #     print(f'input_args[{i}] = {token}')

            command = input_args[0]
            argument = input_args[1:] if len(input_args) > 1 else []

            single_cmds(command, argument, cwd)
            
            if len(argument) > 0 and argument[0] == "--help":
                show_help(command)
                continue
        else:
            execute_pipe_cmds(pipe_cmds)


        # print(f'\nCommand: {command}')
        # print(f'Argument: {argument}')

        # print(input_args)
        # print('')

def single_cmds(command, argument, cwd):
    
        match command:

            case "cd":
                if len(argument) > 0:
                    if argument[0] == "~":
                        homedir = os.path.expanduser("~")
                        os.chdir(homedir)
                        return
                    elif argument[0] == ".":
                        return
                    else:
                        try:
                            os.chdir(f"{argument[0]}")
                        except FileNotFoundError:
                            print(f"\n\33[1m\33[91mcd: {argument[0]}: No such file or directory\33[0m")
                        except PermissionError:
                            print(f"\n\33[1m\33[91mcd: {argument[0]}: Permission denied\33[0m")
                else:
                    return

            case "pwd":
                print(os.getcwd())
                return

            case "clear":
                os.system('cls||clear')
                return

            case "ls":
                try:
                    if hasattr(os, 'fork'):
                        fork_cmd('ls', argument)
                    else: #kl egk pny fork pake ini, windows alternative doang; main ls yg pake fork
                        child = subprocess.Popen(['dir', *argument], 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE, 
                                                    text=True, 
                                                    shell=True)
                        stdout, stderr = child.communicate()
                        print(stdout)
                        return

                except OSError as err:
                    print(f"{err}")

            case "cp":
                # check if enough arguumnetes
                if len(argument) < 2:
                    print("\n\33[1m\33[91mcp: missing file operand\33[0m")
                    print("\n\33[1m\33[91mTry 'cp --help' for more information\33[0m")
                    return
                
                # last argument = destination
                dest = argument[-1]
                sources = argument[:-1]
                
                try:
                    # ceck if destination is  directory udh ada
                    if os.path.isdir(dest):
                        # loop through each source
                        for src in sources:
                            try:
                                # soucce IS directory
                                if os.path.isdir(src):
                                    shutil.copytree(src, os.path.join(dest, os.path.basename(src)))
                                    print(f"Copied directory: {src} -> {dest}")
                                # source IS file
                                else:
                                    shutil.copy2(src, dest)
                                    print(f"Copied file: {src} -> {dest}")
                            except FileNotFoundError:
                                print(f"\n\33[1m\33[91mcp: {src}: No such file or directory\33[0m")
                            except PermissionError:
                                print(f"\n\33[1m\33[91mcp: {src}: Permission denied\33[0m")
                            except FileExistsError:
                                print(f"\n\33[1m\33[91mcp: {os.path.join(dest, os.path.basename(src))}: Already exists\33[0m")
                    # destination is file or doesn't exist
                    else:
                        # mult source tpi dest nya file / gaada
                        if len(sources) > 1:
                            print(f"\n\33[1m\33[91mcp: target '{dest}' is not a directory\33[0m")
                            return
                        # single source
                        src = sources[0]
                        try:
                            # source nya directory
                            if os.path.isdir(src):
                                shutil.copytree(src, dest)
                                print(f"Copied directory: {src} -> {dest}")
                            # source nya file
                            else:
                                shutil.copy2(src, dest)
                                print(f"Copied file: {src} -> {dest}")
                        except FileNotFoundError:
                            print(f"\n\33[1m\33[91mcp: {src}: No such file or directory\33[0m")
                        except PermissionError:
                            print(f"\n\33[1m\33[91mcp: {src}: Permission denied\33[0m")
                        except FileExistsError:
                            print(f"\n\33[1m\33[91mcp: {dest}: Already exists\33[0m")
                #klo ada error lain
                except Exception as e:
                    print(f"\n\33[1m\33[91mcp: {e}\33[0m")

            case "mv":
                # cek argmen cukup/no
                if len(argument) < 2:
                    print("\n\33[1m\33[91mmv: missing file operand\33[0m")
                    print("\n\33[1m\33[91mTry 'mv --help' for more information\33[0m")
                    return
                
                dest = argument[-1]
                sources = argument[:-1]
                
                try:
                    # dest is directory
                    if os.path.isdir(dest):
                        for src in sources:
                            try:
                                # ceck if source exists
                                if not os.path.exists(src):
                                    print(f"\n\33[1m\33[91mmv: {src}: No such file or directory\33[0m")
                                    continue
                                
                                # move the file/directory into dest
                                shutil.move(src, dest)
                                print(f"Moved: {src} -> {dest}")
                                
                            except PermissionError:
                                print(f"\n\33[1m\33[91mmv: {src}: Permission denied\33[0m")
                            except Exception as e:
                                print(f"\n\33[1m\33[91mmv: {e}\33[0m")
                    
                    # dest is file/doesnt exist
                    else:
                        # if mult sources but dest is not a directory then errr
                        if len(sources) > 1:
                            print(f"\n\33[1m\33[91mmv: target '{dest}' is not a directory\33[0m")
                            return
                        
                        src = sources[0]
                        
                        if not os.path.exists(src):
                            print(f"\n\33[1m\33[91mmv: {src}: No such file or directory\33[0m")
                            return
                        
                        try:
                            # move/rename the single source to destination
                            shutil.move(src, dest)
                            print(f"Moved: {src} -> {dest}")
                            
                        except PermissionError:
                            print(f"\n\33[1m\33[91mmv: {src}: Permission denied")
                        except Exception as e:
                            print(f"\n\33[1m\33[91mmv: {e}\33[0m")
                
                except Exception as e:
                    print(f"\n\33[1m\33[91mmv: {e}\33[0m")

            case "rm":
                if len(argument) == 0:
                    print("\n\33[1m\33[91mrm: missing operand\33[0m")
                    print("\n\33[1m\33[91mTry 'rm --help' for more information\33[0m")
                    return

                recursive = False
                files_remove = []

                for arg in argument:
                    if arg == "-r" or arg == "R":
                        recursive = True
                    else:
                        files_remove.append(arg)

                if len(files_remove) == 0:
                    print("\n\33[1m\33[91mrm: missing operand\33[0m")
                    return
                
                for file in files_remove:
                    try:
                        if not os.path.exists(file):
                            print(f"\n\33[1m\33[91mrm: {file}: No such file or directory\33[0m")
                            continue
                        if os.path.isdir(file):
                            if recursive:
                                shutil.rmtree(file)
                                print(f"Removed directory: {file}")
                            else:
                                print(f"\n\33[1m\33[91mrm: {file}: Is a directory (use -r or -R)\33[0m")
                        else:
                            os.remove(file)
                            print(f"Removed file: {file}")
                    except PermissionError:
                        print(f"\n\33[1m\33[91mrm: {file}: Permission denied\33[0m")
                    except Exception as e:
                        print(f"\n\33[1m\33[91mrm: {e}\33[0m")
                        
            case "mkdir":
                try:
                    if len(argument) == 0:
                        print("\n\33[1m\33[91mkdir: missing operand\33[0m")
                        return
                    else:
                        parents = "-p" in argument or "-" in argument
                        dirtargets = [arg for arg in argument if arg.lower() != "-p"]
                        
                        if len(dirtargets) == 0:
                                print("\n\33[1m\33[91mmkdir: missing operand\33[0m")
                                return
                        
                        for arg in dirtargets:
                            path = os.path.join(cwd, arg)
                            
                            if parents:
                                os.makedirs(path, exist_ok=True)
                                print(f"Directory created at {path}")
                            else:
                                if "/" in arg or "\\" in arg:
                                    parentdir = os.path.dirname(path)
                                    if not os.path.exists(parentdir):
                                        print(f"\n\33[1m\33[91mmkdir: cannot create directory {arg}. No such file or directory\33[0m")
                                        continue
                                    
                                try:
                                    os.mkdir(path)
                                    print(f"Created directory at: {path}")
                                except FileExistsError:
                                    print(f"\n\33[1m\33[91mmkdir: cannot create directory '{path}': Directory already exists\33[0m")
                                except OSError as err:
                                    print(f"\n\33[1m\33[91mmkdir: failed to create directory '{path}: {err}\33[0m")
                        
                except Exception as err:
                    print(f"\n\33[1m\33[91mmkdir: {err}\33[0m")

            case "rmdir":
                try:
                    if len(argument) == 0:
                        print("\n\33[1m\33[91mrmdir: missing operand\33[0m")
                        return
                    else:
                        parents = "-p" in argument or "-" in argument
                        dirtargets = [arg for arg in argument if arg.lower() != "-p"]
                        
                        if len(dirtargets) == 0:
                                print("\n\33[1m\33[91mrmdir: missing operand\33[0m")
                                return
                        
                        for arg in dirtargets:
                            if "/" in arg or "\\" in arg:
                                fulldir = arg.rsplit('/', 1)
                                path = os.path.join(cwd, fulldir[0])
                                selecteddir = fulldir[1]
                            else:
                                path = cwd
                                selecteddir = arg
                                
                            origincwd = os.getcwd()

                            try:
                                os.chdir(path)
                                
                                if parents:
                                    os.removedirs(selecteddir)
                                    print(f"Directory and parents removed: {selecteddir}")
                                else:
                                    os.rmdir(selecteddir)
                                    print(f"Directory removed: {selecteddir}")
                            except FileNotFoundError:
                                print(f"\n\33[1m\33[91mrmdir: failed to remove {arg}: No such file or directory\33[0m") 
                            except OSError as err:
                                print(f"\n\33[1m\33[91mrmdir: failed to remove {arg}: {err}\33[0m")
                            finally:
                                os.chdir(origincwd)
                        
                except Exception as err:
                    print(f"\n\33[1m\33[91mrmdir: {err}\33[0m")

            case ":?":
                print("Commands available from the prompt:")
                print("  cd                    Change the current directory")
                print("  pwd                   Print the current working directory")
                print("  clear                 Clear the terminal screen")
                print("  ls                    List files and folders")
                print("  cp                    Copy a file or folder")
                print("  mv                    Mover or rename a file or folder")
                print("  rm                    Remove a file")
                print("  mkdir                 Create a new directory")
                print("  rmdir                 Remove an empty directory")
            
            case _:
                print('\n\33[1m\33[91mbe patient kitten daddy is implementing it next week ;)\33[0m')

def fork_cmd(command, argument):

    pid = os.fork()

    if pid == 0:
        print()
        if len(argument) == 0: 
            os.execvp(command, [command])
        else:
            os.execvp(command, [command, *argument])

    elif pid > 0:
        finishedpid, status = os.waitpid(pid, 0)

def execute_pipe_cmds(pipedcmdlist):
    n_cmds = len(pipedcmdlist)
    prev_pipe = None

    active_pids = []

    for i, cmd_str in enumerate(pipedcmdlist):
        try:
            args = shlex.split(cmd_str)
        except Exception as err:
            print(f"\n\33[1m\33[91mError parsing pipeline command: {err}\33[0m")

        if not args:
            return
        
        command = args[0]
        argument = args[1:] if len(args) > 1 else []

        last_cmd = (i == n_cmds - 1)
        if not last_cmd:
            pipe_r, pipe_w = os.pipe()

        if hasattr(os, 'fork'):
            pid = os.fork()
            if pid == 0:
                if prev_pipe is not None:
                    os.dup2(prev_pipe, 0)
                    os.close(prev_pipe)

                if not last_cmd:
                    os.dup2(pipe_w, 1)
                    os.close(pipe_w)
                    os.close(pipe_r)

                try:
                    os.execvp(command, [command, *argument])
                except FileNotFoundError:
                    print(f"{command}: command not found")
                    os._exit(1)
            else:
                if prev_pipe is not None:
                    os.close(prev_pipe)

                if not last_cmd:
                    os.close(pipe_w)
                    prev_pipe = pipe_r

            for pid in active_pids:
                try:
                    os.waitpid(pid, 0)
                except ChildProcessError:
                    pass
        else:
            processes = []
            prev_stdout = None

            for i, cmd_str in enumerate(pipedcmdlist):
                try:
                    args = shlex.split(cmd_str)
                except Exception as err:
                    print(f"Error parsing command.")
                    return
                if not args: 
                    continue

                if args[0] == 'ls':
                    args = ['dir'] + args[1:]
                    useshell = True
                else: 
                    useshell = False
            
                curr_stdin = prev_stdout if prev_stdout is not None else None

                last_cmd = (i == len(pipedcmdlist) - 1)
                curr_stdout =  None if last_cmd else subprocess.PIPE

                try:
                    proc = subprocess.Popen(args, 
                                            stdin=curr_stdin, 
                                            stdout=curr_stdout,
                                            shell=useshell,
                                            text=True
                                            )
                    processes.append(proc)

                    if prev_stdout is not None:
                        prev_stdout.close()
                    
                    prev_stdout = proc.stdout

                except FileNotFoundError:
                    print(f"{args[0]}: command not found")
                except Exception as err:
                    print(f"Error executing {args[0]}: {err}")

            for proc in processes:
                proc.wait()

def show_help(command):
    print(f'\n\33[3m\33[32mHelp: {command}\33[0m\n')

    if command == "cd":
        print("Usage: cd directory")
        print("Change the current directory to DIRECTORY")
        print("       cd path/to/dir      - Change to specified directory")
        print("       cd                  - Change to home directory")
        print("       cd ~                - Change to home directory")
        print("       cd ..               - Change to previous directory")

    elif command == "pwd":
        print("Usage: pwd")
        print("Print the full pathname of the current working directory")

    elif command == "clear":
        print("Usage: clear")
        print("Clear the terminal screen")
        
    elif command == "ls":
        print("Usage: ls")
        print("List directory contents")
        print("       ls - List current directory")
        print("       ls -l               - Long format")
        print("       ls -a               - Show hidden files")
        print("       ls path             - List PATH directory contents")

    elif command == "cp":
        print("Usage: cp source destination")
        print("       cp source1 source2 ... destination")
        print("Copy SOURCE to DESTINATION or multiple SOURCE(s) to DIRECTORY")
        print("       cp file1 file2      - Copy file1 to file2")
        print("       cp file1 dir/       - Copy file1 to directory dir")
        print("       cp dir1 dir2        - Copy directory dir1 to dir2")
        print("       cp file1 file2 dir/ - Copy file1 and file2 to directory dir")

    elif command == "mv":
        print("Usage: mv source destination")
        print("       mv source1 source2 ... destination")
        print("Rename SOURCE to DEST or move SOURCE(s) to DIRECTORY")
        print("       mv file1 file2      - Rename file1 to file2")
        print("       mv file1 dir/       - Move file1 to directory dir")
        print("       mv dir1 dir2        - Move directory dir1 to dir2")
        print("       mv file1 file2 dir/ - Move file1 and file2 to directory dir")

    elif command == "rm":
        print("Usage: rm [OPTION] file1 file2 ...")
        print("Remove FILE(s) or DIRECTORY(ies)")
        print("       rm file.txt         - Delete file(s)")
        print("       rm -r directory     - Delete directory and contents")
    
    elif command == "mkdir":
        print("Usage: mkdir directory1 directory2 ...")
        print("Create DIRECTORY(ies) if they do not already exist")
        print("       mkdir dir           - Create single directory")    
        print("       mkdir dir1 dir2     - Create multiple directories")
    elif command == "rmdir":
        print("Usage: rmdir directory1 directory2 ...")
        print("Remove empty DIRECTORY(ies)")
        print("       rmdir dir           - Remove single directory")
        
    elif command == "exit":
        print("Usage: exit")
        print("Exit the shell")
        
    else:
        print('\n\33[1m\33[91mbe patient kitten daddy is implementing it next week ;)\33[0m')
        print("Here are options you can try: ")
        print("     cd, pwd, clear, ls")
        print("     cp, mv, rm, mkdir, rmdir")
        print("     exit")
        
if __name__ == '__main__':
    main()
        