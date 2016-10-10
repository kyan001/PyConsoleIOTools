# -*- coding: utf-8 -*-
import queue
class FakeOut:
    '''
    用于重定向 sys.stdout
    系统默认调用 sys.stdout.write()
    '''
    def __init__(self):
        self.q = queue.LifoQueue() #(stack)
        self.buffer = ""

    def write(self, words):
        self.buffer += words
        if words == '\n': #print会自动单独write一个"\n"在末尾，此时讲打印内容放入list内。
            self.flush();

    def readline(self):
        if self.q.empty():
            return None
        else:
            return self.q.get()

    def flush(self):
        self.q.put(self.buffer)

    def clean(self):
        self.q = queue.LifoQueue() #(stack)
        self.buffer = ""
