# -*- coding: utf-8 -*-
import queue
class FakeIn:
    '''
    用于重定向 sys.stdin
    系统默认调用 sys.stdin.readline()[:-1]
    '''
    def __init__(self):
        self.q = queue.LifoQueue() #(stack)

    def readline(self):
        if self.q.empty():
            return '\n'
        else:
            return self.q.get()

    def write(self, words='\n'):
        # q[-1] must be '\n'
        if words and words[-1]=='\n':
            pass
        else: #调用write("")时，或参数最后一位不是\n时
            words += '\n'
        self.q.put(words)

    def clean(self):
        self.q = queue.LifoQueue()
