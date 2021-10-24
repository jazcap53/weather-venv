printf -v date "%(%Y-%m-%d %H:%M:%S)T"
LOGFILE_DIR="weather/weather/"
TESTFILE="${LOGFILE_DIR}testfile.txt"
echo $date " printing something to test file" >> $TESTFILE
