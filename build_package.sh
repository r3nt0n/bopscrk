# Update submodule (https://stackoverflow.com/a/1032653)
#git submodule update --init --recursive  # only the first time
git submodule update --recursive --remote

# Build package
python3 setup.py -v sdist
