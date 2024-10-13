# CVE-2021-25801 Analysis

The vulnerability stems from a failure to throughly check the type of chunk being passed to __Parse_indx when attempting to read a sub indx chunk, pointed to by a valid super indx chunk. 

```
  else if( p_indx->i_indextype == AVI_INDEX_OF_INDEXES ) //this is the expected value for super index
        {
            if ( !p_sys->b_seekable )
                return;
            avi_chunk_t    ck_sub;
            for( unsigned i = 0; i < p_indx->i_entriesinuse; i++ )
            {
                if( vlc_stream_Seek( p_demux->s,
                                     p_indx->idx.super[i].i_offset ) ||
                //as long as the chunk isnt null and the fourcc isnt 0 & there are at least 7 bytes left in the file ChunkRead will return a value
                    AVI_ChunkRead( p_demux->s, &ck_sub, NULL  ) )
                {
                    break;
                }
                //CVE-2021-25801
                //super index points to an offset with the 13th byte set to 0x01 
                //but no check is done on whether or not its actually pointing to a valid indx field chunk
                if( ck_sub.indx.i_indextype == AVI_INDEX_OF_CHUNKS )
                    __Parse_indx( p_demux, &p_index[i_stream], pi_last_offset, &ck_sub.indx );
                AVI_ChunkClean( p_demux->s, &ck_sub );
            }
```

The type of chunk of the sub indx is determined by the AVI_ChunkRead function.

```
int  AVI_ChunkRead( stream_t *s, avi_chunk_t *p_chk, avi_chunk_t *p_father )
{
    int i_index;

    if( !p_chk )
    {
        msg_Warn( (vlc_object_t*)s, "cannot read null chunk" );
        return VLC_EGENERIC;
    }

    if( AVI_ChunkReadCommon( s, p_chk, p_father ) )
        return VLC_EGENERIC;

    if( p_chk->common.i_chunk_fourcc == VLC_FOURCC( 0, 0, 0, 0 ) )
    {
        msg_Warn( (vlc_object_t*)s, "found null fourcc chunk (corrupted file?)" );
        return AVI_ZERO_FOURCC;
    }
    p_chk->common.p_father = p_father;
              //This function reads the fourcc value and checks against a vtable for the corresponding ChunkRead function
    i_index = AVI_ChunkFunctionFind( p_chk->common.i_chunk_fourcc );
    if( AVI_Chunk_Function[i_index].AVI_ChunkRead_function )
    {
        return AVI_Chunk_Function[i_index].AVI_ChunkRead_function( s, p_chk );
    }
    else if( ( ((char*)&p_chk->common.i_chunk_fourcc)[0] == 'i' &&
               ((char*)&p_chk->common.i_chunk_fourcc)[1] == 'x' ) ||
             ( ((char*)&p_chk->common.i_chunk_fourcc)[2] == 'i' &&
               ((char*)&p_chk->common.i_chunk_fourcc)[3] == 'x' ) )
    {
        p_chk->common.i_chunk_fourcc = AVIFOURCC_indx;
        return AVI_ChunkRead_indx( s, p_chk );
    }

    msg_Warn( (vlc_object_t*)s, "unknown chunk: %4.4s (not loaded)",
            (char*)&p_chk->common.i_chunk_fourcc );
    return AVI_NextChunk( s, p_chk );
}
```

If the super indx points to a valid chunk of a type smaller than the expected indx chunk we can cause an out of bounds read to occur when the following variables are assigned in __Parse_indx.

```
  for( unsigned i = 0; i < p_indx->i_entriesinuse; i++ )
        {
            index.i_id     = p_indx->i_id;
            index.i_flags  = p_indx->idx.field[i].i_size & 0x80000000 ? 0 : AVIIF_KEYFRAME;
            index.i_pos    = p_indx->i_baseoffset + p_indx->idx.field[i].i_offset - 8;  //<-Access Violation occurs here
            index.i_length = p_indx->idx.field[i].i_size;
            index.i_lengthtotal = index.i_length;

            avi_index_Append( p_index, pi_max_offset, &index );
        }
```

Utilizing a strh fourcc chunk of size 0x34 bytes I was able to successfully pass all of the prerequisite checks to get to the above vulnerable code, resulting in an access violation.

```
avi stream debug: <list 'AVI '>
avi stream debug: <list 'hdrl'>
avi stream debug: <list 'strl'>
avi stream warning: chunk LIST does not fit into parent 4060
avi stream debug: </list 'strl'>ffffffff
avi stream warning: chunk LIST does not fit into parent 4060
avi stream debug: </list 'hdrl'>ffffffff
avi stream debug: skipping movi chunk
avi stream debug: no more data at 4128
avi stream debug: </list 'AVI '>ffffffff
avi stream debug: no more data at 4128
avi stream debug: * LIST-root size:4128 pos:0
avi stream debug:     + RIFF-AVI  size:4124 pos:0
avi stream debug:     |   + LIST-hdrl size:4040 pos:12
avi stream debug:     |   |   + avih size:56 pos:24
avi stream debug:     |   |   + LIST-strl size:3964 pos:88
avi stream debug:     |   |   |   + strh size:56 pos:100
avi stream debug:     |   |   |   + strf size:44 pos:164
avi stream debug:     |   |   |   + indx size:3832 pos:216
avi stream debug:     |   + LIST-movi size:64 pos:4056
avi demux debug: AVIH: 1 stream, flags  HAS_INDEX IS_INTERLEAVED TRUST_CKTYPE 
avi demux debug: stream[0] rate:419430400 scale:16777216 samplesize:0
avi demux debug: stream[0] video(XVID) 640x360 0bpp 25.000000fps
main input debug: selecting program id=0
avi demux debug: loading subindex(0x1) 1870082273 entries
(7fc.9d4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0a77f838 ebx=0029df9f ecx=4f4e4d4c edx=53525150 esi=091f7000 edi=53525150
eip=6f772c43 esp=0a77f750 ebp=0a77f870 iopl=0         nv up ei pl nz ac pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010216
libavi_plugin+0x2c43:
6f772c43 8b7e04          mov     edi,dword ptr [esi+4] ds:002b:091f7004=????????
```

The provided PoC was tested on Windows 11, with VLC version 3.0.11.
