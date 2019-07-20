import traceback


def home():
    """ Sets up home page """

    page = """
    <h1> Web Calculator </h1>
    <p>In order to use this website effectively, use the url to
    specify operation type (add, subtract, multiply, divide) and the numbers
    for the operation. Example: http://localhost:8080/add/2/3
    """

    return page


def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """

    try:
        one, two = args
        mult = int(one) * int(two)
        page = f"""
            <h1>Multiplication Page</h1>
            <h2>{mult}</h2>
            """
        return page

    except ValueError:
        print("value error")


def divide(*args):
    """ Returns a STRING with the division of the arguments """

    try:
        one, two = args
        divide = int(one) / int(two)
        page = f"""
            <h1>Division Page</h1>
            <h2>{divide}</h2>
            """
        return page

    except ValueError:
        print("value error")


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    try:
        one, two = args
        difference = int(one) - int(two)
        page = f"""
            <h1>Subtraction Page</h1>
            <h2>{difference}</h2>
            """
        return page

    except ValueError:
        print("value error")


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = 0
    try:
        for item in args:
            print(item)
            sum += int(item)
    except ValueError:
        print("value error")
    finally:
        page = f"""
        <h1>Addition Page</h1>
        <h2>{sum}</h2>
        """
        return page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    funcs = {
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply,
        '': home,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    numbers = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, numbers


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        print(path)
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Not Found"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        print(f"This is the body:{body}")
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8080, application)
    server.serve_forever()
