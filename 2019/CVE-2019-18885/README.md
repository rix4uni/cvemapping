# CVE-2019-18885


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [CVE-2019-18885](#cve-2019-18885)
  - [bobfuzzer](#bobfuzzer)
    - [Team Members](#team-members)
  - [Infomations](#infomations)
    - [Overview](#overview)
    - [Target](#target)
    - [Reproduce](#reproduce)
    - [Bug Causes](#bug-causes)
    - [Debugger View](#debugger-view)
    - [KASAN Logs](#kasan-logs)
  - [Acknowledgments](#acknowledgments)

<!-- /code_chunk_output -->

---


## bobfuzzer
project team in BoB(a.k.a Best of the Best), Republic of Korea. ([bobfuzzer@gmail.com](mailto:bobfuzzer@gmail.com))

finding bugs in linux kernel filesystem modules


### Team Members
**Project Member**: 김동희([Kieast](https://github.com/Kieast)), 조형진([zkaryaJo](https://github.com/zkaryaJo)), 홍승표([Ph4nt0m](https://github.com/Phantomn)), 남지효([NJhyo](https://github.com/NJhyo)), 정원영([nonetype](https://github.com/nonetype))

**Project Leader**: 조성준([DelspoN](https://github.com/delspon))

**Project Mentor**: 이상섭([k1rh4](https://github.com/k1rh4)), 박천성([Ashine](https://github.com/ash1n2/))

---

## Infomations
null dereference in btrfs_verify_dev_extents(loop list entry)


### Overview
on mounting crafted btrfs image, got Null-Ptr-Deref.


### Target
Tested on Linux Kernel 5.0.21 BTRFS filesystem(source [here](https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.0.21.tar.gz))

(It can be need `CONFIG_BTRFS_FS=m` option.)


### Reproduce
attached crafted image on [here](/poc_2019_18885.zip)
```sh
mkdir ./mnt
mount -t btrfs ./poc_2019_18885.img ./mnt
```


### Bug Causes
fs/btrfs/volumes.c:430
```c
static struct btrfs_device *find_device(struct btrfs_fs_devices *fs_devices,
		u64 devid, const u8 *uuid)
{
	struct btrfs_device *dev;

[1]	list_for_each_entry(dev, &fs_devices->devices, dev_list) {
		if (dev->devid == devid &&
		    (!uuid || !memcmp(dev->uuid, uuid, BTRFS_UUID_SIZE))) {
			return dev;
		}
	}
	return NULL;
}
```
in `list_for_each_entry` loop(`[1]`), `&fs_devices->devices` list entry can be NULL

### Debugger View
```
[ Legend: Modified register | Code | Heap | Stack | String ]
─────────────────────────────────────────────────────────── registers ────
$rax   : 0x0000000000000000  →  0x0000000000000000
$rbx   : 0xdffffc0000000000  →  0xdffffc0000000000
$rcx   : 0x0000000000000098  →  0x0000000000000098
$rdx   : 0x0000000000000013  →  0x0000000000000013
$rsp   : 0xffff888063d4e620  →  0xffff888067d9a200  →  0x1e44a09cf7d0cbce →  0x1e44a09cf7d0cbce
$rbp   : 0x0000000000c00000  →  0x0000000000c00000
$rsi   : 0x0000000000000001  →  0x0000000000000001
$rdi   : 0xffff88806a4eb248  →  0x0000000000000000  →  0x0000000000000000
$rip   : 0xffffffff81def0e8  →  0x0890850f001a3c80  →  0x0890850f001a3c80
$r8    : 0x1ffff1100d49d781  →  0x1ffff1100d49d781
$r9    : 0x0000000000000000  →  0x0000000000000000
$r10   : 0x0000000000000001  →  0x0000000000000001
$r11   : 0xffffed100cfb3463  →  0x0000000000000000  →  0x0000000000000000
$r12   : 0x0000000000000000  →  0x0000000000000000
$r13   : 0xffff888069f3b4d0  →  0xffff888069d0a560  →  0x0000000001c09000 →  0x0000000001c09000
$r14   : 0x0000000000000001  →  0x0000000000000001
$r15   : 0xffff8880696ee1a0  →  0xffff8880696ee000  →  0x0000000000000001 →  0x0000000000000001
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflowresume virtualx86 identification]
$cs: 0x0010 $ss: 0x0018 $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
─────────────────────────────────────────────────────────────── stack ────
0xffff888063d4e620│+0x0000: 0xffff888067d9a200  →  0x1e44a09cf7d0cbce  →0x1e44a09cf7d0cbce	 ← $rsp
0xffff888063d4e628│+0x0008: 0xffff888063d4e6b8  →  0x0000000000000001  →0x0000000000000001
0xffff888063d4e630│+0x0010: 0xffffed100c7a9cdf  →  0x00000000f2f8f8f8  →0x00000000f2f8f8f8
0xffff888063d4e638│+0x0018: 0x0000000000800000  →  0x0000000000800000
0xffff888063d4e640│+0x0020: 0xffff888063d4e6c0  →  0x00000000c00000cc  →0x00000000c00000cc
0xffff888063d4e648│+0x0028: 0xffff888063d4e6f8  →  0x0000000000000001  →0x0000000000000001
0xffff888063d4e650│+0x0030: 0xffff888067d9a318  →  0x0000000000000000  →0x0000000000000000
0xffff888063d4e658│+0x0038: 0x0000000000800000  →  0x0000000000800000
───────────────────────────────────────────────────────── code:x86:64 ────
   0xffffffff81def0da <btrfs_verify_dev_extents+1898> lea    rcx, [rax+0x98]
   0xffffffff81def0e1 <btrfs_verify_dev_extents+1905> mov    rdx, rcx
   0xffffffff81def0e4 <btrfs_verify_dev_extents+1908> shr    rdx, 0x3
 → 0xffffffff81def0e8 <btrfs_verify_dev_extents+1912> cmp    BYTE PTR [rdx+rbx*1], 0x0
   0xffffffff81def0ec <btrfs_verify_dev_extents+1916> jne    0xffffffff81def982 <btrfs_verify_dev_extents+4114>
   0xffffffff81def0f2 <btrfs_verify_dev_extents+1922> mov    rax, QWORD PTR [rax+0x98]
   0xffffffff81def0f9 <btrfs_verify_dev_extents+1929> cmp    rax, rcx
   0xffffffff81def0fc <btrfs_verify_dev_extents+1932> je     0xffffffff81def95c <btrfs_verify_dev_extents+4076>
   0xffffffff81def102 <btrfs_verify_dev_extents+1938> lea    rdi, [rax+0x88]
─────────────────────────────────────── source:fs/btrfs/volumes.c+430 ────
    425	 static struct btrfs_device *find_device(struct btrfs_fs_devices *fs_devices,
    426	 		u64 devid, const u8 *uuid)
    427	 {
    428	 	struct btrfs_device *dev;
    429
 →  430	 	list_for_each_entry(dev, &fs_devices->devices, dev_list) {
    431	 		if (dev->devid == devid &&
    432	 		    (!uuid || !memcmp(dev->uuid, uuid, BTRFS_UUID_SIZE))) {
    433	 			return dev;
    434	 		}
    435	 	}
───────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "", stopped, reason: BREAKPOINT
[#1] Id 2, Name: "", stopped, reason: BREAKPOINT
─────────────────────────────────────────────────────────────── trace ────
[#0] 0xffffffff81def0e8 → find_device(uuid=<optimized out>, devid=<optimized out>, fs_devices=<optimized out>)
[#1] 0xffffffff81def0e8 → verify_one_dev_extent(physical_len=<optimized out>, physical_offset=<optimized out>, devid=<optimized out>, chunk_offset=<optimized out>, fs_info=<optimized out>)
[#2] 0xffffffff81def0e8 → btrfs_verify_dev_extents(fs_info=<optimized out>)
[#3] 0xffffffff81d243f0 → open_ctree(sb=0xffff888069cf3b80, fs_devices=<optimized out>, options=<optimized out>)
[#4] 0xffffffff81c7c5d4 → btrfs_fill_super(data=<optimized out>, fs_devices=<optimized out>, sb=<optimized out>)
[#5] 0xffffffff81c7c5d4 → btrfs_mount_root(fs_type=<optimized out>, flags=<optimized out>, device_name=<optimized out>, data=0x0 <irq_stack_union>)
[#6] 0xffffffff816979d9 → mount_fs(type=0xffff88806a4eb248, flags=0x0, name=<optimized out>, data=<optimized out>)
[#7] 0xffffffff8170e8d9 → vfs_kern_mount(type=<optimized out>, flags=<optimized out>, name=0xffff88806c594160 "/dev/loop0", data=0x0 <irq_stack_union>)
[#8] 0xffffffff8170ec2a → vfs_kern_mount(type=<optimized out>, flags=<optimized out>, name=<optimized out>, data=<optimized out>)
[#9] 0xffffffff81c810d5 → btrfs_mount(fs_type=<optimized out>, flags=0x0,device_name=<optimized out>, data=0x0 <irq_stack_union>)
──────────────────────────────────────────────────────────────────────────

Thread 2 hit Breakpoint 1, 0xffffffff81def0e8 in find_device (uuid=<optimized out>, devid=<optimized out>, fs_devices=<optimized out>) at fs/btrfs/volumes.c:430
430		list_for_each_entry(dev, &fs_devices->devices, dev_list) {
```
instruction `cmp    BYTE PTR [rdx+rbx*1], 0x0` trying to read `0xdffffc0000000000 + 0x13` address value


### KASAN Logs
```
[  196.251167] BTRFS: device fsid a62e00e8-e94e-4200-8217-12444de93c2e devid 1 transid 8 /dev/loop0
[  196.392627] BTRFS info (device loop0): disk space caching is enabled
[  196.395228] BTRFS info (device loop0): has skinny extents
[  196.770076] BTRFS critical (device loop0): corrupt leaf: root=1 block=29417472 slot=6 ino=6, name hash mismatch with key, have 0x00000000be52bff8 e
xpect 0x000000008dbfc2d2
[  196.794355] BTRFS info (device loop0): read error corrected: ino 0 off 29417472 (dev /dev/loop0 sector 73840)
[  196.879172] kasan: CONFIG_KASAN_INLINE enabled
[  196.881094] kasan: GPF could be caused by NULL-ptr deref or user memory access
[  196.883004] general protection fault: 0000 [#1] SMP KASAN NOPTI
[  196.883474] CPU: 0 PID: 1989 Comm: mount Not tainted 5.0.21 #1
[  196.883474] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.10.2-1ubuntu1 04/01/2014
[  196.883474] RIP: 0010:btrfs_verify_dev_extents+0x778/0x1140
[  196.883474] Code: c8 00 00 00 48 89 fa 48 c1 ea 03 80 3c 1a 00 0f 85 31 06 00 00 48 8b 80 c8 00 00 00 48 8d 88 98 00 00 00 48 89 ca 48 c1 ea 03 <8$
> 3c 1a 00 0f 85 90 08 00 00 48 8b 80 98 00 00 00 48 39 c8 0f 84

[  196.883474] RSP: 0018:ffff888067eee620 EFLAGS: 00000202
[  196.883474] RAX: 0000000000000000 RBX: dffffc0000000000 RCX: 0000000000000098
[  196.883474] RDX: 0000000000000013 RSI: 0000000000000001 RDI: ffff888069afa348
[  196.883474] RBP: 0000000000c00000 R08: 1ffff1100d8c3f81 R09: 0000000000000000
[  196.883474] R10: 0000000000000001 R11: ffffed100c82f023 R12: 0000000000000000
[  196.883474] R13: ffff888069e5f210 R14: 0000000000000001 R15: ffff888069f061a0
[  196.883474] FS:  00007f581c668e40(0000) GS:ffff88806d000000(0000) knlGS:0000000000000000
[  196.883474] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  196.883474] CR2: 0000564ef42ea000 CR3: 0000000069f98000 CR4: 00000000000006f0[  196.883474] Call Trace:
[  196.883474]  ? run_one_async_done+0x250/0x250
[  196.883474]  ? btrfs_bg_type_to_factor+0x10/0x10
[  196.883474]  ? __kasan_slab_free+0x143/0x180
[  196.883474]  ? btrfs_read_tree_root+0x166/0x330
[  196.883474]  ? btrfs_read_tree_root+0x166/0x330
[  196.883474]  open_ctree+0x4cd0/0x7ada
[  196.883474]  ? close_ctree+0xa10/0xa10
[  196.883474]  ? __lock_text_start+0x8/0x8
[  196.883474]  ? __save_stack_trace+0x8d/0xf0
[  196.883474]  ? depot_save_stack+0x2d9/0x470
[  196.883474]  ? lockref_put_or_lock+0x1c0/0x360
[  196.883474]  ? lockref_put_return+0x280/0x280
[  196.883474]  ? __debugfs_create_file+0x69/0x380
[  196.883474]  ? super_setup_bdi_name+0x135/0x260
[  196.883474]  ? mount_fs+0xb9/0x370
[  196.883474]  ? vfs_kern_mount.part.28+0xb9/0x400
[  196.883474]  ? mount_fs+0xb9/0x370
[  196.883474]  ? vfs_kern_mount.part.28+0xb9/0x400
[  196.883474]  ? do_mount+0xef4/0x2d40
[  196.883474]  ? ksys_mount+0x7b/0xd0
[  196.883474]  ? do_syscall_64+0x12b/0x440
[  196.883474]  ? __dentry_path+0x31e/0x6e0
[  196.883474]  ? rcu_qs+0x2f0/0x2f0
[  196.883474]  ? __alloc_pages_nodemask+0x467/0xa00
[  196.883474]  ? dput+0x33b/0x540
[  196.883474]  ? rcu_qs+0x2f0/0x2f0
[  196.883474]  ? page_alloc_cpu_dead+0x30/0x30
[  196.883474]  ? free_pcp_prepare+0xb8/0x220
[  196.883474]  ? _raw_spin_lock+0x99/0x130
[  196.883474]  ? _raw_read_lock_irq+0x30/0x30
[  196.883474]  ? __fsnotify_inode_delete+0x10/0x10
[  196.883474]  ? get_nr_inodes+0xf0/0xf0
[  196.883474]  ? __d_instantiate+0x366/0x6e0
[  196.883474]  ? __lookup_slow+0x1f7/0x450
[  196.883474]  ? rcu_qs+0x2f0/0x2f0
[  196.883474]  ? _raw_spin_lock+0x30/0x130
[  196.883474]  ? _raw_read_lock_irq+0x30/0x30
[  196.883474]  ? _raw_read_lock_irq+0x30/0x30
[  196.883474]  ? _raw_spin_lock+0x99/0x130
[  196.883474]  ? _raw_read_lock_irq+0x30/0x30
[  196.883474]  ? _raw_spin_lock_bh+0xa4/0x130
[  196.883474]  ? _raw_write_trylock+0x1f0/0x1f0
[  196.883474]  ? __debugfs_create_file+0x277/0x380
[  196.883474]  ? debugfs_create_dir+0x286/0x360
[  196.883474]  ? address_val+0x90/0x90
[  196.883474]  ? set_wb_congested+0x30/0x30
[  196.883474]  ? rcu_qs+0x2f0/0x2f0
[  196.883474]  ? __kasan_kmalloc.constprop.4+0xa0/0xd0
[  196.883474]  ? super_setup_bdi_name+0x135/0x260
[  196.883474]  ? kill_block_super+0xd0/0xd0
[  196.883474]  ? snprintf+0x8f/0xc0
[  196.883474]  ? btrfs_mount_root+0xe24/0x14c0
[  196.883474]  btrfs_mount_root+0xe24/0x14c0
[  196.883474]  ? btrfs_decode_error+0x50/0x50
[  196.883474]  ? module_enable_ro.part.69+0x160/0x160
[  196.883474]  ? deref_stack_reg+0xab/0x110
[  196.883474]  ? __read_once_size_nocheck.constprop.8+0x10/0x10
[  196.883474]  ? deref_stack_reg+0xab/0x110
[  196.883474]  ? __free_insn_slot+0x450/0x450
[  196.883474]  ? rcu_is_watching+0x7d/0x130
[  196.883474]  ? entry_SYSCALL_64_after_hwframe+0x44/0xa9
[  196.883474]  ? rcu_barrier_trace+0x260/0x260
[  196.883474]  ? mount_fs+0xb9/0x370
[  196.883474]  ? btrfs_decode_error+0x50/0x50
[  196.883474]  mount_fs+0xb9/0x370
[  196.883474]  ? pcpu_next_unpop+0xe0/0xe0
[  196.883474]  ? __kernel_text_address+0x9/0x30
[  196.883474]  ? emergency_thaw_all+0x230/0x230
[  196.883474]  ? apic_timer_interrupt+0xa/0x20
[  196.883474]  vfs_kern_mount.part.28+0xb9/0x400
[  196.883474]  ? __cleanup_mnt+0x10/0x10
[  196.883474]  ? __lock_text_start+0x8/0x8
[  196.883474]  ? pcpu_alloc_area+0x170/0x3c0
[  196.883474]  btrfs_mount+0x3c5/0x1fd9
[  196.883474]  ? btrfs_remount+0x1190/0x1190
[  196.883474]  ? ida_free+0x3b0/0x3b0
[  196.883474]  ? kasan_unpoison_shadow+0x30/0x40
[  196.883474]  ? __kasan_kmalloc.constprop.4+0xa0/0xd0
[  196.883474]  ? dl_cpu_busy+0x1f0/0x1f0
[  196.883474]  ? alloc_vfsmnt+0x146/0x950
[  196.883474]  ? memcpy+0x34/0x50
[  196.883474]  ? alloc_vfsmnt+0x617/0x950
[  196.883474]  ? m_stop+0x10/0x10
[  196.883474]  ? memcpy+0x34/0x50
[  196.883474]  ? avc_has_perm_noaudit+0x22a/0x4c0
[  196.883474]  ? avc_has_perm+0x24f/0x620
[  196.883474]  ? avc_has_extended_perms+0x1320/0x1320
[  196.883474]  ? __read_once_size_nocheck.constprop.8+0x10/0x10
[  196.883474]  ? mount_fs+0xb9/0x370
[  196.883474]  mount_fs+0xb9/0x370
[  196.883474]  ? emergency_thaw_all+0x230/0x230
[  196.883474]  ? __module_get+0x1a0/0x1a0
[  196.883474]  ? selinux_sb_eat_lsm_opts+0x520/0x520
[  196.883474]  vfs_kern_mount.part.28+0xb9/0x400
[  196.883474]  ? __cleanup_mnt+0x10/0x10
[  196.883474]  ? getname_flags+0xb5/0x500
[  196.883474]  ? __get_fs_type+0x79/0xb0
[  196.883474]  do_mount+0xef4/0x2d40
[  196.883474]  ? copy_mount_string+0x20/0x20
[  196.883474]  ? save_stack+0x89/0xb0
[  196.883474]  ? __kasan_kmalloc.constprop.4+0xa0/0xd0
[  196.883474]  ? __kmalloc_track_caller+0xc7/0x1d0
[  196.883474]  ? memdup_user+0x23/0x60
[  196.883474]  ? __x64_sys_mount+0xb5/0x150
[  196.883474]  ? do_syscall_64+0x12b/0x440
[  196.883474]  ? entry_SYSCALL_64_after_hwframe+0x44/0xa9
[  196.883474]  ? security_file_free+0x3a/0x70
[  196.883474]  ? kmem_cache_free+0x70/0x1a0
[  196.883474]  ? __fput+0x3f1/0x840
[  196.883474]  ? _copy_to_user+0x68/0x90
[  196.883474]  ? _raw_spin_lock_irq+0x9a/0x130
[  196.883474]  ? _raw_write_unlock_irqrestore+0x110/0x110
[  196.883474]  ? __close_fd+0x32a/0x540
[  196.883474]  ? task_work_run+0xd0/0x290
[  196.883474]  ? rcu_qs+0x2f0/0x2f0
[  196.883474]  ? kasan_unpoison_shadow+0x30/0x40
[  196.883474]  ? __kasan_kmalloc.constprop.4+0xa0/0xd0
[  196.883474]  ? strndup_user+0x42/0x90
[  196.883474]  ? __kmalloc_track_caller+0xc7/0x1d0
[  196.883474]  ? _copy_from_user+0x70/0xa0
[  196.883474]  ? memdup_user+0x39/0x60
[  196.883474]  ksys_mount+0x7b/0xd0
[  196.883474]  __x64_sys_mount+0xb5/0x150
[  196.883474]  do_syscall_64+0x12b/0x440
[  196.883474]  ? syscall_return_slowpath+0x2e0/0x2e0
[  196.883474]  ? prepare_exit_to_usermode+0x1be/0x210
[  196.883474]  ? perf_trace_sys_enter+0x1050/0x1050
[  196.883474]  ? __x64_sys_sigaltstack+0x270/0x270
[  196.883474]  ? __put_user_4+0x1c/0x30
[  196.883474]  entry_SYSCALL_64_after_hwframe+0x44/0xa9
[  196.883474] RIP: 0033:0x7f581bd2348a
[  196.883474] Code: 48 8b 0d 11 fa 2a 00 f7 d8 64 89 01 48 83 c8 ff c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 44 00 00 49 89 ca b8 a5 00 00 00 0f 05 <48
> 3d 01 f0 ff ff 73 01 c3 48 8b 0d de f9 2a 00 f7 d8 64 89 01 48

[  196.883474] RSP: 002b:00007fffbf988ac8 EFLAGS: 00000202 ORIG_RAX: 00000000000000a5
[  196.883474] RAX: ffffffffffffffda RBX: 000055718faa2080 RCX: 00007f581bd2348a
[  196.883474] RDX: 000055718faa2260 RSI: 000055718faa7ec0 RDI: 000055718faa8db0
[  196.883474] RBP: 0000000000000000 R08: 0000000000000000 R09: 0000000000000020
[  196.883474] R10: 00000000c0ed0000 R11: 0000000000000202 R12: 000055718faa8db0
[  196.883474] R13: 000055718faa2260 R14: 0000000000000000 R15: 00000000ffffffff
[  196.883474] Modules linked in:
[  196.934565] ---[ end trace b2518a0a4d2b3ae0 ]---
[  196.935064] RIP: 0010:btrfs_verify_dev_extents+0x778/0x1140
[  196.935271] Code: c8 00 00 00 48 89 fa 48 c1 ea 03 80 3c 1a 00 0f 85 31 06 00 00 48 8b 80 c8 00 00 00 48 8d 88 98 00 00 00 48 89 ca 48 c1 ea 03 <80
> 3c 1a 00 0f 85 90 08 00 00 48 8b 80 98 00 00 00 48 39 c8 0f 84

[  196.939094] RSP: 0018:ffff888067eee620 EFLAGS: 00000202
[  196.942503] RAX: 0000000000000000 RBX: dffffc0000000000 RCX: 0000000000000098
[  196.942811] RDX: 0000000000000013 RSI: 0000000000000001 RDI: ffff888069afa348
[  196.943370] RBP: 0000000000c00000 R08: 1ffff1100d8c3f81 R09: 0000000000000000
[  196.946786] R10: 0000000000000001 R11: ffffed100c82f023 R12: 0000000000000000
[  196.947634] R13: ffff888069e5f210 R14: 0000000000000001 R15: ffff888069f061a0
[  196.950778] FS:  00007f581c668e40(0000) GS:ffff88806d000000(0000) knlGS:0000000000000000
[  196.952541] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  196.952704] CR2: 0000564ef42ea000 CR3: 0000000069f98000 CR4: 00000000000006f0
```

## Acknowledgments
This Project used ported version(to 5.0.21 and 5.3.14 linux kernel) of filesystem fuzzer 'JANUS' which developed by GeorgiaTech Systems Software & Security Lab(SSLab)

Thank you for the excellent fuzzer and paper below.

* [sslab-gatech/janus](https://github.com/sslab-gatech/janus)
* [Fuzzing File Systems via Two-Dimensional Input Space Exploration (IEEE S&P 2019)](https://gts3.org/assets/papers/2019/xu:janus.pdf)
