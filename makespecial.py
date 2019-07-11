def makeSpecial(trackIn, cType):
    """
        returns a function which takes the form of a object intializer 
        and stores a pointer to the new object method 'html' within 
        a key-value pair store (trackIn.idstr {'id', cType.html method} ) 
        
        trackIn:
            an intialized object which will store the new intialzed {id: html} 
            method pointer information.
        cType:
            class type of new object which will be initialized.
            class should already contain a method named 'html' 
        Usage:
            class c(object):
                def __init__(self, name, id, **kw):
                    self.name = name
                    self.id = id
                    self.kw = kw
                def html(self):
                    print (self.name)
                    
            bIns = b() # bIns is an intialized object to store new objects info \
            bIns.spec = makeSpecial(bIns, c)
            
            newObj = bIns.spec('name1', 'id1', test=1)
            IN:
                bIns.__dict__
            Out[14]: 
                {'items': [],
                 'idstr': {'id1': <bound method c.html of <__main__.c object at 0x000001E8432F4438>>}}
    """
    def aSpecialFunc(trackIn, cType, *args,**kw):
        def track(self,obj):
            """
                used to add key,value pair of {id: html-func} for reference
            """
            if not 'idstr' in obj.__dict__:
                obj.idstr = {}
            obj.idstr[self.id] = self.html
            return self
        cObj = cType(*args, **kw)
        cObj.track = track
        return cObj.track(cObj, trackIn)
    return lambda *args,**kw: aSpecialFunc(trackIn,cType,*args,**kw)

def makeAction(trackIn, mapName, cType, funcName):
    """
        maps the mapName to action within trackIn object
        Example input:
            class a:
                def __init__(self):
                    self.base = {'data':{'a':[1,2,3,4],
                                         'b':[1,2,3,4],
                                         'c':[1,2,3,4],
                                         'd':[1,2,3,4]}}
                def rem_data(self, inkey, *args,**kw):
                    key = kw['inkey'] if 'inkey' in kw else inkey
                    if key in self.base['data']:
                        del self.base['data'][key]
            class b:
                def __init__(self, name, **kw):
                    self.name = name
                    self.id = name + '_id'
                    self.kw = kw
                    self.items = []
                    
            aIns = a()
            aIns.crazy = makeAction(aIns, # Object to store map within
                                    'id', # maps aIns.id to input functions
                                    b, # class type object which is created by aIns.crazy return function.
                                    'crazy' # name of function 
                                    )
            # creates a b type class object which reqires the same arguments to intialize b \
              plus the 'funcName' def funcName={'f': funcToCal, 'args': ['list','of', 'args'], 'kw': {'key': 'word', 'a': 'rgs'}}               
            aBClassObj = aIns.crazy('bObjName', crazy={'f': rem_data, 'args':['a']}) 
            
            # aIns.idstr will contain this entry { aBClassObj.id: aIns.rem_data('a')} \ 
            which can be called to perform the function if required
            
            
            
        pre-defined funcName's:
            delete:
                return object has a .delete() function.
            test:
                return object has a .test() function.
            add:
                return object has a .add() function.
            modify:
                return object has a .add() function.
        Undefined names:
            return object has a .special[funcName]() function.
    """
    def aSpecialFunc(trackIn, cType, funcName, *args,**kw):
        def add_func(funcName, cObj):               
            if funcName in cObj.kw:
                argF = False
                if 'kw' in cObj.kw[funcName]:
                    for kwa in cObj.kw[funcName]['kw']:
                        if type(cObj.kw[funcName]['kw'][kwa]) == dict:
                            if 'f' in cObj.kw[funcName]['kw'][kwa]:
                                print ("function in keywords: %s"%(cObj.kw[funcName]['kw'][kwa]['f']))
                                def argfunc():
                                    print ("argfunc called")
                                    return cObj.kw[funcName]['kw'][kwa]['f'](*cObj.kw[funcName]['kw'][kwa]['args'] if 'args' in cObj.kw[funcName]['kw'][kwa] else [], **cObj.kw[funcName]['kw'][kwa]['kw'] if 'kw' in cObj.kw[funcName]['kw'][kwa] else {})
                                cObj.kw[funcName]['kw'][kwa]['a'] = argfunc
                                argF=True
                if argF == True:
                    def preArgs():
                        newKwargs = {}
                        kwArgs =  cObj.kw[funcName]['kw']
                        print ("kwArgs before collected: %s"%(kwArgs))
                        """
                        {'inline': {'a': <function argfunc at 0x7ff00478a9b0>, 
                                    'kw': {'key': 'Data__Time__inLine'}, 
                                    'f': <bound method FileToParse.getWebInput of <configmgr2.FileToParse instance at 0x7ff004809638>>}}
                        """
                        for kwa in kwArgs:
                            if type(kwArgs[kwa]) is dict and 'a' in kwArgs[kwa].keys():
                                if callable(kwArgs[kwa]['a']):
                                    newKwargs[kwa] = kwArgs[kwa]['a']()
                            else:
                                newKwargs[kwa] = kwArgs[kwa]
                        print ("newKwargs after collected: %s"%(newKwargs))
                        return newKwargs
                    def func():
                        newKwargs = preArgs
                        function = cObj.kw[funcName]['f']
                        function(**newKwargs())
                else:
                    def func():
                        
                        print ("No kwArgs need to be collected:")
                        cObj.kw[funcName]['f'](*cObj.kw[funcName]['args'] if 'args' in cObj.kw[funcName] else [],
                               **cObj.kw[funcName]['kw'] if 'kw' in cObj.kw[funcName] else {})
            if funcName == 'delete':
                cObj.delete = func
            elif funcName == 'add':
                cObj.add = func
            elif funcName == 'modify':
                cObj.modify = func
            else:
                cObj.special = {funcName: func}
            
        def track(self,obj):
            """
                used to add key,value pair of {id: html-func} for reference
            """
            mapValue = self.__dict__[mapName] if mapName in self.__dict__ else funcName
            if not 'idstr' in obj.__dict__:
                obj.idstr = {}
            if funcName == 'delete':
                obj.idstr[mapValue] = self.delete
            elif funcName == 'add':
                obj.idstr[mapValue] = self.add
            elif funcName == 'modify':
                obj.idstr[mapValue] = self.modify
            else: 
                try:
                    if callable(getattr(self, funcName)):
                        obj.idstr[mapValue] = getattr(self, funcName)
                except:
                    obj.idstr[mapValue] = self.special[funcName]
            return self
        cObj = cType(*args, **kw)
        try:
            if callable(getattr(cObj, funcName)): # Checking if created object has method already
                pass
        except:
            add_func(funcName, cObj)
        cObj.track = track
        return cObj.track(cObj, trackIn)
    return lambda *args,**kw: aSpecialFunc(trackIn,cType,funcName,*args,**kw)

"""
#tests


class a:
    def __init__(self):
        self.base = {'data':{'a':[1,2,3,4],
                             'b':[1,2,3,4],
                             'c':[1,2,3,4],
                             'd':[1,2,3,4]}}
    def rem_data(self, inkey, *args,**kw):
        key = kw['inkey'] if 'inkey' in kw else inkey
        if key in self.base['data']:
            del self.base['data'][key]
        
class b:
    def __init__(self, name, **kw):
        self.name = name
        self.id = name+'_id'
        self.kw = kw
        self.items = []
    def html(self):
        print ("I am HTML from b class")

aIns = a()
aIns.crazy = makeAction(aIns, 'id', b, 'html')
bt = aIns.crazy('test')
"""