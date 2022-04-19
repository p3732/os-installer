class Page:
    image_name: str
    can_navigate_backward: bool = False
    can_navigate_forward: bool = False
    can_reload: bool = False

    loaded: bool = False

    def id(self):
        return self.__gtype_name__

    ### dummy stubs ###

    def navigate_backward(self):
        '''
        Called upon backward navigation if `can_navigate_backward` is True.
        '''
        return

    def navigate_forward(self):
        '''
        Called upon forward navigation if `can_navigate_forward` is True.
        '''
        return

    def load(self):
        '''
        Called before the page is shown.
        Pages can overwrite this to receive call every time.
        Returning True means the page can be skipped.
        '''
        if not self.loaded:
            self.loaded = True
            return self.load_once()

    def load_once(self):
        '''
        Called once on first page construction. Used for e.g. filling lists.
        Returning True means the page can be skipped.
        '''
        return

    def unload(self):
        '''
        Called before the page is no longer shown. Used for e.g. storing current enrty values.
        '''
        return
