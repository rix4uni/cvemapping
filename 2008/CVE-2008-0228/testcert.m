/*
 *  testcert 
 *
 *  Reference implementation for TWSL2011-007 vulnerability workaround (aka 
 *  CVE-2011-0228).
 *
 *  Author: Eric Monti
 *  Date:   July 28, 2011
 *
 *  = Compiling
 *
 *  Compile with your Apple iOS SDK CFLAGS along with:
 *     gcc -o testcert testcert.m -framework Foundation -framework Security
 *
 *  The compile arguments above should work as-is for OS X if you just want
 *  to check it out.
 *
 *  = Usage:
 *
 *      $ testcert path/to/file.der severname
 *
 *  The file should be in raw DER format, which is just base64-decoded
 *  data found beween the BEGIN and END CERTIFICATE lines in an encoded
 *  certificate:
 *
 *    -----BEGIN CERTIFICATE-----
 *    ...
 *    -----END CERTIFICATE-----
 *  
 *
 *  = License:
 *
 *  Eric Monti
 *  Copyright (C) 2011 Trustwave Holdings
 *  
 *  This program is free software: you can redistribute it and/or modify it 
 *  under the terms of the GNU General Public License as published by the 
 *  Free Software Foundation, either version 3 of the License, or (at your
 *  option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful, but 
 *  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 *  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 *  for more details.
 *  
 *  You should have received a copy of the GNU General Public License along
 *  with this program. If not, see <http://www.gnu.org/licenses/>.
 *  
*/

#import <Foundation/Foundation.h>
#import <CoreFoundation/CoreFoundation.h>

#import <Security/Security.h>

bool isCertValid(CFStringRef leafName, SecCertificateRef leafCert) {
  bool ret=false;
  SecTrustRef trust;
  SecTrustResultType res;
  
  SecPolicyRef policy = SecPolicyCreateSSL(true, leafName);
  OSStatus status = SecTrustCreateWithCertificates((void *)leafCert, policy, &trust);
  
  if ((status == noErr) &&
      (SecTrustEvaluate(trust, &res) == errSecSuccess) && 
      ((res == kSecTrustResultProceed) || (res == kSecTrustResultUnspecified))) 
  { ret = true; }
  
  if (trust) CFRelease(trust);
  if (policy) CFRelease(policy); 
  
  return ret;
}


int main(int argc, char **argv)
{
  int i;

  if (argc < 3) {
    fprintf(stderr, "usage: %s path/to/file.der severname\n", argv[0]);
    exit(1);
  }

  NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];

  NSString *thePath=[NSString stringWithUTF8String:argv[1]];
  CFStringRef serverName = CFStringCreateWithCString(NULL, argv[2], 0);

  CFDataRef certData = (CFDataRef)[[NSData alloc] initWithContentsOfFile:thePath];
  SecCertificateRef cert = SecCertificateCreateWithData(kCFAllocatorDefault, certData);

  CFStringRef desc = SecCertificateCopySubjectSummary(cert);
  if (desc != NULL) {
    printf("Certificate Description: %s\n", CFStringGetCStringPtr(desc, 0));
    CFRelease(desc);
  }
 
  printf("Certificate is ");
  if(isCertValid(serverName, cert))
    printf("VALID\n");
  else
    printf("INVALID!!!\n");

  [pool release];
  return 0;
}
