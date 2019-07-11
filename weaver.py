import htmlform as f
from makespecial import makeSpecial

# Base html element to start weaver 


class Weaver:
    def __init__(self):
        self.__set_specials()
    def __set_specials(self):
        ignore = [
            'name', 'doc', 'package', 'loader', 'spec', 
            'file', 'cached', 'builtins', 'label', 'Input'
            ]
        for k,v in f.__dict__.items():
            if k in ignore:
                continue
            setattr(self, k, makeSpecial(self, v))

def test():
    w = Weaver()
    root = w.form('root')

    root.add_item(f.button("test", value=''))

    print(w.idstr['root']())
test()