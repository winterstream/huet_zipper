
def empty_node(item):
    return ((), (), item)

def concat(source, target):
    head, tail = source
    while tail != ():
        target = (head, target)
        head, tail = tail
    return (head, target)

class Cursor(tuple):
    def __new__(cls, values):
        return tuple.__new__(cls, values)

    def __repr__(self):
        return "(p=%s, l=%s, r=%s, d=%s)" % (self.parent, self.left_list, self.right_list, self.data)

    parent     = property(lambda self: self[0])
    left_list  = property(lambda self: self[1])
    right_list = property(lambda self: self[2])
    data       = property(lambda self: self[3])

    def down(self):
        head, tail = self.right_list
        new_left, new_right, new_data = head
        return Cursor(((self.parent, self.left_list, tail, self.data), new_left, new_right, new_data))

    def up(self):
        return Cursor((self.parent[0], self.parent[1], ((self.left_list, self.right_list, self.data), self.parent[2]), self.parent[3]))

    def left(self):
        head, tail = self.left_list
        return Cursor((self.parent, tail, (head, self.right_list), self.data))

    def right(self):
        head, tail = self.right_list
        return Cursor((self.parent, (head, self.left_list), tail, self.data))

    def insert_left(self, item):
        return Cursor((self.parent, (empty_node(item), self.left_list), self.right_list, self.data))

    def insert_right(self, item):
        return Cursor((self.parent, self.left_list, (empty_node(item), self.right_list), self.data))

    def set_data(self, item):
        return Cursor((self.parent, self.left_list, self.right_list, item))

    def rewind(self):
        if self.left_list != ():
            return Cursor((self.parent, (), concat(self.left_list, self.right_list), self.data))
        else:
            return self
        
    def unwind(self):
        if self.right_list != ():
            return Cursor((self.parent, concat(self.right_list, self.left_list), (), self.data))
        else:
            return self

def root(item=None):
    return Cursor((None, (), (), item))
