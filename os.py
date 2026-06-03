import os

#izin tes 
username = os.getlogin()
def main():
    while True:

        try:
            user_input = input(f"tes {username}:~$ ")

            if user_input == "exit":
                print('dadahh')
                break

        except KeyboardInterrupt:
            print('dadahh')
            break

        print(user_input)

        if not user_input.strip():
            print('emptyy oooo')
            continue

        input_args = user_input.split(' ')

        for i, token in enumerate(input_args):
            print(f'input_args[{i}] = {token}')

        command = input_args[0]
        argument = input_args[1:] if len(input_args) > 1 else []

        print(f'\nCommand: {command}')
        print(f'Argument: {argument}')

        print(input_args)

if __name__ == '__main__':
    main()

        