SnatchBox.app: SnatchBox.app/Contents/MacOS/SnatchBox Info.plist ent.xml
	cp Info.plist SnatchBox.app/Contents/
	codesign --force --sign - $@ --entitlements ent.xml

SnatchBox.app/Contents/MacOS/SnatchBox: main.m
	mkdir -p $(dir $@)
	clang -O3 -Wall -framework Foundation $^ -o $@
	
clean:
	rm -rf SnatchBox.app