import re
import io


class StringIO(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getvalue(self):
        value = super().getvalue()
        ANSI_ESC = re.compile(r'\x1b[^m]*m')
        return ANSI_ESC.sub("", value)
