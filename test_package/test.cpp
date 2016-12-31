#include "curl_easy.h"
#include "curl_exception.h"

using curl::curl_easy;
using curl::curl_easy_exception;
using curl::curlcpp_traceback;

int main(int argc, const char **argv)
{
    curl_easy easy;

    // Add some option to the curl_easy object.
    easy.add<CURLOPT_URL>("http://www.google.com");
    easy.add<CURLOPT_FOLLOWLOCATION>(1L);

    try
    {
        // Execute the request.
        easy.perform();
    }
    catch (curl_easy_exception error)
    {
        // If you want to get the entire error stack we can do:
        curlcpp_traceback errors = error.get_traceback();

        // Otherwise we could print the stack like this:
        error.print_traceback();

        // Note that the printing the stack will erase it
    }

    return 0;
}

