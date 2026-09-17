import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT))

(ROOT / "logs").mkdir(exist_ok=True)

from avionics.main import main

if __name__ == "__main__":
    main()
