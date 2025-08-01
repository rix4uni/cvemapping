#import <UIKit/UIKit.h>

@interface ViewController : UIViewController

@property (nonatomic, strong) UITextView *logTextView;
@property (nonatomic, strong) UIButton *exploitButton;

- (void)appendLog:(NSString *)log;

@end
