/*
	Monitors directory changes
	(c) 2006-2007 Vladimir Dubrovin, 3APA3A
	http://securityvulns.com/
	http://securityvulns.ru/
*/

#include <windows.h>
#include <stdio.h>
#include <io.h>
#include <fcntl.h>
#include <string.h>


char buf[4096];

int main(int argc, char *argv[]){
    HANDLE hDir;

	FILE_NOTIFY_INFORMATION * fn;
	int read;
	WCHAR * action = NULL;

	if(argc != 2) {
		printf(
"Usage: %s <directory_path>\n"
" Monitor directory changes with all subdirectories\n"
" For any files, including ones you have no access\n"
" (as on January, 2007)\n"
"(c) Vladimir Dubrovin, 3APA3A\n"
" http://securityvulns.com\n"
" http://securityvulns.ru\n"
"This approach is not reliable and should not be used for audit and another critical operations.\n",
 argv[0]);
		return 1;
	}

	CreateDirectory(argv[1], 0);
	hDir = CreateFile(
	  argv[1],
	  FILE_LIST_DIRECTORY,
	  FILE_SHARE_READ|FILE_SHARE_DELETE,
	  NULL,
	  OPEN_EXISTING,
	  FILE_FLAG_BACKUP_SEMANTICS,
	  NULL
	);
	if(hDir == INVALID_HANDLE_VALUE){
		fprintf(stdout, "Failed to open dir\n");
		return 2;
	}
	for(;;){
	    if(!ReadDirectoryChangesW(
		hDir,
		buf,
		sizeof(buf) - sizeof(WCHAR),
		1,
		FILE_NOTIFY_CHANGE_DIR_NAME | FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_LAST_ACCESS |
			FILE_NOTIFY_CHANGE_ATTRIBUTES | FILE_NOTIFY_CHANGE_SIZE	| FILE_NOTIFY_CHANGE_LAST_WRITE	|
			FILE_NOTIFY_CHANGE_CREATION	 | FILE_NOTIFY_CHANGE_SECURITY
		,
		(DWORD *)&read,
		NULL,
		NULL
		)) {
			fprintf(stderr, "Failed to read directory changes\n");
			break;
		}
		_setmode(_fileno(stdout), _O_U16TEXT);
		for (fn = (FILE_NOTIFY_INFORMATION *)buf; ;fn = (FILE_NOTIFY_INFORMATION *)(((char *)fn) + fn->NextEntryOffset)){
			WCHAR t;
			switch(fn->Action){
			case FILE_ACTION_ADDED:
				action = L"added";
				break;
			case FILE_ACTION_REMOVED:
				action = L"removed";
				break;
			case FILE_ACTION_MODIFIED:
				action = L"modified";
				break;
			case FILE_ACTION_RENAMED_OLD_NAME:
				action = L"renamed (old name)";
				break;
			case FILE_ACTION_RENAMED_NEW_NAME:
				action = L"renamed (new name)";
				break;
			default:
				action = L"(unknown)";
			}
		    t = fn->FileName[fn->FileNameLength/sizeof(WCHAR)];
		    fn->FileName[fn->FileNameLength/sizeof(WCHAR)] = 0;
		    wprintf(L"File %s: %s\n", action, fn->FileName);
		    fn->FileName[fn->FileNameLength/sizeof(WCHAR)] = t;
		    if(!fn->NextEntryOffset) break;
		}
	}
	return 0;
	
}
