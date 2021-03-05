# SPDX-License-Identifier: GPL-3.0-or-later

import threading
import sys


class StackManager:
    '''
    Manages a main stack 
    Widget to manage a stack of pages with arrows for forward and backward navigation.
    Pages can may allow proceeding or ask for it via return values of their load() method.
    Pages can save their information by implementing a unload() method.
    The stack also offers methods for navigating it from outside.
    '''

    section: int = 0
    page: int = 0
    furthest_page: int = 0
    maximum_page: int = 0

    def __init__(self, stacks, pages, global_state, **kwargs):
        super().__init__(**kwargs)

        self.main_stack, self.image_stack, self.previous_stack, self.next_stack = stacks
        self.global_state = global_state
        self.navigation_lock = threading.Lock()

        # setup pages
        self.pages = pages
        self.current_pages = []

    def _go_to_next(self):
        # save current page
        page = self.current_pages[self.current]
        if hasattr(page, 'unload'):
            page.unload()

        # load next
        if self.current == self.maximum:
            self._load_section(self.current_section + 1)
        else:
            self._load_page(self.current + 1)

    def _load_section(self, section):
        old_pages = self.current_pages

        self.current_section = section
        self.current = 0
        self.accessible = 0
        self.maximum = len(self.pages[self.current_section]) - 1

        # initialize pages in section
        self.current_pages = []
        for page in self.pages[self.current_section]:
            page = page(self.global_state)
            self.main_stack.add_named(page, page.__gtype_name__)
            self.current_pages.append(page)

        self._load_page(self.current)

        # clean up old pages
        for page in old_pages:
            page.destroy()

    def _load_page(self, page_number):
        assert page_number >= 0, 'Tried to go to non-existent page (underflow)'
        assert page_number <= self.maximum, 'Tried to go to non-existent page (overflow)'

        self.current = page_number
        self._make_accessible(self.current)

        # load page
        page = self.current_pages[self.current]
        self.main_stack.set_visible_child_name(page.__gtype_name__)
        icon_name = page.load()

        if not icon_name:
            self._go_to_next()
        else:
            # set icon
            self.global_state.window._set_image(icon_name)

            self._update_navigation_buttons()

    def _make_accessible(self, page):
        # setting accessible bigger than the maximum allows for forward navigation
        self.accessible = max(self.accessible, page)

    def _make_inaccessible(self, page):
        self.accessible = max(self.current, page-1)

    def _update_navigation_buttons(self):
        # update navigation buttons
        self.previous_stack.set_visible_child_name('enabled' if self.current > 0 else 'disabled')
        self.next_stack.set_visible_child_name('enabled' if self.accessible > self.current else 'disabled')

    ### public methods ###

    def advance(self, name=None):
        with self.navigation_lock:
            if name:
                current_page_name = self.current_pages[self.current].__gtype_name__
                if not name == current_page_name:
                    return
            self._go_to_next()

    def allow_forward_navigation(self):
        # no lock, only allowed during page load
        self._make_accessible(self.current + 1)
        self._update_navigation_buttons()

    def load_initial_page(self):
        with self.navigation_lock:
            self._load_section(0)

    def try_go_to_next(self):
        with self.navigation_lock:
            if self.current < self.accessible:
                self._go_to_next()

    def try_go_to_previous(self):
        with self.navigation_lock:
            # ignore incorrect calls
            if self.current > 0:
                self._load_page(self.current - 1)
