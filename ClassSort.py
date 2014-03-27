

class MyClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b

def compare(a, b):

    if a.b > b.b:
        return 1
    else:
        return -1
    

if __name__ == "__main__":

    classList = []
    classList.append(MyClass("5", "b"))
    classList.append(MyClass("3", "7"))
    classList.append(MyClass("1", "a"))
    
    classList.sort(compare)

    for cl in classList:
        print cl.a, " ", cl.b

    
