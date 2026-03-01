# Standard library imports

# Third party imports
import pandas as pd

# Local application imports
from poe.woke.use_cases.price_tab import price_tab

# Pandas settings
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

if __name__ == '__main__':
    price_tab('empty')


