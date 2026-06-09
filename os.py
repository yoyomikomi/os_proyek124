import os
import shlex

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

        input_args = shlex.split(user_input)

        for i, token in enumerate(input_args):
            print(f'input_args[{i}] = {token}')

        command = input_args[0]
        argument = input_args[1:] if len(input_args) > 1 else []
        print(f'\nCommand: {command}')
        print(f'Argument: {argument}')

        print(input_args)
        print('')
        if command == "cd":
            if len(argument) > 0:
                try:
                    os.chdir(f"{argument[0]}")
                    
                except FileNotFoundError:
                    print(f"cd: {argument[0]}: No such file or directory")
                except PermissionError:
                    print(f"cd: {argument[0]}: Permission denied")
            else:
                pass

        elif command == "pwd":
            print(os.getcwd())

        else:
            print('\n\33[1m\33[91mbe patient kitten daddy is implementing it next week ;)')
#e mau nanya dah, kl misal foldernya ada spasi gmn ? blm ak mau coba pake backslash di spasinya bisa tak
# cb cb
if __name__ == '__main__':
    main()
        