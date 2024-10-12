/*
Compile:

gcc -framework Foundation -framework AppKit screenshot.m -o screenshot
*/

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>

int main(void) {
	[NSThread sleepForTimeInterval:3.000];
	//capture window
	CGImageRef screenshot = CGWindowListCreateImage(CGRectInfinite, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, kCGWindowImageDefault);

	//create bitmap
	NSBitmapImageRep *bitmap = [[NSBitmapImageRep alloc] initWithCGImage:screenshot];

	//create PNG from bitmap
	NSData *data = [bitmap representationUsingType:NSBitmapImageFileTypePNG properties:NULL];

	//save file
	[data writeToFile: @"screenshot.png" atomically: NO];

	return 0;
}
