import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app import demo  # noqa: E402

if __name__ == "__main__":
    demo.launch()