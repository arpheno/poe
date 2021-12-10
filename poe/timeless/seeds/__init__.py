import glob
from pathlib import Path

paths = list(filter(lambda x: "__" not in x, glob.glob(f"{Path(__file__).parent}/*")))
seeds = {Path(path).parts[-1]:[seed.strip() for seed in open(path).readlines()] for path in paths}
