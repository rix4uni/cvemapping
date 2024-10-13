#include "stdio.h"
#include "stdint.h"
typedef unsigned int u32;
typedef unsigned long u64;

enum vb2_buffer_state {
	VB2_BUF_STATE_DEQUEUED,
	VB2_BUF_STATE_IN_REQUEST,
	VB2_BUF_STATE_PREPARING,
	VB2_BUF_STATE_QUEUED,
	VB2_BUF_STATE_ACTIVE,
	VB2_BUF_STATE_DONE,
	VB2_BUF_STATE_ERROR,
};


struct list_head {
    struct list_head *next;
    struct list_head *prev;
};
struct vb2_mem_ops {
    char off[0x58];
    void *(*vaddr)(void *);

};


struct vb2_plane {
    void *mem_priv;
    char dma_buf[0xf8];
    unsigned int dbuf_mapped;
    unsigned int bytesused;
    unsigned int length;
    unsigned int min_length;
    union {
        unsigned int offset;
        unsigned long userptr;
        int fd;
    } m;
    unsigned int data_offset;
};

struct vb2_queue {
    unsigned int type;
    unsigned int io_modes;
   	u64 device;
    unsigned long dma_attrs;
    unsigned int bidirectional : 1;
    unsigned int fileio_read_once : 1;
    unsigned int fileio_write_immediately : 1;
    unsigned int allow_zero_bytesused : 1;
    unsigned int quirk_poll_must_check_waiting_for_buffers : 1;
    unsigned int supports_requests : 1;
    unsigned int requires_requests : 1;
    unsigned int uses_qbuf : 1;
    unsigned int uses_requests : 1;
    u64 mutex;
    void *owner;
    u64 vb2_ops;
    struct vb2_mem_ops *mem_ops;
    u64 vb2_buf_ops;
    void *drv_priv;
    unsigned int buf_struct_size;
    u32 timestamp_flags;
    u32 gfp_flags;
    u32 min_buffers_needed;
    struct device *alloc_devs[8];
    char mmap_mutex[0x20];
    unsigned int memory;
    char dma_data_direction[4];
    struct vb2_buffer *bufs[32];
    unsigned int num_buffers;
    struct list_head queued_list;
    unsigned int queued_count;
    u32 owned_by_drv_count;
    struct list_head done_list;
    u32 done_lock;
    char  done_wq[0x18];
    unsigned int streaming : 1;
    unsigned int start_streaming_called : 1;
    unsigned int error : 1;
    unsigned int waiting_for_buffers : 1;
    unsigned int waiting_in_dqbuf : 1;
    unsigned int is_multiplanar : 1;
    unsigned int is_output : 1;
    unsigned int copy_timestamp : 1;
    unsigned int last_buffer_dequeued : 1;
    void *fileio;
    void *threadio;
    u32 cnt_queue_setup;
    u32 cnt_wait_prepare;
    u32 cnt_wait_finish;
    u32 cnt_start_streaming;
    u32 cnt_stop_streaming;
};


struct vb2_buffer { 
    struct vb2_queue * vb2_queue;
    unsigned int index;
    unsigned int type;
    unsigned int memory;
    unsigned int num_planes;
    u64 timestamp;
    u64 *media_request;
    char media_request_object[0x30];
    enum vb2_buffer_state state;
    unsigned int synced:1;
    unsigned int prepared:1;
    unsigned int copied_timestamp:1;
    struct vb2_plane planes[8];
    struct list_head queued_entry;
    struct list_head done_entry;
    u32 cnt_mem_alloc;
    u32 cnt_mem_put;
    u32 cnt_mem_get_dmabuf;
    u32 cnt_mem_get_userptr;
    u32 cnt_mem_put_userptr;
    u32 cnt_mem_prepare;
    u32 cnt_mem_finish;
    u32 cnt_mem_attach_dmabuf;
    u32 cnt_mem_detach_dmabuf;
    u32 cnt_mem_map_dmabuf;
    u32 cnt_mem_unmap_dmabuf;
    u32 cnt_mem_vaddr;
    u32 cnt_mem_cookie;
    u32 cnt_mem_num_users;
    u32 cnt_mem_mmap;
    u32 cnt_buf_out_validate;
    u32 cnt_buf_init;
    u32 cnt_buf_prepare;
    u32 cnt_buf_finish;
    u32 cnt_buf_cleanup;
    u32 cnt_buf_queue;
    u32 cnt_buf_request_complete;
    u32 cnt_buf_done;
};
