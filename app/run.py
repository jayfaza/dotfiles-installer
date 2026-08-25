from .entry.app import App
import sys

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("CtrlC")
        exit(0)
