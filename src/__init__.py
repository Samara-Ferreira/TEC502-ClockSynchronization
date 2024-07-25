"""Este arquivo é responsável por adicionar o diretório pai ao sys.path, para que os módulos do projeto possam ser
importados de qualquer lugar do projeto."""

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)
