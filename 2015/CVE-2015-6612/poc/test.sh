mm
adb push $TOP/out/target/product/hammerhead/symbols/system/bin/servicefuzz /data/local/tmp/servicefuzz
if [ $# == 0 ]; then
    adb shell  setenforce 0
    adb shell  /data/local/tmp/servicefuzz 
else
    adb shell su -c setenforce 0
    adb shell su -c gdbserver :6666 /data/local/tmp/servicefuzz tt &
    adb forward tcp:5039 tcp:5039
    adb forward tcp:6666 tcp:6666
    gdbclient servicefuzz :6666
fi
