"""
    htmlforms
"""

class label:
    """
        name: String visible & describing form.
        label_of: target id which this is labeled of.         
    
        used by forms to describe form input,
        label_of - id this label describes
        
        default: class="control-label col-sm-2", can be modified by input kwargs
        
        **kwargs: 
            class: control-label, 
            size: lg,md,sm
            blk: value out of 12
    """
    def __init__(self, name, targetForm, kw):
        print (kw)
        self.bsClass = self.__getClass(kw)
        self.Id = name if not 'id' in kw else kw['id']
        self.dispname = name
        self.inline = False if not 'inline' in kw else kw['inline']
        self.targetForm = targetForm['p']
        self.childElements = targetForm['c']
        
    def __getClass(self,inKws):
        defClass = 'class="control-label col-sm-2"'
        defClass = 'class="%s"'%(inKws['class']) if 'class' in inKws else defClass
        if "size" in inKws:
            defClass = ' '.join([defClass.split(' ')[1], 'col-%s-%s'%(inKws['size'], inKws['blk'] if 'blk' in inKws else str(2))])
        if "blk" in inKws:
            if not "size" in inKws:
                defClass = 'class="control-label col-sm-%s"'%(inKws['blk'])
        return defClass
    def parentAndChild(self, toAppend):
        toAppend.append(self.targetForm)
        if len(self.childElements) > 0:
            for child in self.childElements:
                toAppend.append(child)
        return toAppend
    def wrapped_html(self, isHidden):
        if isHidden is not True:
            """
            if self.inline is False:
                return ['<label {lblcls} for="{htmlId}">'.format(lblcls=self.bsClass, htmlId=self.Id), 
                        '{form}'.format(form=self.targetForm),
                        '{name}</label>'.format(name=self.dispname)]
            """
            if self.inline is False:
                return self.parentAndChild(['<label {lblcls} for="{htmlId}">'.format(lblcls=self.bsClass, htmlId=self.Id) + 
                        '{name}</label>'.format(name=self.dispname)])
            else:
                print ("label is InLine")
                toReturn = '<label {lblcls} for="{htmlId}">'.format(lblcls=self.bsClass, htmlId=self.Id)
                parAndChild = self.parentAndChild([])
                for pc in parAndChild:
                    toReturn = toReturn + pc
                toReturn = toReturn + '{name}</label>'.format(name=self.dispname)
                return [toReturn]
        else:
            return self.parentAndChild([])

class Input:        
    def __processKw(self,otherProp=None):
        lookFor = ['label', 'class', 'id', 'value', 'disabled', 'name', 'type']
        if otherProp is not None:
            for item in otherProp:
                lookFor.append(item)
        hasValues = []
        for prop in lookFor:
            if prop in self.kw:
                hasValues.append(prop)
        if not 'id' in hasValues:
            #hasValues.append('id')
            #self.kw['id'] = self.dispname
            self.label['id'] = self.dispname
        return hasValues
    def getProperties(self):
        propToRet = ''
        customLabel = False
        for prop in self.__processKw(self.formSpecial):
            if prop == 'label':
                customLabel = True
            else:
                #print("getProperties prop:------------%s"%(prop))
                if str(prop) == "onclick":
                    pass
                    #propToRet = propToRet + '%s=%s '%(prop, self.kw[prop])
                else:
                    propToRet = propToRet + '%s="%s" '%(prop, self.kw[prop])
        return propToRet, customLabel
        
    def labelWrap(self, hasCustomLabel, inputText):
        lbl = self.kw['label'] if hasCustomLabel is True else self.label
        return label(self.dispname if not 'name' in lbl else lbl['name'],
                     {'p': inputText, 'c': self.elementChildren},
                     lbl).wrapped_html(self.hideLabel)
    def reInit(self, dispname, kw):
        kw = self.preInit(dispname, kw)
        self.setInitVars(dispname, kw, self.defaultLabel, self.formSpecific)
    def setInitVars(self, name, kw, label, frmSpec):
        """
            name - sets form name - type str
            kw - kw var inputs to parent form - type {}
            label - type {'default': True, 'class': 'form-check-label'}
            frmSpec - list input [] can be used by form init to set value
        """
        self.dispname = name
        self.customType = None
        self.value = kw['value'] if 'value' in kw else None
        self.kw = kw
        self.label = label
        self.hideLabel = False if not 'lblhidden' in kw else kw['lblhidden']
        self.formSpecial = frmSpec
        self.elementType = 'input' # default type for input objects, other possible is 'select'
        self.elementChildren = [] # elements within input object, to be added when labelWrap() is called.
        
    def html(self):
        toReturn = ['<div class="%s">'%(self.cName)]
        properties, hasCustomLabel = self.getProperties()
        cNameV = self.cName if not self.cName == 'button' else 'submit'
        if self.customType is not None:
            cNameV = self.customType
        inputText = '<{eleType} type="{cName}"{value}{onclick}{prop}{name}>'.format(
            eleType=self.elementType, 
            cName=cNameV,
            prop=properties,
            value=' value="%s"'%(self.dispname) if not 'value' in self.kw else '',
            name=' name="%s"'%(self.name) if 'name' in self.__dict__ else '',
            onclick=' onclick=SendForm("%s","%s","%s") '%(
                self.kw['onclick']['id'], 
                self.kw['onclick']['self'], 
                self.kw['onclick']['tar']) if 'onclick' in self.kw else '')
        for retItems in self.labelWrap(hasCustomLabel, inputText):
            toReturn.append(retItems)
        if not self.elementType == 'input':
            toReturn.append('</%s>'%(self.elementType))
        toReturn.append('</div>')
        return toReturn
    def inputText(self):
        properties, hasCustomLabel = self.getProperties()
        addOptions = ''
        if 'options' in self.kw:
            for opt in self.kw['options']:
                addOptions = addOptions + ' %s'%(opt)
        inputText = '<%s type="%s" %s %s>'%(self.elementType, self.elementType,properties, addOptions)
        return inputText
        
class checkbox(Input):
    def __init__(self, dispname, **kw):
        """
            see .setInitVars description
        """
        self.cName = 'checkbox'
        self.setInitVars(dispname, kw, {'default': True, 'class': 'form-check-label'}, ["checked", 'oncheck'])
class textbox(Input):
    """
        use type="password" for *** input,
            "email" for email input
        lblhidden=True:
            show/hide label discription for text box
    """
    def __init__(self, dispname, tbType, **kw):
        self.cName = 'text'
        
        self.setInitVars(dispname, kw, {'default': True, 'class': 'form-check-label'}, 
                        ["type", # Type = Password for *** input
                        "email"])
        self.customType = tbType
class radio(Input):
    def __init__(self, dispname, **kw):
        self.cName = 'radio'
        self.setInitVars(dispname, kw, {'default': True, 'class': 'form-check-label'}, ["checked"])
class text:
    def __init__(self, text):
        try:
            self.text = text if type(text) in [str, type(u'')] else str(text)
        except:
            assert True, "class text: input %s cannot be converted to string format"%(text)
    def html(self):
        return [self.text]
        

class button(Input):
    """
        style:
            https://getbootstrap.com/docs/4.0/components/buttons/ for color styles
            color - default btn btn-primary. Other options: secondary, success, danger, warning, info, light
        size: 
            options: lg,md,sm,xs, block(spans entire block)
        action:
            Use: action={'action': '<showHide|submit>', 
                         'id': <'idOfFormToSubmit|None'>,
                         'target': <'id of element to change'>
                         }
        label - 
            default: hidden use lblhidden = False to show
        Example:
            aButton= button("b1", value="b1")
            aButton.setActionOnClick('showHide', None,'b1-div')
            print ('\n'.join(aButton.html()))
            Output:
            <div class="button">
                <input type="button" class="btn active" value="b1" onclick="showHideCh(b1-div)" id="b1"  >
            </div>
    """
    def __init__(self, dispname, **kw):
        self.cName = 'button'
        self.defaultLabel = {'default': True, 'class': 'form-check-label'}
        self.formSpecific = ['onclick', 'data-toggle', 'data-target'] # 'data-toggle', 'data-target' are used for bootstrap collapse functions
        newkw = self.preInit(dispname, kw)
        self.setInitVars(dispname, newkw, self.defaultLabel, self.formSpecific)
        self.name = dispname if not 'name' in newkw else newkw['name']
        local = self.setActionOnClick(newkw['action']['action'], newkw['action']['id'], newkw['action']['target']) if 'action' in kw else ''
    def preInit(self, dispname, kw):
        self.disp = dispname
        self.special = kw['special'] if 'special' in kw else None
        addBtnCls = kw
        addBtnCls['class'] = 'btn btn-'+ kw['style'] if 'style' in kw else 'btn'
        addBtnCls['class'] = addBtnCls['class'] +' btn-' + kw['size'] if 'size' in kw else addBtnCls['class']
        if self.special is None:
            addBtnCls['class'] = addBtnCls['class'] + ' active' if not 'disabled' in kw else addBtnCls['class'] + ' disabled'
        else:
            addBtnCls['class'] = addBtnCls['class'] + ' %s'%(self.special)
        #Default buttons should appear without label
        addBtnCls['lblhidden'] = True
        return addBtnCls
    def setActionOnClick(self, action, id_of_FormToSubmit, target):
        """
            action: 
                - "submit" (send form data for id) 
                - "showHide" (collapse / show target id)
        """
        if str(action) == 'submit':
            #self.kw['onclick'] = 'SendForm("%s", "%s", "%s")'%(id_of_FormToSubmit, self.disp, target)
            self.kw['onclick'] = {'id': id_of_FormToSubmit, 'self': self.name, 'tar': target}
        elif str(action) == 'showHide':
            self.kw['data-toggle'] = "collapse"
            self.kw['data-target'] = "#%s"%(target)
        else:
            pass
class select(Input):
    """
        style:
            https://getbootstrap.com/docs/4.0/components/input-group/#custom-select
            default: form-control, Other options: "custom-select"
        Use: 
            options=[<optionList>] for drop down selections.
            lblhidden = True|False (default False) to show / hide label
        Example:
            select("select 1", name="b1", options=['1','2','3','4'], label={'blk': 2})
            print ('\n'.join(select("select 1", name="b1", options=['1','2','3','4'], label={'blk': 2}).html()))
            Output:
                <div class="select">
                    <label class="control-label col-sm-2" for="select 1">select 1</label>
                    <select type="select" class="form-control" name="b1" id="select 1"  >
                        <option>1</option>
                        <option>2</option>
                        <option>3</option>
                        <option>4</option>
                    </select>
                </div>
    """
    def __init__(self, dispname, **kw):
        self.cName = 'select'
        
        addSelCls = kw
        addSelCls['class'] = "form-control" if not 'cstm_cls' in kw else kw['cstm_cls']
        
        self.setInitVars(dispname, kw, {'default': True}, None)
        self.elementType = 'select'
        if 'options' in kw:
            for opt in kw['options']:
                self.elementChildren.append('<option selected="selected">%s</option>'%(opt) if opt == str(self.value) else '<option>%s</option>'%(opt))
                      

class htmlelement(object):
    def initParamItems(self, kw):
        self.options = '' if not 'options' in kw else kw['options']
        self.action = kw['action'] if 'action' in kw else None
        self.sesid= kw['sesid'] if 'sesid' in kw else None
        self.items = kw['items'] if 'items' in kw else []
    def getChildHtml(self, toReturn):
        localRet = toReturn
        for item in self.items:
            try:
                itemIns = item.html()
            except AttributeError:
                print(item)
                print('is not the correct type htmlelement')
            if itemIns is not None:
                for itemInsItem in itemIns:
                    assert (type(itemInsItem) not in [dict, list]), "item is a list or dict: %s"%(itemInsItem)
                    localRet.append(itemInsItem)
        return localRet
    def printOp(self):
        retOps = ''
        for op in self.options:
            retOps = retOps + ' %s'%(op)
        return retOps
    def add_item(self, item):
        self.items.append(item)
    def add_items(self, items):
        assert type(items) == list
        for item in items:
            self.add_item(item)


        
class td(htmlelement):
    def __init__(self, **kw):
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<td>'])
        toReturn.append('</td>')
        return toReturn
        
class tr(object):
    """
        Table Row
        optional kw args:
            color: primary, success, info, warning, danger, active, secondary, light and dark
                    https://www.w3schools.com/bootstrap4/tryit.asp?filename=trybs_table_contextual&stacked=h
    """
    def __init__(self, rowItems, **kw):
        self.color = kw['color'] if 'color' in kw else None
        self.cols = []
        for col in rowItems:
            self.cols.append(td(items=[col]))
    def getChildHtml(self, toReturn):
        locRet = toReturn
        for col in self.cols:
            colIns = col.html()
            if colIns is not None:
                for colInsItem in colIns:
                    locRet.append(colInsItem)
        return locRet
    def html(self):
        toReturn = self.getChildHtml(['<tr{color}>'.format(color=' table-%s'%(self.color) if self.color is not None else '')])
        toReturn.append('</tr>')
        return toReturn
        
        
class table(object):
    """
        headRow: 
            type(list) input which should contain html elements with .html() method
        optional kw args:
            - border: default True, Use border=False to make borderless
            - size: default sm, Use size=[md|lg] to adjust
            - hover: default False, Use hover=True to add hover effect
            - color: default primary use color = [ success, info, warning, danger, active, secondary, light or dark ]
                    https://www.w3schools.com/bootstrap4/tryit.asp?filename=trybs_table_contextual&stacked=h
    """
    def __init__(self, headRow,**kw):
        self.headRow = headRow
        self.rows = self.__getInitRows(kw['rows']) if 'rows' in kw else []
        self.id = kw['id'] if 'id' in kw else ''
        self.hover = kw['hover'] if 'hover' in kw else False
        self.color = kw['color'] if 'color' in kw else ''
        self.size = kw['size'] if 'size' in kw else 'sm'
        self.border = kw['border'] if 'border' in kw else True
    def __getInitRows(self, rows):
        rList = []
        for row in rows:
            if type(row) is tr:
                rList.append(row)
            else:
                rList.append(tr(row))
        return rList
    def getChildHtml(self, toReturn):
        localReturn = toReturn
        for th in self.headRow:
            localReturn.append('<th>')
            for thItems in th.html():
                localReturn.append(thItems)
            localReturn.append('</th>')
        for row in self.rows:
            rowIns = row.html()
            if not rowIns is None:
                for rowInsItem in rowIns:
                    localReturn.append(rowInsItem)
        return localReturn
    def add_row(self, row):
        """
            optional kw args:
                color: primary, success, info, warning, danger, active, secondary, light and dark
                        https://www.w3schools.com/bootstrap4/tryit.asp?filename=trybs_table_contextual&stacked=h
        """
        if type(row) is tr:
            self.rows.append(row)
        else:
            self.rows.append(tr(row))
    def html(self):
        toReturn = ['<table class="table{hover}{color}{border}{size}{tid}">'.format(hover=' table-hover' if self.hover is True else '',
                                                                                   color=' table-%s'%(self.color) if self.color is not '' else '',
                                                                                   border=' table-borderless'if self.border is False else '',
                                                                                   size=' table-%s'%(self.size),
                                                                                   tid=' %s'%('id="%s"'%(self.id) if self.id is not '' else ''))]
        withChild = self.getChildHtml(toReturn)
        withChild.append('</table>')
        return withChild
        
        
class dropdown(htmlelement):
    def __init__(self, dispname, id, **kw):
        self.dispname = dispname
        self.id = id
        self.displayBtn = button(dispname, style="secondary dropdown-toggle", id=self.id, options=['data-toggle="dropdown"', 'aria-haspopup="true"', 'aria-expanded="false"'])
        self.displayBtn.elementType = "button"
        self.initParamItems(kw)
    def html(self):
        toReturn = ['<div class="dropdown">',
                    self.displayBtn.inputText(), 
                    self.dispname, 
                    '</button>', 
                    '<div class="dropdown-menu" aria-labelledby="%s">'%(self.id)]
        for item in self.items:
            if type(item) == button:
                item.special = 'dropdown-item'
                item.reInit(item.disp, item.kw)
            itemIns = item.html()
            for Insitem in itemIns:
                toReturn.append(Insitem)
        toReturn.append('</div>')
        toReturn.append('</div>')
        return toReturn

class a(htmlelement):
    """
    Usage:
        a('Getting Started', href='#GetStarted', options=['nav-link'])
        a('Company Name', href='index.html', options=['navbar-brand'])
    """
    def __init__(self, text, **kw):
        
        self.text = text
        self.href = kw['href'] if 'href' in kw else None
        self.custom = kw['custom'] if 'custom' in kw else ''
        self.initParamItems(kw)
    def html(self):
        if len(self.items) > 0:
            toReturn = self.getChildHtml(['<a class="{options}" href={href} {custom}>'.format(
                options=self.printOp(),
                href=self.href,
                custom=self.custom)])
            toReturn.append('<span>%s</span>'%(self.text))
            toReturn.append('</a>')
        else:
            return ['<a class="{options}" href={href} {custom}>{text}</a>'.format(
                options=self.printOp(),
                href=self.href,
                text=self.text,
                custom=self.custom)]
        return toReturn
class li(htmlelement):
    def __init__(self, **kw):
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<li class="{options}">'.format(options=self.printOp())])
        toReturn.append('</li>')
        return toReturn

class ul(htmlelement):
    def __init__(self, **kw):
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<ul class="{options}">'.format(options=self.printOp())])
        toReturn.append('</ul>')
        return toReturn

class col(htmlelement):
    """
        colums(vertical) which contain html elements such as inputs(select, check_box, text_box, button, radio)
        id:  
            unique id for column element
        blk: 
            value out of 12 for which row will be filled with column element at a given screen size.
        offset: 
            number of blank block space which will proceed this element in row. 
        align:
            vertical alignment in column opts: start, center, end
        collapse:
            default False, set to True to allow for buttons to target col ID to hide
        options:
            as an argument for addtional class options. Example column('id1', None, blk=2, options="form-group")
        Example:
            In:
                aCol = col(items=[button("A", value="A", id="col-id-A")])
                print ('\n'.join(aCol.html()))
            Out:
                <div class="col-md-2 " >
                    <div class="button">
                        <input type="submit" class="btn active" id="col-id-A" value="A"  >
                    </div>
                </div>
    """
    def __init__(self, **kw):
        self.id = kw['id'] if 'id' in kw else ''
        self.size = 'md' # Default size is medium
        self.collapse = 'collapse show' if 'collapse' in kw else ''
        self.blk = '2' if 'blk' not in kw else kw['blk'] # Default blk cnt is 2
        self.offset = kw['offset'] if 'offset' in kw else ''
        self.align = kw['align'] if 'align' in kw else 'center'
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<div class="col-{}-{} {options}{offset}{align}{colapse}"{action}{id}{sesid}>'.format(self.size, self.blk, 
                                                              options=self.printOp(),
                                                              colapse='%s'%(' %s'%(self.collapse) if self.collapse is not '' else ''),
                                                              offset=' offset-%s-%s'%(self.size,self.offset) if self.offset is not '' else '', 
                                                              align=' align-self-%s'%(self.align),
                                                              action=' action="%s"'%(self.action) if self.action is not None else '',
                                                              sesid=' sesid="%s"'%(self.sesid) if self.sesid is not None else '',
                                                              id=' %s'%('id="%s"'%(self.id) if self.id is not '' else ''))])
        toReturn.append('</div>')
        return toReturn

class row(htmlelement):
    """
        row element which columns will be placed.
        common options:
            hor_align: 
                start, center, end - How columns in row will be aligned(horizontally) in given row.
            ver_align: 
                start, center, end - How columns in row will be aligned(vertically) in given row.
                
           Output Html: 
            <div class="row justify-content-start " >
               <div class="button">
                <input type="submit" class="btn active" value="a" id="a"  >
               </div>
            </div>
    """
    def __init__(self, **kw):
        self.id = kw['id'] if 'id' in kw else ''
        self.hor_align= kw['hor_align'] if 'hor_align' in kw else None
        self.ver_align= kw['ver_align'] if 'ver_align' in kw else None
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<div class="row{hor_align}{ver_align}{options}" {action}{sesid}>'.format(hor_align=' justify-content-%s'%(self.hor_align) if self.hor_align is not None else '',
                                                                                                 ver_align=' align-items-%s'%(self.ver_align) if self.ver_align is not None else '',
                                                                                                 action=' action="%s"'%(self.action) if self.action is not None else '',
                                                                                                 sesid=' sesid="%s"'%(self.sesid) if self.sesid is not None else '',
                                                                                                  options=' %s'%(self.printOp()))])
        toReturn.append('</div>')
        return toReturn

class rowOfCol(row,col):
    """
        a row element, with columns with equal blk cols
        input listOfCols is type(list), with each item in list is either a list of items in column, or a single item.
        default:
            blk = 2, overide with blk = 2,3,4,5 etc
    """
    def __init__(self, listOfCols, **kw):
        self.cols = []
        self.blk = kw['blk'] if 'blk' in kw else 2
        for c in listOfCols:
            self.cols.append(col(items=[c] if type(c) is not list else c, blk=self.blk))
        self.row = row(items=self.cols)
        self.initParamItems(kw)
    def html(self):
        return self.row.html()
        
        
class form(htmlelement):
    """
        a form object is a combination of rows & columns. Each row cotains columns. 
        
        Example:
        In:
            aForm = form('fId1', options=['target="/formHandler"', 'method="POST"'])
        Out:
            <form  target="/formHandler" method="POST">
                items
            </form>
    """
    def __init__(self, frmId, **kw):
        self.id = frmId
        self.initParamItems(kw)
    def html(self):
        """
            something
        """
        toReturn = self.getChildHtml(['<form id="%s" %s>'%(self.id, self.printOp())])
        toReturn.append('</form>')
        return toReturn
    
class container(htmlelement):
    """
        basic bootstrap delement required for grid / block system.
        
        kw args:
            fluid=True, will result in container spanning entire row block
        
    """
    def __init__(self, **kw):
        self.fluid = kw['fluid'] if 'fluid' in kw else False
        self.initParamItems(kw)
    def html(self):
        toReturn = self.getChildHtml(['<div class="{cont} {options}">'.format(
            cont='container' if self.fluid is False else 'container-fluid',
            options=self.printOp())]
            )
        toReturn.append('</div>')
        return toReturn

class sidebar(htmlelement):
    """
        Side bar - type(ul) styled with sidebar navbar-nav where items are inside of type(li) nav items
    """
    def __init__(self, **kw):
        self.id = kw['id'] if 'id' in kw else 'sidebar-default'
        self.blk = '4' if 'blk' not in kw else kw['blk'] # Default blk cnt is 4
        self.fixed = True
        self.initParamItems(kw)
    def html(self):
        sidebarItems = []
        for item in self.items:
            sidebarItems.append(li(items=[item],options=['nav-item']))
        sideBarUl = ul(items=sidebarItems, blk=self.blk, id=self.id, options=['sidebar', 'navbar-nav'])
        return sideBarUl.html()
        
#aSideBar = sidebar(items=[text_box('a text box', value=""), button('button a', value="button a"), button('button b', value="button b"), button('button c', value="button c")])
    

class header(htmlelement):
    """
        Large Text appearing in various different size depending on provided size
        headerText - Large Text to Appear 
        size:  
            1 = <h1>Text</h1> 
            2 = <h2>Text</h2>
            3 = <h3>Text</h3>
    """
    def __init__(self, headerText, size, **kw):
        self.headerText = headerText
        self.size = size
        self.initParamItems(kw)
    def html(self):
        toReturn = ['<div class="page-header">']
        toReturn.append('<h{sz}>{tx}</h{sz}>'.format(sz=self.size,tx=self.headerText))
        toReturn.append('</div>')
        return toReturn

class navbar(htmlelement):
    """
        barType - type options (top / bottom ) TOODOO: right / left 
        kw:
            bgcolor: default dark, light,dark, primary,
        options:
            fixed-top
            fixed-bottom
            navbar-dark
        Example:
            
        
        <nav class="navbar navbar-inverse fixed-top">
          <div class="container-fluid">
            <div class="navbar-header">
              <a class="navbar-brand" href="#">WebSiteName</a>
            </div>
            <ul class="nav navbar-nav">
              <li class="active"><a href="#">Home</a></li>
              <li><a href="#">Page 1</a></li>
              <li><a href="#">Page 2</a></li>
              <li><a href="#">Page 3</a></li>
            </ul>
          </div>
        </nav>    
    """
    def __init__(self, barType, **kw):
        self.id = kw['id'] if 'id' in kw else ''
        self.barType = barType
        self.bg = 'bg-dark' if not 'bgcolor' in kw else 'bg-%s'%(kw['bgcolor'])
        self.expand = 'navbar-expand-md' if not 'expand' in kw else kw['expand']
        self.header = kw['header'] if 'header' in kw else None
        self.initParamItems(kw)
    def navprintOp(self):
        retOps = ''
        for op in self.options:
            retOps = retOps + ' %s'%(op)
        return retOps
    def html(self):
        toReturn = ['<nav class="navbar{options} {bg} {expand}">'.format(options=self.navprintOp(),
                                                            bg=self.bg, expand=self.expand),
                        '<div class="container-fluid">']

        withChild = self.getChildHtml(toReturn)
        withChild.append('</div>')
        withChild.append('</nav>')
        return withChild

class modal(htmlelement):
    """
        A modal consists of two elements:
        - type(a) which triggers
        - modal dialog - elements which are displayed by the modal 


        <a href="#" data-toggle="modal" data-target="#login-modal">Login</a>
        <div class="modal fade" id="login-modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: none;">
    	  <div class="modal-dialog">
				<div class="loginmodal-container">
					<h1>Login to Your Account</h1><br>
				  <form>
					<input type="text" name="user" placeholder="Username">
					<input type="password" name="pass" placeholder="Password">
					<input type="submit" name="login" class="login loginmodal-submit" value="Login">
				  </form>
					
				  <div class="login-help">
					<a href="#">Register</a> - <a href="#">Forgot Password</a>
				  </div>
				</div>
			</div>
		</div>
    """
    def __init__(self, linkName, id, **kw):
        self.id = id
        self.a_link = a(linkName,href='#', custom='data-toggle="modal" data-target="#%s"'%(self.id))
        self.initParamItems(kw)
    def html(self):
        toReturn = self.a_link.html()
        toReturn.append(
            '<div class="modal fade" id="%s" tabindex="-1" role="document" aria-labelledby="modal-body" aria-hidden="true">'%(self.id)
        )
        toReturn.append(
            '<div class="modal-dialog" role="document">'
        )
        toReturn.append(
            '<div class="modal-content">'
        )
        toReturn.append(
            '<div class="modal-body" id=modal-body>'
        )
        withChild = self.getChildHtml(toReturn)
        withChild.append('</div>')
        withChild.append('</div>')
        withChild.append('</div>')
        withChild.append('</div>')
        return withChild

        

        