/* code snippet from /include/linux/msm_kgsl.h */

#ifndef _MSM_KGSL_H
#define _MSM_KGSL_H

/**
 * struct kgsl_gpumem_alloc_id - argument to IOCTL_KGSL_GPUMEM_ALLOC_ID
 * @id: returned id value for this allocation.
 * @flags: mask of KGSL_MEM* values requested and actual flags on return.
 * @size: requested size of the allocation and actual size on return.
 * @mmapsize: returned size to pass to mmap() which may be larger than 'size'
 * @gpuaddr: returned GPU address for the allocation
 *
 * Allocate memory for access by the GPU. The flags and size fields are echoed
 * back by the kernel, so that the caller can know if the request was
 * adjusted.
 *
 * Supported flags:
 * KGSL_MEMFLAGS_GPUREADONLY: the GPU will be unable to write to the buffer
 * KGSL_MEMTYPE*: usage hint for debugging aid
 * KGSL_MEMALIGN*: alignment hint, may be ignored or adjusted by the kernel.
 * KGSL_MEMFLAGS_USE_CPU_MAP: If set on call and return, the returned GPU
 * address will be 0. Calling mmap() will set the GPU address.
 */
struct kgsl_gpumem_alloc_id {
	unsigned int id;
	unsigned int flags;
	unsigned int size;
	unsigned int mmapsize;
	unsigned long gpuaddr;
/* private: reserved for future use*/
	unsigned int __pad[2];
};

#define KGSL_IOC_TYPE	0x09

#define IOCTL_KGSL_GPUMEM_ALLOC_ID \
	_IOWR(KGSL_IOC_TYPE, 0x34, struct kgsl_gpumem_alloc_id)

#endif /* _MSM_KGSL_H */
