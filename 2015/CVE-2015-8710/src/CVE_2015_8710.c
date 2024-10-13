// @author Mike Dalessio, Francois Chagnon, Florian Weingarten

#include "string.h"
#include <libxml/HTMLparser.h>
#include <libxml/HTMLtree.h>

int main(int argc, char** argv) {
    htmlDocPtr doc;
    int options = HTML_PARSE_RECOVER | HTML_PARSE_NOERROR | HTML_PARSE_NOWARNING | HTML_PARSE_NONET;
    char* HTMLFRAG_BAD  = "<html><body><!--";
    char* HTMLFRAG = HTMLFRAG_BAD;
    xmlInitParser();
    doc = htmlReadMemory(HTMLFRAG, strlen(HTMLFRAG), NULL, "UTF-8", options);
    xmlFreeDoc(doc);
    printf("Done.\n");
}
