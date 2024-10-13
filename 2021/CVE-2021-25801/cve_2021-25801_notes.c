Open()
{
    ...
    //only check that ever happens for whether or not an index exists prior to AVI_IndexLoad_indx()
        i_do_index = var_InheritInteger( p_demux, "avi-index" );
    if( i_do_index == 1 ) /* Always fix */
    {
aviindex:
        if( p_sys->b_fastseekable ) //off by default in 3.0.15
        {
            AVI_IndexCreate( p_demux );
        }
        else if( p_sys->b_seekable ) 
        {
            AVI_IndexLoad( p_demux ); //default case
        }
        else
        {
            msg_Warn( p_demux, "cannot create index (unseekable stream)" );
        }
    }
    else if( p_sys->b_seekable )
    {
        AVI_IndexLoad( p_demux );
    }
    ...
}

static void AVI_IndexLoad( demux_t *p_demux )
{
      demux_sys_t *p_sys = p_demux->p_sys;

    /* Load indexes */
    assert( p_sys->i_track <= 100 );
    avi_index_t p_idx_indx[p_sys->i_track];
    avi_index_t p_idx_idx1[p_sys->i_track];
    for( unsigned i = 0; i < p_sys->i_track; i++ )
    {
        avi_index_Init( &p_idx_indx[i] );
        avi_index_Init( &p_idx_idx1[i] );
    }

    uint64_t i_indx_last_pos = p_sys->i_movi_lastchunk_pos; 
    uint64_t i_idx1_last_pos = p_sys->i_movi_lastchunk_pos; 

    AVI_IndexLoad_indx( p_demux, p_idx_indx, &i_indx_last_pos ); 
    if( !p_sys->b_odml )
        AVI_IndexLoad_idx1( p_demux, p_idx_idx1, &i_idx1_last_pos );
        ...
}

//zz open() -> AVI_IndexLoad() -> AVI_IndexLoad_indx() 
static void AVI_IndexLoad_indx( demux_t *p_demux,
                                avi_index_t p_index[], uint64_t *pi_last_offset )
{
    //i_indx_last_pos = p_sys->i_movi_lastchunk_pos;
    demux_sys_t         *p_sys = p_demux->p_sys;

    avi_chunk_list_t    *p_riff;
    avi_chunk_list_t    *p_hdrl;

    p_riff = AVI_ChunkFind( &p_sys->ck_root, AVIFOURCC_RIFF, 0, true);
    p_hdrl = AVI_ChunkFind( p_riff, AVIFOURCC_hdrl, 0, true );

    for( unsigned i_stream = 0; i_stream < p_sys->i_track; i_stream++ )
    {
        avi_chunk_list_t    *p_strl;
        avi_chunk_indx_t    *p_indx;

#define p_stream  p_sys->track[i_stream]
        p_strl = AVI_ChunkFind( p_hdrl, AVIFOURCC_strl, i_stream, true );
        //indx fourcc used in the Super Index Chunk , https://web.archive.org/web/20191226055430/http://www.morgan-multimedia.com/download/odmlff2.pdf - page 16
        p_indx = AVI_ChunkFind( p_strl, AVIFOURCC_indx, 0, false );

        if( !p_indx )
        {
            if( p_sys->b_odml )
                msg_Warn( p_demux, "cannot find indx (misdetect/broken OpenDML file?)" );
            continue;
        }

        if( p_indx->i_indextype == AVI_INDEX_OF_CHUNKS ) 
        {
            __Parse_indx( p_demux, &p_index[i_stream], pi_last_offset, p_indx );
        }
        else if( p_indx->i_indextype == AVI_INDEX_OF_INDEXES ) //this is the expected value for super index
        {
            if ( !p_sys->b_seekable )
                return;
            //if seekable & INDEX_of_INDEXES
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

            /*//CVE-2021-25801 subsequently changed to:
            if( ck_sub.common.i_chunk_fourcc == AVIFOURCC_indx &&
                     ck_sub.indx.i_indextype == AVI_INDEX_OF_CHUNKS )
                    __Parse_indx( p_demux, &p_index[i_stream], pi_last_offset, &ck_sub.indx );*/
        }
 else
        {
            msg_Warn( p_demux, "unknown type index(0x%x)", p_indx->i_indextype );
        }
#undef p_stream

    }
}

//AVI_IndexLoad_indx() -> __Parse_indx()
static void __Parse_indx( demux_t *p_demux, avi_index_t *p_index, uint64_t *pi_max_offset,
                          avi_chunk_indx_t *p_indx )
{
    //i_indx_last_pos = p_sys->i_movi_lastchunk_pos
    //p_indx = &ck_sub.indx
    //p_index = &p_index[istream]
    avi_entry_t index;

    p_demux->p_sys->b_indexloaded = true;

    msg_Dbg( p_demux, "loading subindex(0x%x) %d entries", p_indx->i_indextype, p_indx->i_entriesinuse );
    if( p_indx->i_indexsubtype == 0 )
    {
        //overflow by setting i_entriesinuse to arbitrary high value resulting in out of bounds read?
        for( unsigned i = 0; i < p_indx->i_entriesinuse; i++ )
        {
                            //indxFieldChunk.dwChunkId
            index.i_id     = p_indx->i_id;
                            //?indxFieldChunk.dwSize[0:0]  
            index.i_flags  = p_indx->idx.std[i].i_size & 0x80000000 ? 0 : AVIIF_KEYFRAME; //only keep the most significant bit
                            //indxFieldChunk.qwBaseOffset  + indxFieldChunk.dwOffset - 8
            index.i_pos    = p_indx->i_baseoffset + p_indx->idx.std[i].i_offset - 8; //0x00 - 0xfffffff7
                            //?indxFieldChunk.dwSize[1:7]
            index.i_length = p_indx->idx.std[i].i_size&0x7fffffff; //set most significant bit to 0
            index.i_lengthtotal = index.i_length;

            avi_index_Append( p_index, pi_max_offset, &index );
        }
    }
    else if( p_indx->i_indexsubtype == AVI_INDEX_2FIELD )
    {
        for( unsigned i = 0; i < p_indx->i_entriesinuse; i++ )
        {
            index.i_id     = p_indx->i_id;
            index.i_flags  = p_indx->idx.field[i].i_size & 0x80000000 ? 0 : AVIIF_KEYFRAME;
            index.i_pos    = p_indx->i_baseoffset + p_indx->idx.field[i].i_offset - 8;  //<-Access Violation occurs here?
            index.i_length = p_indx->idx.field[i].i_size;
            index.i_lengthtotal = index.i_length;

            avi_index_Append( p_index, pi_max_offset, &index );
        }
    }
    else
    {
        msg_Warn( p_demux, "unknown subtype index(0x%x)", p_indx->i_indexsubtype );
    }
}

void AVI_ChunkClean( stream_t *s,
                     avi_chunk_t *p_chk )
{
    int i_index;
    avi_chunk_t *p_child, *p_next;

    if( !p_chk )
    {
        return;
    }

    /* Free all child chunk */
    p_child = p_chk->common.p_first;
    while( p_child )
    {
        p_next = p_child->common.p_next;
        AVI_ChunkClean( s, p_child );
        free( p_child );
        p_child = p_next;
    }

    i_index = AVI_ChunkFunctionFind( p_chk->common.i_chunk_fourcc );
    if( AVI_Chunk_Function[i_index].AVI_ChunkFree_function )
    {
#ifdef AVI_DEBUG
        msg_Dbg( (vlc_object_t*)s, "free chunk %4.4s",
                 (char*)&p_chk->common.i_chunk_fourcc );
#endif
        AVI_Chunk_Function[i_index].AVI_ChunkFree_function( p_chk);
    }
    else if( p_chk->common.i_chunk_fourcc != 0 )
    {
        msg_Warn( (vlc_object_t*)s, "unknown chunk: %4.4s (not unloaded)",
                (char*)&p_chk->common.i_chunk_fourcc );
    }
    p_chk->common.p_first = NULL;

    return;
}


//__Parse_index() -> avi_index_Append()
static void avi_index_Append( avi_index_t *p_index, uint64_t *pi_last_pos, avi_entry_t *p_entry )
{
    //p_entry = ck_sub.indx.p_indx[]
    i_indx_last_pos = p_sys->i_movi_lastchunk_pos
   
    /* Update last chunk position */
    if( *pi_last_pos < p_entry->i_pos )
         *pi_last_pos = p_entry->i_pos; //i_movi_lastchunk_pos - 0xfffffff7

    /* add the entry */
    if( p_index->i_size >= p_index->i_max )
    {
        p_index->i_max += 16384;
        p_index->p_entry = realloc_or_free( p_index->p_entry,
                                            p_index->i_max * sizeof( *p_index->p_entry ) );
        /*vlc_arrays.h
        static inline void *realloc_or_free( void *p, size_t sz )
            {
                void *n = realloc(p,sz);
                if( !n )
                    free(p);
                return n;
            }
        */
        if( !p_index->p_entry )
            return;
    }
   
    /* calculate cumulate length */
    if( p_index->i_size > 0 )
    {
        p_entry->i_lengthtotal =
            p_index->p_entry[p_index->i_size - 1].i_length +
                p_index->p_entry[p_index->i_size - 1].i_lengthtotal;
    }
    else
    {
        p_entry->i_lengthtotal = 0;
    }
    //is this the buffer overflow?
    //if i_size > sizeof( p_index->p_entry) == BO?
    //TODO do we control i_size?
    p_index->p_entry[p_index->i_size++] = *p_entry;
}


//__Parse_indx() -> AVI_ChunkRead() && AVI_IndexLoad_indx()
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

//libavi.c
static int AVI_NextChunk( stream_t *s, avi_chunk_t *p_chk )
{
    avi_chunk_t chk;

    if( !p_chk )
    {
        if( AVI_ChunkReadCommon( s, &chk, NULL ) )
        {
            return VLC_EGENERIC;
        }
        p_chk = &chk;
    }

    return AVI_GotoNextChunk( s, p_chk );
}

//AVI_ChunkRead() -> AVI_ChunkReadCommon()
static int AVI_ChunkReadCommon( stream_t *s, avi_chunk_t *p_chk,
                                const avi_chunk_t *p_father )
{
    const uint8_t *p_peek;

    memset( p_chk, 0, sizeof( avi_chunk_t ) );

    const uint64_t i_pos = vlc_stream_Tell( s );
    if( vlc_stream_Peek( s, &p_peek, 8 ) < 8 )
    {
        if( stream_Size( s ) > 0 && (uint64_t) stream_Size( s ) > i_pos )
            msg_Warn( s, "can't peek at %"PRIu64, i_pos );
        else
            //creating an indx that points to an absolute offset outside of the file results in this error thrown
            msg_Dbg( s, "no more data at %"PRIu64, i_pos );
        return VLC_EGENERIC;
    }

    p_chk->common.i_chunk_fourcc = GetFOURCC( p_peek );
    p_chk->common.i_chunk_size   = GetDWLE( p_peek + 4 );
    p_chk->common.i_chunk_pos    = i_pos;

    if( p_chk->common.i_chunk_size >= UINT64_MAX - 8 ||
        p_chk->common.i_chunk_pos > UINT64_MAX - 8 ||
        UINT64_MAX - p_chk->common.i_chunk_pos - 8 < __EVEN(p_chk->common.i_chunk_size) )
        return VLC_EGENERIC;

    if( p_father && AVI_ChunkEnd( p_chk ) > AVI_ChunkEnd( p_father ) )
    {
        msg_Warn( s, "chunk %4.4s does not fit into parent %"PRIu64,
                  (char*)&p_chk->common.i_chunk_fourcc, AVI_ChunkEnd( p_father ) );

        /* How hard is to produce files with the correct declared size ? */
        if( p_father->common.i_chunk_fourcc != AVIFOURCC_RIFF ||
            p_father->common.p_father == NULL ||
            p_father->common.p_father->common.p_father != NULL ) /* Root > RIFF only */
            return VLC_EGENERIC;
    }

#ifdef AVI_DEBUG
    msg_Dbg( (vlc_object_t*)s,
             "found chunk, fourcc: %4.4s size:%"PRIu64" pos:%"PRIu64,
             (char*)&p_chk->common.i_chunk_fourcc,
             p_chk->common.i_chunk_size,
             p_chk->common.i_chunk_pos );
#endif
    return VLC_SUCCESS;
}


//AVI_ChunkReadCommon() -> vlc_stream_Peek( s, &p_peek, 8 )
//src/input/stream.c
ssize_t vlc_stream_Peek(stream_t *s, const uint8_t **restrict bufp, size_t len)
{
    stream_priv_t *priv = (stream_priv_t *)s; 
    block_t *peek;

    peek = priv->peek;
    if (peek == NULL)
    {
        peek = priv->block;
        priv->peek = peek;
        priv->block = NULL;
    }
    //hit
    if (peek == NULL)
    {
        peek = block_Alloc(len);
        if (unlikely(peek == NULL))
            return VLC_ENOMEM;

        peek->i_buffer = 0;
    }
    else
    if (peek->i_buffer < len)
    {
        size_t avail = peek->i_buffer;

        peek = block_TryRealloc(peek, 0, len);
        if (unlikely(peek == NULL))
            return VLC_ENOMEM;

        peek->i_buffer = avail;
    }

    priv->peek = peek;
    *bufp = peek->p_buffer;

    while (peek->i_buffer < len)
    {
        size_t avail = peek->i_buffer;
        ssize_t ret;

        ret = vlc_stream_ReadRaw(s, peek->p_buffer + avail, len - avail);
        if (ret < 0)
            continue;

        peek->i_buffer += ret;

        if (ret == 0)
            return peek->i_buffer;
    }

    return len;
}

//libavi.c
// AVI_IndexLoad_indx() -> AVI_ChunkFind()
void *AVI_ChunkFind_( avi_chunk_t *p_chk,
                      vlc_fourcc_t i_fourcc, int i_number, bool b_list )
{
    if( !p_chk )
        return NULL;

    for( avi_chunk_t *p_child = p_chk->common.p_first;
                      p_child; p_child = p_child->common.p_next )
    {
        if( b_list && p_child->list.i_type == 0 )
            continue;

        if( p_child->common.i_chunk_fourcc != i_fourcc &&
            (!b_list || p_child->list.i_type != i_fourcc) )
            continue;

        if( i_number-- == 0 )
            return p_child; /* We found it */
    }

    return NULL;
}

static int AVI_ChunkRead_indx( stream_t *s, avi_chunk_t *p_chk )
{
    unsigned int i_count, i;
    int          i_ret = VLC_SUCCESS;
    int32_t      i_dummy;
    VLC_UNUSED(i_dummy);
    avi_chunk_indx_t *p_indx = (avi_chunk_indx_t*)p_chk;

    AVI_READCHUNK_ENTER;

    AVI_READ2BYTES( p_indx->i_longsperentry );
    AVI_READ1BYTE ( p_indx->i_indexsubtype );
    AVI_READ1BYTE ( p_indx->i_indextype );
    AVI_READ4BYTES( p_indx->i_entriesinuse );

    AVI_READ4BYTES( p_indx->i_id );
    p_indx->idx.std     = NULL;
    p_indx->idx.field   = NULL;
    p_indx->idx.super   = NULL;

    if( p_indx->i_indextype == AVI_INDEX_OF_CHUNKS && p_indx->i_indexsubtype == 0 )
    {
        AVI_READ8BYTES( p_indx->i_baseoffset );
        AVI_READ4BYTES( i_dummy );
        /*
        #define AVI_READCHUNK_ENTER \
        int64_t i_read = __EVEN(p_chk->common.i_chunk_size ) + 8; \
        if( i_read > 100000000 ) \
        { \
            msg_Err( s, "Big chunk ignored" ); \
            return VLC_EGENERIC; \
        } \

        */
        i_count = __MIN( p_indx->i_entriesinuse, i_read / 8 );
        p_indx->i_entriesinuse = i_count;
        p_indx->idx.std = calloc( i_count, sizeof( indx_std_entry_t ) );
        if( i_count == 0 || p_indx->idx.std )
        {
            for( i = 0; i < i_count; i++ )
            {
                AVI_READ4BYTES( p_indx->idx.std[i].i_offset );
                AVI_READ4BYTES( p_indx->idx.std[i].i_size );
            }
        }
        else i_ret = VLC_EGENERIC;
    }
    else if( p_indx->i_indextype == AVI_INDEX_OF_CHUNKS && p_indx->i_indexsubtype == AVI_INDEX_2FIELD )
    {
        AVI_READ8BYTES( p_indx->i_baseoffset );
        AVI_READ4BYTES( i_dummy );

        i_count = __MIN( p_indx->i_entriesinuse, i_read / 12 );
        p_indx->i_entriesinuse = i_count;
        p_indx->idx.field = calloc( i_count, sizeof( indx_field_entry_t ) );
        if( i_count == 0 || p_indx->idx.field )
        {
            for( i = 0; i < i_count; i++ )
            {
                AVI_READ4BYTES( p_indx->idx.field[i].i_offset );
                AVI_READ4BYTES( p_indx->idx.field[i].i_size );
                AVI_READ4BYTES( p_indx->idx.field[i].i_offsetfield2 );
            }
        }
        else i_ret = VLC_EGENERIC;
    }
    else if( p_indx->i_indextype == AVI_INDEX_OF_INDEXES )
    {
        p_indx->i_baseoffset = 0;
        AVI_READ4BYTES( i_dummy );
        AVI_READ4BYTES( i_dummy );
        AVI_READ4BYTES( i_dummy );

        i_count = __MIN( p_indx->i_entriesinuse, i_read / 16 );
        p_indx->i_entriesinuse = i_count;
        p_indx->idx.super = calloc( i_count, sizeof( indx_super_entry_t ) );
        if( i_count == 0 || p_indx->idx.super )
        {
            for( i = 0; i < i_count; i++ )
            {
                AVI_READ8BYTES( p_indx->idx.super[i].i_offset );
                AVI_READ4BYTES( p_indx->idx.super[i].i_size );
                AVI_READ4BYTES( p_indx->idx.super[i].i_duration );
            }
        }
        else i_ret = VLC_EGENERIC;
    }
    else
    {
        msg_Warn( (vlc_object_t*)s, "unknown type/subtype index" );
    }

#ifdef AVI_DEBUG
    msg_Dbg( (vlc_object_t*)s, "indx: type=%d subtype=%d entry=%d",
             p_indx->i_indextype, p_indx->i_indexsubtype, p_indx->i_entriesinuse );
#endif
    AVI_READCHUNK_EXIT( i_ret );
}

///src/input/stream.c
int vlc_stream_Seek(stream_t *s, uint64_t offset)
{
    stream_priv_t *priv = (stream_priv_t *)s;

    priv->eof = false;

    block_t *peek = priv->peek;
    if (peek != NULL)
    {
        if (offset >= priv->offset
         && offset <= (priv->offset + peek->i_buffer))
        {   /* Seeking within the peek buffer */
            size_t fwd = offset - priv->offset;

            peek->p_buffer += fwd;
            peek->i_buffer -= fwd;
            priv->offset = offset;

            if (peek->i_buffer == 0)
            {
                priv->peek = NULL;
                block_Release(peek);
            }

            return VLC_SUCCESS;
        }
    }
    else
    {
        if (priv->offset == offset)
            return VLC_SUCCESS; /* Nothing to do! */
    }

    if (s->pf_seek == NULL)
        return VLC_EGENERIC;

    int ret = s->pf_seek(s, offset);
    if (ret != VLC_SUCCESS)
        return ret;

    priv->offset = offset;

    if (peek != NULL)
    {
        priv->peek = NULL;
        block_Release(peek);
    }

    if (priv->block != NULL)
    {
        block_Release(priv->block);
        priv->block = NULL;
    }

    return VLC_SUCCESS;
}

//libavi.c
static int AVI_GotoNextChunk( stream_t *s, const avi_chunk_t *p_chk )
{
    bool b_seekable = false;
    const uint64_t i_offset = AVI_ChunkEnd( p_chk );
    if ( !vlc_stream_Control(s, STREAM_CAN_SEEK, &b_seekable) && b_seekable )
    {
        return vlc_stream_Seek( s, i_offset );
    }
    else
    {
        ssize_t i_read = i_offset - vlc_stream_Tell( s );
        return (i_read >=0 && vlc_stream_Read( s, NULL, i_read ) == i_read) ?
                    VLC_SUCCESS : VLC_EGENERIC;
    }
}

//libavi.c
static uint64_t AVI_ChunkEnd( const avi_chunk_t *p_ck )
{
    return p_ck->common.i_chunk_pos + AVI_ChunkSize( p_ck );
}

