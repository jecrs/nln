def parse(content):
    
    lmnts = {}
    plmnts = []
    
    parseplmnt = lambda line: Element(line[:line.find(":")],line[line.find(":")+1:]) if line.count(":") > 0 else None
    
    # this class is used to describe the element in the HDoE
    class Element():

        name = "" # the name of the objet
        childs = [] # its childs
        parent = None # its parent
        parlist = [] # this is the path to it location. this is done when the HDoE is builded
        hyearchy_lvl = -1 # the hyearchy level of this element, It's used to build an Hyearchy
        value = "" # the Element value
        
        def __init__(self,name,value):
            
            self.name = name
            self.value = value
            
    # loop that parses the elements
    for l in content.splitlines():
        
        hl = -1
        lmnt = None
        
        if l.startswith("-"):
            
            hl = 0
            
            while l[hl] == "-":
                
                hl += 1
                
            lmnt = parseplmnt(l[hl:])
            for o in plmnts:
                print(lmnt.name,hl,o.hyearchy_lvl,o.name)
                if o.hyearchy_lvl == hl-1:

                    lmnt.hyearchy_lvl = hl
                    lmnt.parent = plmnts.index(o)
                    plmnts[plmnts.index(o)].childs.append(len(plmnts))
                    
            if lmnt.parent == None:
                
                print("no parent")
                plmnts[len(plmnts)-1].hyearchy_lvl = hl
                lmnt.parent = len(plmnts)-1
                
        else:
            
            lmnt = parseplmnt(l)
            lmnt.hyearchy_lvl = 0
                
        plmnts.append(lmnt)
        
    plmntt = []
    
    # loop that build the HDoE
    for l in plmnts:
        
        if l == None:
            
            continue
        
        if l.parent == None:
            
            plmntt.append(l)
            plmnts[plmnts.index(l)].parent = None
            
        else:
            
            if l.parent != -1:
                
                par = []
                lll = plmnts[l.parent]
                
                while lll != None and lll.parent != None:
                    
                    par.append(lll.name)
                    lll = plmnts[lll.parent]
                    
                par.reverse()
                plmnts[plmnts.index(l)].parlist = par
                
        plmntt.append(l)
    
    # build the dict based on the HDoE

    for l in plmntt:
        
            loc = lmnts
            
            for k in l.parlist:
                
                loc = loc[k]
                
            loc[l.name] = {"_val":l.value}

    # since the HDoE isn't organized in a way that i can know if a element have or no childs this loops fix this
    # Example of what the loop does: "Hello":{"_val":"World"} -> "Hello":"World"

    for l in plmntt:
        
            loc = lmnts
            
            for k in l.parlist:
                
                loc = loc[k]
            if type(loc[l.name]) == dict:
                
                if len(list(loc[l.name].keys())) == 1:

                    loc[l.name] = loc[l.name]["_val"]
                    
            
    return lmnts