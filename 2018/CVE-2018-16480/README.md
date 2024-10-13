# public.js

  Run static file hosting server with specified public dir & port.
  Support a "direcotry index" like Apache httpd.

## Apologies for module name

  The name of this module is "public", but it is not recommended to use for "public". It is for development server on the local computer. **Do not use on the public network!**

## Usage

    # install
    npm install -g public

    # start server 
    public
    Public.js server running with "/path/to/./" on port 3000

    # start server with option
    public test 3030
    Public.js server running with "/path/to/test" on port 3030

