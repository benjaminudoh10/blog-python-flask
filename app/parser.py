class BlogContentParser:
    def __init__(self, content):
        self._content = content
        self._html = None

        self.build_html()

    def build_html(self):
        blocks = self._content['blocks']

        block_builder = {
            'header': self.build_header,
            'image': self.build_image,
            'paragraph': self.build_paragraph,
            'list': self.build_list,
            'alert': self.build_alert,
            'checklist': self.build_checklist,
            'quote': self.build_quote,
        }

        built_html_blocks = [block_builder.get(block['type'])(block) for block in blocks]
        self._html = ''.join(built_html_blocks)

    def build_header(self, block):
        assert block['type'] == 'header'
        headers = {
            1: 'h1',
            2: 'h2',
            3: 'h3',
            4: 'h4',
            5: 'h5',
            6: 'h6',
        }
        tag = headers[block['data']['level']]
        data = block['data']['text']

        return f"<{tag}>{data}</{tag}>"

    def build_image(self, block):
        assert block['type'] == 'image'

        tag = 'img'
        data = block['data']['file']['url']
        caption = block['data']['caption']

        # todo: add other image block attributes
        return f'''
            <div class="blog-img">
                <{tag} src="{data}" alt="blog-image" />
                <p class="caption">{caption}</p>
            </div>'''
    
    def build_paragraph(self, block):
        assert block['type'] == 'paragraph'

        tag = 'p'
        data = block['data']['text']

        return f"<{tag}>{data}</{tag}>"
    
    def build_list(self, block):
        assert block['type'] == 'list'

        list_types = {
            'ordered': 'ol',
            'unordered': 'ul'
        }

        tag = list_types[block['data']['style']]
        items = [f"<li>{elem}</li>" for elem in block['data']['items']]
        items = "\n".join(items)

        return f"<{tag}>{items}</{tag}>"

    def build_quote(self, block):
        assert block['type'] == 'quote'

        tag = 'div'
        text = block['data']['text']
        caption = block['data']['caption']

        # todo: cater for alignment (left or center)
        return f'<{tag} class="quote"><p>{text}</p><span>{caption}</span></{tag}>'
    
    def build_checklist(self, block):
        assert block['type'] == 'checklist'

        tag = 'div'
        checklists = [
            f"<input type=\"checkbox\" name=\"blog-checklist\" checked={item['checked']} /><label>{item['text']}</label>"
            for item in block['data']['items']
        ]
        checklists = '<br>'.join(checklists)
        return f'<{tag} class="checklist">{checklists}</{tag}>'
    
    def build_alert(self, block):
        assert block['type'] == 'alert'

        tag = 'span'
        text = block['data']['message']
        type = block['data']['type']

        return f'<div class="alert-container"><{tag} class="alert alert-{type}">{text}</{tag}></div>'

    def html(self):
        return self._html
