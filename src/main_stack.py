import threading
import sys

from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/main_stack.ui')
class MainStack(Gtk.Box):
    __gtype_name__ = 'MainStack'

    '''
    MainStack
    Widget to manage a stack of pages with arrows for forward and backward navigation.
    Pages can may allow proceeding or ask for it via return values of their load() method.
    Pages can save their information by implementing a save() method.
    The stack also offers methods for navigating it from outside.
    '''

    main_stack = Gtk.Template.Child()

    previous_stack = Gtk.Template.Child()
    previous_button = Gtk.Template.Child()

    next_stack = Gtk.Template.Child()
    next_button = Gtk.Template.Child()

    def __init__(self, pages, **kwargs):
        super().__init__(**kwargs)

        self.navigation_lock = threading.Lock()

        # setup pages
        self.pages = pages
        for section in self.pages:
            for page in section:
                self.main_stack.add_named(page, page.__gtype_name__)
                page.set_vexpand(True)

    def _go_to_next(self):
        self._save_current_page()
        if self.current == self.maximum:
            self._load_section(self.current_section + 1)
        else:
            self._make_accessible(self.current + 1)
            self._load_page(self.current + 1)

    def _go_to_previous(self):
        # ignore incorrect (fatal) calls
        if self.current > 0:
            self._load_page(self.current - 1)

    def _load_section(self, section):
        self.current_section = section
        self.current = 0
        self.accessible = 0
        self.maximum = len(self.pages[self.current_section]) - 1

        self._load_page(self.current)

    def _load_page(self, page_number):
        assert page_number >= 0, 'Tried to go to non-existent page (underflow)'
        assert page_number <= self.accessible, 'Tried to go to innaccassible page'
        assert page_number <= self.maximum, 'Tried to go to non-existent page (overflow)'

        self.current = page_number
        self._make_accessible(self.current)

        # load page
        page = self.pages[self.current_section][self.current]
        self.main_stack.set_visible_child_name(page.__gtype_name__)
        retVal = page.load()

        if retVal == 'ok_to_proceed':
            self._make_accessible(self.current + 1)
            self._update_buttons()
        elif retVal == 'waiting':
            self.next_stack.set_visible_child_name('waiting')
        elif retVal == 'automatic':
            self._go_to_next()
        else:
            self._update_buttons()

    def _make_accessible(self, page):
        # setting accessible bigger than the maximum allows for forward navigation
        self.accessible = max(self.accessible, page)

    def _make_inaccessible(self, page):
        self.accessible = max(self.current, page-1)

    def _save_current_page(self):
        page = self.pages[self.current_section][self.current]
        if hasattr(page, 'save'):
            page.save()

    def _update_buttons(self):
        # previous
        if self.current > 0:
            self.previous_stack.set_visible_child_name('enabled')
        else:
            self.previous_stack.set_visible_child_name('disabled')

        # next
        if self.accessible > self.current:
            self.next_stack.set_visible_child_name('enabled')
        else:
            self.next_stack.set_visible_child_name('disabled')

    ### public methods ###
    def advance(self):
        with self.navigation_lock:
            self._go_to_next()

    def load_initial_page(self):
        with self.navigation_lock:
            self._load_section(0)

    def page_can_proceed_automatically(self, name):
        with self.navigation_lock:
            current_page = self.pages[self.current_section][self.current]
            if current_page.__gtype_name__ == name:
                self._go_to_next()

    def page_is_ok_to_proceed(self, name, ok):
        with self.navigation_lock:
            current_page = self.pages[self.current_section][self.current]
            if current_page.__gtype_name__ == name:
                if ok:
                    self._make_accessible(self.current + 1)
                else:
                    self._make_inaccessible(self.current + 1)
                self._update_buttons()

    def try_go_to_next(self):
        with self.navigation_lock:
            if self.current < self.accessible:
                self._go_to_next()

    def try_go_to_previous(self):
        with self.navigation_lock:
            if self.current > 0:
                self._go_to_previous()
