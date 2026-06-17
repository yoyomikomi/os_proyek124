import os, shlex, subprocess, shutil, platform

#izin tes 
username = os.getlogin()
device = platform.node()

def main():
    while True:
        try:
            cwd = os.getcwd()
            user_input = input(f"\33[1m\33[35m{username} -{device}@{cwd}:~$ \33[0m").strip()

            if user_input == "exit":
                print('\ndadahh')
                break

        except KeyboardInterrupt:
            print()
            continue

        except EOFError:
            print()
            continue

        print(user_input)

        if not user_input.strip():
            print('emptyy oooo')
            continue
        
        try:
            input_args = shlex.split(user_input)
        except:
            print("\n\33[1m\33[91mUnknown error occured.\33[0m")
            continue

        for i, token in enumerate(input_args):
            print(f'input_args[{i}] = {token}')

        command = input_args[0]
        argument = input_args[1:] if len(input_args) > 1 else []
        print(f'\nCommand: {command}')
        print(f'Argument: {argument}')

        print(input_args)
        print('')

        if len(argument) > 0 and argument[0] == "--help":
            show_help(command)
            continue

        match command:

            case "cd":
                if len(argument) > 0:
                    if argument[0] == "~":
                        os.path.expanduser("~")
                    elif argument[0] == ".":
                        pass
                    else:
                        try:
                            os.chdir(f"{argument[0]}")
                        except FileNotFoundError:
                            print(f"\n\33[1m\33[91mcd: {argument[0]}: No such file or directory\33[0m")
                        except PermissionError:
                            print(f"\n\33[1m\33[91mcd: {argument[0]}: Permission denied\33[0m")
                else:
                    os.chdir(os.path.expanduser("~"))

            case "pwd":
                print(os.getcwd())

            case "clear":
                os.system('cls||clear')

            case "ls":
                try:
                    if hasattr(os, 'fork'): #check kl os bisa fork or not

                        pid = os.fork()

                        if pid == 0:
                            print()
                            if len(argument) == 0: 
                                os.execvp('ls', ['ls'])
                            else:
                                os.execvp('ls', ['ls', *argument])

                            # exec adlh cmd buat executing cmd yg ad d argumenny
                            # v = vector, p = path
                            # execvp berbasis path, jd egk perlu path absolut
                            # intiny execvp(file, args) nyari file ls buat di execute dg argumen yg ad di list

                        elif pid > 0:
                            finishedpid, status = os.waitpid(pid, 0)
    
                    else: #kl egk pny fork pake ini, windows alternative doang; main ls yg pake fork
                        child = subprocess.Popen(['dir', *argument], 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE, 
                                                    text=True, 
                                                    shell=True)
                        stdout, stderr = child.communicate()
                        print(stdout)

                except OSError as err:
                    print(f"{err}")

            case "cp":
                # check if enough arguumnetes
                if len(argument) < 2:
                    print("\n\33[1m\33[91mcp: missing file operand\33[0m")
                    print("\n\33[1m\33[91mTry 'cp --help' for more information\33[0m")
                    continue
                
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
                            continue
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
                    continue
                
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
                            continue
                        
                        src = sources[0]
                        
                        if not os.path.exists(src):
                            print(f"\n\33[1m\33[91mmv: {src}: No such file or directory\33[0m")
                            continue
                        
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
                    continue

                recursive = False
                files_remove = []

                for arg in argument:
                    if arg == "-r" or arg == "R":
                        recursive = True
                    else:
                        files_remove.append(arg)

                if len(files_remove) == 0:
                    print("\n\33[1m\33[91mrm: missing operand\33[0m")
                    continue
                
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
                        continue
                    else:
                        parents = "-p" in argument or "-" in argument
                        dirtargets = [arg for arg in argument if arg.lower() != "-p"]
                        
                        if len(dirtargets) == 0:
                                print("\n\33[1m\33[91mmkdir: missing operand\33[0m")
                                continue
                        
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
                        continue
                    else:
                        parents = "-p" in argument or "-" in argument
                        dirtargets = [arg for arg in argument if arg.lower() != "-p"]
                        
                        if len(dirtargets) == 0:
                                print("\n\33[1m\33[91mrmdir: missing operand\33[0m")
                                continue
                        
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
        