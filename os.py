import os, shlex

#izin tes 
username = os.getlogin()

def main():
    while True:
        

        try:
            cwd = os.getcwd()
            user_input = input(f"\33[1m\33[35m{username}_{cwd}:~$ \33[0m").strip()

            if user_input == "exit":
                print('\ndadahh')
                break

        except KeyboardInterrupt:
            print('\ndadahh')
            break

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
                            os._exit
    
                    else: #kl egk pny fork pake ini 
                        print(os.listdir())

                except OSError as err:
                    print(err)

            case _:
                print('\n\33[1m\33[91mbe patient kitten daddy is implementing it next week ;)')

if __name__ == '__main__':
    main()
        