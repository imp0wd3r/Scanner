from pyfiglet import Figlet


def print_banner():
    f = Figlet(font='doom')
    print(f.renderText('Scanner'))