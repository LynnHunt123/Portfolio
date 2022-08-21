# For version sphinx==4.2.0
#############################################
############### For demo only ############### 
#############################################

############### Generate config files ###############
mkdir docs
cd docs
# sphinx-quickstart creates default configuration
sphinx-quickstart -q -p "$PROJECT" -a "$AUTHOR" -v "$VERSION"


############### Makefile config ###############
sed -i 's/BUILDDIR      = _build/BUILDDIR      = ../g' Makefile

############### conf.py config ###############
sed -i 's/# import/import/g' conf.py 
sed -i 's/# sys.path.insert/sys.path.insert/g' conf.py
sed -i "s/abspath('.')/abspath('..')/g" conf.py
echo "" >> conf.py
echo "
extensions.extend(['sphinx.ext.autodoc', 'sphinx.ext.autosummary'])
autosummary_generate = True
" >> conf.py
echo "
def get_all_subpath(path: str) -> list:
    all_abspaths = []
    for subpath in os.listdir(path):
        subpath = os.path.join(path, subpath)
        if os.path.isdir(subpath):
            all_abspaths.append(subpath)
            if get_all_subpath(subpath):
                all_abspaths.extend(get_all_subpath(subpath))
    return all_abspaths


for path in get_all_subpath(os.path.abspath('..')):
    sys.path.insert(0, path)

import logging
logging.debug(f'All sys path: {sys.path}')
" >> conf.py

# Changes documentation theme
sed -i 's/alabaster/sphinx_rtd_theme/g' conf.py

############### index.rst config ###############
sed -i '13i \ \ \ modules' index.rst
sed -i '14i \ \ \ includeme' index.rst
sed -i "8i ..\ autosummary::\n\ \ \ :toctree: _autosummary\n\ \ \ :recursive:" index.rst

############### includeme.rst creation ###############
# This step follows instructions found at https://daler.github.io/sphinxdoc-test/includeme.html 
# Get date information from UNIX CLI
currentDate=`date`
# Add line to enable sphinx to display content of README to documentation page.
echo "
README
================================
.. include:: ../README.rst
" >> includeme.rst
# Adds newline at the end of includeme.rst
echo "" >> includeme.rst
# Displays update time at the end of README page on documentation index.
echo "Updated ${currentDate}." >> includeme.rst
