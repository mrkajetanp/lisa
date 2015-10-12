#!/bin/bash

echo
echo "This script is required only for the development version"
echo "It will not be required once we have a stable vetsion".
echo "At that time everythin will work magically out-of-the-box"
echo

echo "Initializing dependency libraries..."
git submodule init
git submodule update

echo "To run the suite, first edit you configuration:"
echo "  target.config        : to setup your target board"
echo "  tests/eas/rfc.config : to define the experiment to run"
echo
echo "Than run the tests with:"
echo "  nosetests -v tests/eas/rfc.py"
echo
echo "Once tests have completed, you could report results by running"
echo "./tools/report.py"
echo

