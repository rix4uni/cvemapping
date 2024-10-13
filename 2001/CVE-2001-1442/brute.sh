
#!/bin/ksh
L=-2000
O=40
while [ $L -lt 12000 ]
do
echo $L
L=`expr $L + 1`
./x-startinnfeed $L 
done
