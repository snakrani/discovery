
class catch_key_error(object):

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        try:
            return self.f(*args)
        except KeyError as e:
            return None
        except TypeError as t:
            return None

