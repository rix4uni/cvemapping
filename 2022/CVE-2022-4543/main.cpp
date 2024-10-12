#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;

void execute_cmd(const char *cmd, char *result)
{
    char buf_ps[1024];
    char ps[1024] = {0};
    FILE *ptr;
    strcpy(ps, cmd);
    if ((ptr = popen(ps, "r")) != NULL)
    {
        while (fgets(buf_ps, 1024, ptr) != NULL)
        {
            strcat(result, buf_ps);
            if (strlen(result) > 1024)
                break;
        }
        pclose(ptr);
        ptr = NULL;
    }
    else
    {
        printf("popen %s error\n", ps);
    }
}

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        puts("[*] Usage: ./binary dekaslr_path entry_SYSCALL_64_offset(in hex) max_loop");
        return -1;
    }

    string dekaslr_path = argv[1];
    string koffset = argv[2];
    string max_loop = argv[3];
    string cmd = dekaslr_path + " " + koffset;

    char result[0x1000] = {0};
    int max_tries = stoi(max_loop);

    map<string, unsigned int> base_record;

    for (size_t i = 0; i < max_tries; i++)
    {
        memset(result, 0, 0x100);
        execute_cmd(cmd.c_str(), result);
        // printf("%s\n", result);
        string key = result;
        if (base_record.find(key) != base_record.end())
        {
            base_record[key]++;
        }
        else
        {
            base_record[key] = 1;
        }
    }

    map<string, unsigned int>::iterator iter;
    unsigned int max_cnt = 0;

    for (iter = base_record.begin(); iter != base_record.end(); iter++)
    {
        if (iter->second > max_cnt)
        {
            max_cnt = iter->second;
        }
    }

    string kernel_base;
    for (iter = base_record.begin(); iter != base_record.end(); iter++)
    {
        if (iter->second == max_cnt)
        {
            kernel_base = iter->first;
            cout << "0x" << kernel_base << ": " << max_cnt << "/" << max_tries << endl;
            break;
        }
    }

    return 0;
}
