#!/bin/sh

# three-fingered claw technique
shout() { echo "$0: $*" >&2; }
die() { shout "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }

# fancy coloring for script output
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color
TEST_COUNT=0
TEST_COUNT_OK=0


### TEST IF ANACONDA IS installed
printf "*** check if conda is installed... "
OUTPUT=$(which conda)
TEST_COUNT=$((TEST_COUNT+1))
if [[ $OUTPUT = *[!\ ]* ]]; then
  #OUTPUT contains characters other than space"
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  #OUTPUT consists of spaces only"
  printf "${RED}FAIL${NC}\n"
  printf "Error: can't find Anaconda. Did you install it ? Did you add it in your \$PATH ?"
  die "CHECK DID NOT COMPLETE"
fi


### TEST ANACONDA ENVIRONMENT CBC
printf "*** check if conda has a 'cbc' environment... "
OUTPUT="$(conda info --envs)"
TEST_COUNT=$((TEST_COUNT+1))
# TODO: write a better test here
if [[ $OUTPUT =~ .*anaconda\/envs\/cbc.* ]]
then
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  printf "${RED}FAIL${NC}\n"
  printf "Error: Can't find the 'cbc' environment in conda output:\n"
  conda info --envs

  # TODO: provide a recommendation
  printf "Error: can't find 'cbc' as a conda environment. Check tutorial to create it.\n"
  die "CHECK DID NOT COMPLETE"
fi


### TEST PYTHON VERSION
printf "*** check python version inside 'cbc' environment..."
OUTPUT=`source activate cbc; python -c "import sys;t='{}'.format(sys.version_info[0]);sys.stdout.write(t)";`
TEST_COUNT=$((TEST_COUNT+1))
if [[ "$OUTPUT" == "3" ]]
then
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  printf "${RED}FAIL${NC}\n"
  printf "Error: Version of python is $OUTPUT, should be Python 3.\n"
  die "CHECK DID NOT COMPLETE"
fi


### LOOK FOR WATSON IN ANACONDA ENVIRONMENT CBC
printf "*** check conda 'cbc' environment for Watson API... "
OUTPUT="$(conda list -n cbc)"
TEST_COUNT=$((TEST_COUNT+1))
# TODO: write a better test here
if [[ $OUTPUT =~ .*watson\-developer\-cloud.* ]]
then
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  printf "${RED}FAIL${NC}\n"
  printf "Error: Can't find watson-developer-cloud package in conda output:\n"
  conda list -n cbc

  printf "Please run 'pip install --upgrade watson-developer-cloud' inside that environment.\n"
  die "CHECK DID NOT COMPLETE"
fi


### LOOK FOR PYTHON-DOTENV IN ANACONDA ENVIRONMENT CBC
printf "*** check conda 'cbc' environment for python-dotenv... "
OUTPUT="$(conda list -n cbc)"
TEST_COUNT=$((TEST_COUNT+1))
# TODO: write a better test here
if [[ $OUTPUT =~ .*python\-dotenv.* ]]
then
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  printf "${RED}FAIL${NC}\n"
  printf "Error: Can't find python-dotenv package in conda output:\n"
  conda list -n cbc

  printf "Please run 'pip install --upgrade python-dotenv' inside that environment.\n"
  die "CHECK DID NOT COMPLETE"
fi


### LOOK FOR PYTEST IN ANACONDA ENVIRONMENT CBC
printf "*** check conda 'cbc' environment for pytest... "
OUTPUT="$(conda list -n cbc)"
TEST_COUNT=$((TEST_COUNT+1))
# TODO: write a better test here
if [[ $OUTPUT =~ .*pytest.* ]]
then
  printf "${GREEN}OK${NC}\n"
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
else
  printf "${RED}FAIL${NC}\n"
  printf "Error: Can't find pytest package in conda output:\n"
  conda list -n cbc

  printf "Please run 'pip install --upgrade pytest' inside that environment.\n"
  die "CHECK DID NOT COMPLETE"
fi


### TEST YOUR CBC_HOME VARIABLE
printf "*** check your CBC_HOME variable... "
TEST_COUNT=$((TEST_COUNT+1))
if [[ -z "${CBC_HOME}" ]]
then
  printf "${RED}FAIL${NC}\n"
  printf "Error: variable CBC_HOME is not set."
  die "CHECK DID NOT COMPLETE"
else
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
  printf "${GREEN}OK${NC}\n"
  printf "> variable CBC_HOME is set to $CBC_HOME\n"
fi


### TEST YOUR CBC_HOME CONTENT
printf "*** check if backpack files unzipped in CBC_HOME... "
TEST_COUNT=$((TEST_COUNT+1))
if [ ! -f "${CBC_HOME}/code/precourse/hello_python.py" ]
then
  printf "${RED}FAIL${NC}\n"
  printf "Error: can't find file 'code/precourse/hello_python.py' in ${CBC_HOME}\n"
  die "CHECK DID NOT COMPLETE"
else
  TEST_COUNT_OK=$((TEST_COUNT_OK+1))
  printf "${GREEN}OK${NC}\n"
fi


if [ $TEST_COUNT == $TEST_COUNT_OK ]
then
  printf "VERIFICATION DONE, $TEST_COUNT CHECKS OK\n"
else
  printf "UNVERIFIED\n"
fi
