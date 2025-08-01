#import "ViewController.h"
#import "Exploit.h"
#import <AVFoundation/AVFoundation.h>

@interface ViewController ()

@end

@implementation ViewController

@synthesize logTextView, exploitButton;

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // Setup UI
    self.view.backgroundColor = [UIColor whiteColor];
    
    // Setup UI log text view
    logTextView = [[UITextView alloc] initWithFrame:CGRectMake(20, 100, self.view.frame.size.width - 40, self.view.frame.size.height - 200)];
    logTextView.editable = NO;
    logTextView.font = [UIFont systemFontOfSize:14];
    logTextView.text = @"Exploit Log:\n";
    [self.view addSubview:logTextView];
    
    // Setup UI button
    exploitButton = [UIButton buttonWithType:UIButtonTypeSystem];
    exploitButton.frame = CGRectMake(20, 50, self.view.frame.size.width - 40, 40);
    [exploitButton setTitle:@"Run Exploit" forState:UIControlStateNormal];
    [exploitButton addTarget:self action:@selector(runExploit) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:exploitButton];
}

- (void)appendLog:(NSString *)log {
    dispatch_async(dispatch_get_main_queue(), ^{
        self.logTextView.text = [self.logTextView.text stringByAppendingFormat:@"%@\n", log];
        [self.logTextView scrollRangeToVisible:NSMakeRange(self.logTextView.text.length, 0)];
    });
}

- (void)runExploit {
    [self appendLog:@"Starting Concrete Balerina..."];
    
    // Get path to bundled input file
    NSString *filePath = [[NSBundle mainBundle] pathForResource:@"orientation-normal-fragmented" ofType:@"mp4.mov"];
    if (!filePath) {
        [self appendLog:@"Error: Input file not found in bundle"];
        return;
    }
    
    // Initialize and run exploit
    Exploit *exploit = [[Exploit alloc] initWithLogCallback:^(const char *log) {
        [self appendLog:[NSString stringWithUTF8String:log]];
    }];
    
    [exploit runExploitWithFilePath:[filePath UTF8String]];
}

@end
