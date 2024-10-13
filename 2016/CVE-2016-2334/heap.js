'use strict'
var allocations = Object();

function toString(out, opt = "")
{
	var str = "";
	for(var line of out)
	{
		str += line + opt
	}
	return str;
}
function readValue(str)
{
	var out = host.namespace.Debugger.Utility.Control.ExecuteCommand("dd poi("+ str +") L1");	
	var str = toString(out);
	return str.split(" ")[0];
}

function dumpObjectTree (o, recurse, compress, level)
{
    var s = "";
    var pfx = "";

    if (typeof recurse == "undefined")
        recurse = 0;
    if (typeof level == "undefined")
        level = 0;
    if (typeof compress == "undefined")
        compress = true;

    for (var i = 0; i < level; i++)
        pfx += (compress) ? "| " : "|  ";

    var tee = (compress) ? "+ " : "+- ";

    for (i in o)
    {
        var t, ex;

        try
        {
            t = typeof o[i];
        }
        catch (ex)
        {
            t = "ERROR";
        }

        switch (t)
        {
            case "function":
                var sfunc = String(o[i]).split("\n");
                if (sfunc[2] == "    [native code]")
                    sfunc = "[native code]";
                else
                    if (sfunc.length == 1)
                        sfunc = String(sfunc);
                    else
                        sfunc = sfunc.length + " lines";
                s += pfx + tee + i + " (function) " + sfunc + "\n";
                break;

            case "object":
                s += pfx + tee + i + " (object)";
                if (o[i] == null)
                {
                    s += " null\n";
                    break;
                }

                s += "\n";

                if (!compress)
                    s += pfx + "|\n";
                if ((i != "parent") && (recurse))
                    s += dumpObjectTree (o[i], recurse - 1,
                                         compress, level + 1);
                break;

            case "string":
                if (o[i].length > 200)
                    s += pfx + tee + i + " (" + t + ") " +
                        o[i].length + " chars\n";
                else
                    s += pfx + tee + i + " (" + t + ") '" + o[i] + "'\n";
                break;

            case "ERROR":
                s += pfx + tee + i + " (" + t + ") ?\n";
                break;

            default:
                s += pfx + tee + i + " (" + t + ") " + o[i] + "\n";

        }

        if (!compress)
            s += pfx + "|\n";

    }

    s += pfx + "*\n";

    return s;

}
function getMethods(obj) 
{
  host.diagnostics.debugLog("inside getMethods");
  var result = [];
  for (var id in obj) {
    try {
      if (typeof(obj[id]) == "function") {
        result.push(id + ": " + obj[id].toString());
      }
    } catch (err) {
      result.push(id + ": inaccessible");
    }
  }
  return result;
}

function initializeScript()
{
	host.diagnostics.debugLog("[+] HeapInspector loaded!s\n");	
}

function getAllocation(addr)
{
	return allocations[addr];
}

function showStackTrace(addr)
{
	host.diagnostics.debugLog(allocations[addr].stack);
}
function dumpAllocations()
{
	var addresses = Object.keys(allocations);
	for(var addr of addresses)
	{
		host.diagnostics.debugLog("Address : " + allocations[addr].addr + "\n");
		host.diagnostics.debugLog("Size : " + allocations[addr].size + "\n");
		host.diagnostics.debugLog("Stack : " + allocations[addr].stack + "\n");
	}
}
function getStackTrace()
{
	var out = host.namespace.Debugger.Utility.Control.ExecuteCommand("kc");	
	return toString(out,"\n");
}

function handleRtlHeapAlloc()
{
	var heapHandle = readValue("esp+4");
	var flags = readValue("esp+8");
	var size = readValue("esp+C");
	var addr = Number(host.namespace.Debugger.State.DebuggerVariables.curthread.Registers.User.eax).toString(16);
	host.diagnostics.debugLog("RtlHeapAlloc("+heapHandle+","+flags + ","+size+") = " + addr + "\n");		
	allocations[addr] = {"addr" : addr, "size" : size, "heap" : heapHandle, "stack": getStackTrace()};
}

function handleRtlFreeHeap()
{
	var heapHandle = readValue("esp+4");
	var flags = readValue("esp+8");
	var addr = readValue("esp+C");
	host.diagnostics.debugLog("RtlFreeHeap("+heapHandle+","+flags + ","+addr+"\n");			
}

function handleRtlReAllocateHeap()
{
	var heapHandle = readValue("esp+4");
	var flags = readValue("esp+8");
	var memPtr = readValue("esp+C");
	var size = readValue("esp+0x10");
	var addr = Number(host.namespace.Debugger.State.DebuggerVariables.curthread.Registers.User.eax).toString(16);
	host.diagnostics.debugLog("RtlReAllocateHeap("+heapHandle+","+flags + ","+memPtr+","+size+") = " + addr + "\n");		
	allocations[addr] = {"addr" : addr, "size" : size, "heap" : heapHandle, "stack": 0};
}


function showHeap(heapHandle)
{
	/*
		To be able to use this function you need to collect stack trace. Set the following breakpoint at the beginning of your application:
		
		bp ntdll!RtlAllocateHeap "pt \"dx Debugger.State.Scripts.heap.Contents.handleRtlHeapAlloc();g\""
		
		Next you can use it in that way :
		0:000> !heap -x 0x003a9bb0  
		Entry     User      Heap      Segment       Size  PrevSize  Unused    Flags
		-----------------------------------------------------------------------------
		003a9ba8  003a9bb0  00340000  00340000     10028        d8        18  busy extra fill 		
		
		dx Debugger.State.Scripts.heap.Contents.showHeap("00340000")
	*/
	var blackList = ["RtlAllocateHeap","RtlDebugAllocateHeap","RtlpAllocateHeap","malloc","7z!operator","7z_exe!operator","ChildEBP","WARNING"," #"];
	var heap = host.namespace.Debugger.Utility.Control.ExecuteCommand("!heap -p -h " + heapHandle);
	var addr = "";
	for(var chunk of heap)
	{
		try
		{
			addr = chunk.split("   ")[3];
			addr = (parseInt(addr,16)).toString(16);
		}
		catch(exc)
		{
			addr = "";
		}		
		try
		{
			var stack = allocations[addr]["stack"].split("\n");	
			var flag = false;
			var finalFrame;
			for(var frame of stack)
			{
				finalFrame = frame;
				for( var entry of blackList )
				{
					if(frame.includes(entry))
					{
						flag = true;
						break;
					}
				}
				if(!flag)	
					break;
				
				flag = false;
			}
			host.diagnostics.debugLog(chunk + " - " + finalFrame + "\n");			
		}
		catch(exc){
			//print line without changes
			host.diagnostics.debugLog(chunk + "\n");	
		}						
	}
}

function showObjects(heapHandle)
{
	/*
		This function won't work without turning on gflag +ust
		WARNING : 
		line : var callStack = host.namespace.Debugger.Utility.Control.ExecuteCommand("!heap -p -a " + previous);
		cause windbg DoS at least under Win7x86 Windbg 6.1 (7610)
	*/
	var heap = host.namespace.Debugger.Utility.Control.ExecuteCommand("!heap -p -h " + heapHandle);
	var previous = "";
	var previousChunk = "";
	var addr = "";
	for(var chunk of heap)
	{
		try
		{
			try
			{
				addr = chunk.split("   ")[3];
				addr = (parseInt(addr,16)).toString(16);
			}
			catch(exc)
			{
				addr = "";
			}		
			if( chunk.includes("vftable") )
			{
				//object with vftable found. previous point on its address. print stack trace
				host.diagnostics.debugLog(previousChunk);
				host.diagnostics.debugLog(chunk);
				host.diagnostics.debugLog("\n");
				//var callStack = host.namespace.Debugger.Utility.Control.ExecuteCommand("!heap -p -a " + previous);
				//host.diagnostics.debugLog( toString(callStack) );
				showStackTrace(previous)
				host.diagnostics.debugLog("\n===============================================================\n");
				
			}
			previous = addr
			previousChunk = chunk
		}
		catch(exc)
		{
		}			
	}
	
}
