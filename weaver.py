import htmlform as f
from makespecial import makeSpecial

# Base html element to start weaver 


class Weaver:
    def __init__(self, server, route='/weaver'):
        server.weaver = self
        self.server = server
        self.route = route
        self.__set_specials()
        self.elements = []
        self.__set_server_route(self.server)
    def __set_server_route(self, server):
        from flask import request as req
        @server.route(self.route, methods=['GET', 'POST'])
        def process_weaver_input():
            request = req
            weaver = self
            tarId = None
            for k,v in request.form.items():
                if k in weaver.idstr:
                    return '\n'.join(weaver.idstr[k]())
            return '<p> resource not found </p>'
    def __set_specials(self):
        self.weavables = []
        ignore = [
            '__name__', '__doc__', '__package__', '__loader__', '__spec__', 
            '__file__', '__cached__', '__builtins__', 'label', 'Input'
            ]
        for k,v in f.__dict__.items():
            if k in ignore:
                continue
            setattr(self, k, makeSpecial(self, v))
            self.weavables.append(k)
        self.weaver_buttons = self.col()
    def get_weaver_buttons(self, id):
        items = []
        for k in self.weavables:
            weavable_btn = f.col(
                blk=2,  
                items=[
                    f.button(
                        k, 
                        value=k,
                        action={
                            'action': 'submit',
                            'id': id + k + '_new',
                            'target': id
                            },
                        )
                    ], 
                id=id + k + '_new')
            items.append(weavable_btn)
        return items
        
    def add_element_button(self, id):
        # need to return row of buttons with weavable options
        #   each button points to its respective weavable html element type
        #   when selected will display form of required inputs for element creation
        self.elements.append(self.row(id='add_html_element', items=self.get_weaver_buttons(id)))
        col = self.col(
            id=id+'_add_element_button',
            items = [
                f.button(
                'AddHtmlElement', 
                value='add_html_element',
                action={
                    'action': 'submit',
                    'id': id+'_add_element_button',
                    'target': id+'_add_element_button'
                })
            ])
        col.action = '/weaver'
        return col




def test():
    from flask import Flask,request
    app = Flask(__name__)
    w = Weaver(app)
    root = w.col(id='root')
    root.add_item(f.button("test", value=''))
    root.add_item(w.add_element_button('root'))

    from htmlpage import page as pg

    h = pg("Home")
    h.head.add_style_sheet('https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css')
    h.head.add_script("https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js")
    h.head.add_script("https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js")
    h.head.add_script("https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js")
    h.head.add_script('/static/webs3.js')

    h.body.add_item(root)



    @app.route('/')
    def home():
        print(w.idstr)
        return h.htmlrender(None)
    app.run(host='0.0.0.0', port=5000, debug=True)
test()