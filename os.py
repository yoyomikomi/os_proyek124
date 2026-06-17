import os, shlex, subprocess, shutil

#izin tes 
username = os.getlogin()

def main():
    while True:
        

        try:
            cwd = os.getcwd()
            user_input = input(f"\33[1m\33[35m{username}@{cwd}:~$ \33[0m").strip()

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
            print("Unknown error occured.")
            continue

        for i, token in enumerate(input_args):
            print(f'input_args[{i}] = {token}')

        command = input_args[0]
        argument = input_args[1:] if len(input_args) > 1 else []
        print(f'\nCommand: {command}')
        print(f'Argument: {argument}')

        print(input_args)
        print('')

        match command:

            case "cd":
                if len(argument) > 0:
                    try:
                        os.chdir(f"{argument[0]}")
                        
                    except FileNotFoundError:
                        print(f"cd: {argument[0]}: No such file or directory")
                    except PermissionError:
                        print(f"cd: {argument[0]}: Permission denied")
                else:
                    pass

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
                        else:
                            print("NOOOO")
                            os._exit(1)
    
                    else: #kl egk pny fork pake ini, windows alternative doang; main ls yg pake fork
                        child = subprocess.Popen(['dir', *argument], 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE, 
                                                    text=True, 
                                                    shell=True)
                        stdout, stderr = child.communicate()
                        print(stdout)

                except OSError as err:
                    print(err)

            case "cp":
                # check if enough arguumnetes
                if len(argument) < 2:
                    print("cp: missing file operand")
                    print("Usage: cp source destination")
                    print("       cp source1 source2 ... destination")
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
                                print(f"cp: {src}: No such file or directory")
                            except PermissionError:
                                print(f"cp: {src}: Permission denied")
                            except FileExistsError:
                                print(f"cp: {os.path.join(dest, os.path.basename(src))}: Already exists")
                    # destination is file or doesn't exist
                    else:
                        # mult source tpi dest nya file / gaada
                        if len(sources) > 1:
                            print(f"cp: target '{dest}' is not a directory")
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
                            print(f"cp: {src}: No such file or directory")
                        except PermissionError:
                            print(f"cp: {src}: Permission denied")
                        except FileExistsError:
                            print(f"cp: {dest}: Already exists")
                #klo ada error lain
                except Exception as e:
                    print(f"cp: {e}")

            case _:
                print('\n\33[1m\33[91mbe patient kitten daddy is implementing it next week ;)')

if __name__ == '__main__':
    main()
        