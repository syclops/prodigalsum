"""
Built-in range wrapper class.

This is provided for reference and testing purposes. It is deliberately not
documented to give you practice in reading unfamiliar code and in designing your
own implementation without too much potential bias. You should not edit any
code, but feel free to add your own documentation to this file if it's helpful.

Author: Steve Matsumoto <stephanos.matsumoto@sporic.me>
"""


class BuiltinRange:

    def __init__(self, start, stop=None, step=1):
        if stop is None:
            builtin_range = range(start)
        else:
            builtin_range = range(start, stop, step)
        self.iter = iter(builtin_range)
        self.current = None
        self.in_range = True
        self.next()

    def value(self):
        return self.current

    def next(self):
        try:
            self.current = next(self.iter)
        except StopIteration:
            self.in_range = False

    def done(self):
        return not self.in_range
