from typing import Any, Callable

def custom_fence(fence: str = "+"):

    def add_fence(func):

        def wrapper(text: str):
            print(fence * len(text))
            func(text)      
            print(fence * len(text))
        return wrapper
    return add_fence

@custom_fence("*")
def log(text: str):
    print(text)


log('df')   

###############

def decorator(func: Callable[[Any], None]):
    pass

##############


routes: dict[str, Callable[..., Any]] = {}

def route(path: str):
    def register_route(func):
        routes[path] = func
        return func
    return register_route

@route("/shipment")
def get_shipment():
    return "Shipment details: Wooden table, In transit"

request: str = ""

while request != "exit":
    request = input("Enter route: ")

    if request in routes:
        response = routes[request]()
        print(response, end="\n\n")
    else:
        print("Route not found")