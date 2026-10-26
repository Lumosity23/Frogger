import argparse
import ctypes
import platform

from src.main import App

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        # Option de secours pour les versions plus anciennes de Windows
        ctypes.windll.user32.SetProcessDPIAware()


if __name__ == "__main__":
    # Catch the argument of the scale
    parser = argparse.ArgumentParser("frogger")
    parser.add_argument(
        "--scale",
        dest="scale",
        nargs="?",
        const=1,
        default=1.0,
        help="Scale the size of the Game window with a float",
        type=float
    )
    args = parser.parse_args()

    frog = App(
        600, 1000, "Test de la boucle de base", scale=args.scale
    )  # Resolution de telephone comme pour un crossy road
    frog.run()
