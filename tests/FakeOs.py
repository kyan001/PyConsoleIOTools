# -*- coding: utf-8 -*-
import queue
class FakeOs:
    '''用于重定向 os.system'''
    def __init__(self):
        self.call_q = queue.LifoQueue() #(stack)

    def system(self, cmd):
        self.call_q.put(cmd);
        return 0;

    def readline(self):
        if self.call_q.empty():
            return None
        else:
            return self.call_q.get()

    def clean(self):
        self.call_q = queue.LifoQueue()
