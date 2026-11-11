# main.py
"""Entry point for 'La derrota del dictador General P. Tardo'.

Keeps only initialization logic. All game-loop and rendering details
live inside the ui package so that core/ and algorithms/ stay free
of any pygame dependency.
"""
import sys

from ui.app import App


def main() -> None:
    try:
        App().run()
    except KeyboardInterrupt:
        pass
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()