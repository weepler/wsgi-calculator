"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    sum = str(args[0] + args[1])
    return sum


def subtract(*args):
    """ Returns a STRING with the differenceof the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    difference = str(args[0] - args[1])
    return difference


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    quotient = str(args[0] / args[1])
    return quotient


def multiply(*args):
    """ Returns a STRING with the multiplier  of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    multiplier = str(args[0] * args[1])
    return multiplier


def readme(*args):

    return '''<h1>WSGI Calculator</h1>

    <p>Use the webpages address to add, subtract, multiply, and divide functions in the format below:</p>
    <ul>

    <li><a href="http://localhost:8080/multiply/3/5" rel="nofollow">http://localhost:8080/multiply/3/5 </a> =&gt; 15</li>
    <li><a href="http://localhost:8080/add/23/42" rel="nofollow">http://localhost:8080/add/23/42 </a> =&gt; 65</li>
    <li><a href="http://localhost:8080/subtract/23/42" rel="nofollow">http://localhost:8080/subtract/23/42 </a> =&gt; -19</li>
    <li><a href="http://localhost:8080/divide/22/11" rel="nofollow">http://localhost:8080/divide/22/11 </a> =&gt; 2</li>
    
    </ul>'''

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    # Given that path is something like: 
    # 'add/3/3'
    # 'divide/10/5/'
    # '/multiply/8/6/'



    path = path.strip('/').split('/')   #  now ive got something like                                     #  ["add", "3","4"]
    func_name = path.pop(0)  # "add" and ["3", "4"]
    args = [int(arg) for arg in path]  # args is now ["3","4"]
    funcs = {'': readme,
            'add': add,
            'subtract': subtract,
            'multiply': multiply,
            'divide': divide,
            }
    func = funcs[func_name]
    # try:
    #     func = funcs[func_name]
    # except KeyError:
    #     raise NameError 

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']

    return func, args

    # has to recieve the environ and then receive the start
    # response function. it takes these requests and then 
    # figures out what response. 
def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None) #requested path 
        if path is None:
            raise NameError
        func, args = resolve_path(path) # returns a func and args for 
        body = func(*args)              # the function
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]  # returns the body as bites

    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.


# WSGI is split between a server and an application the server
# is the part of the request that breaks it down and figures out 
# what those requests are. we are using a built in server. 

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

