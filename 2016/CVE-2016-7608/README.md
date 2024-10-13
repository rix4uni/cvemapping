## IOFireWireFamily-overflow

IOFireWireFamily-overflow is a proof-of-concept exploit for CVE-2016-7608, a buffer overflow in
`IOFireWireUserClient` that was fixed in [macOS Sierra 10.12.2]. This vulnerability can be
triggered to cause denial of service or possibly arbitrary code execution on devices with a
FireWire port.

[macOS Sierra 10.12.2]: https://support.apple.com/en-us/HT207423

### CVE-2016-7608

The `AppleFWOHCI::updateROM` method does not check the length of an `OSData` argument before `bcopy`ing
its contents into a fixed-size memory region allocated using `AppleFWOHCI_IOMemoryBlock32::create`.

The exploit can be triggered using an instance of `IOFireWireUserClient`. Calling the method
`localConfigDirectory_Create` yields a handle to an `IOLocalConfigDirectory`. Arbitrary data can be
added to this directory object using the `localConfigDirectory_addEntry_Buffer` method, which does
not restrict the size of the data beyond the limits of the 32-bit `size` parameter. Finally, the
exploit can be triggered by calling `localConfigDirectory_Publish`, which eventually calls
`IOFireWireController::UpdateROM`. `UpdateROM` creates an `OSData` object representing the compiled
ROM, including the user-controlled data added earlier. It then passes the `OSData` object to
`AppleFWOHCI::updateROM`, which copies the data into the memory region pointed to by
`fpNextConfigROM`. This is a 4096-byte memory region allocated in `AppleFWOHCI::setupAsync` using
`AppleFWOHCI_IOMemoryBlock32::create`. If more than 4096 bytes are passed to
`localConfigDirectory_addEntry_Buffer`, then the write will overflow this allocation onto the
subsequent pages.

In practice, the page after the overflowed buffer is usually unmapped, causing a kernel panic on
overflow.

### License

The IOFireWireFamily-overflow code is released into the public domain. As a courtesy I ask that if
you reference or use any of this code you attribute it to me.
