import json
from classes.App import WpApp


def main():

    app = WpApp()
    app.verify_folders()
    app.update()


if __name__ == '__main__':
    main()
