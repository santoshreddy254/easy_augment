var=$(python3 -c 'import sys; print(sys.version_info[:])')
var2=(3, 5, 2, 'final', 0)
if [$var=var2]
then
	echo "okay"
fi
