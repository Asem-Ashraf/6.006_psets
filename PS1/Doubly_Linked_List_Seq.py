class Doubly_Linked_List_Node:
    def __init__(self, x):
        self.item = x
        self.prev = None
        self.next = None

    def later_node(self, i):
        if i == 0: return self
        assert self.next
        return self.next.later_node(i - 1)

class Doubly_Linked_List_Seq:
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        node = self.head
        while node:
            yield node.item
            node = node.next

    def __str__(self):
        return '-'.join([('(%s)' % x) for x in self])

    def build(self, X):
        for a in X:
            self.insert_last(a)

    def get_at(self, i):
        node = self.head.later_node(i)
        return node.item

    def set_at(self, i, x):
        node = self.head.later_node(i)
        node.item = x

    def insert_first(self, x):
        newnode = Doubly_Linked_List_Node(x)
        if self.head==None:
            self.head=newnode
            self.tail=newnode
            return
        newnode.next=self.head
        self.head.prev=newnode
        self.head=newnode

    def insert_last(self, x):
        newnode = Doubly_Linked_List_Node(x)
        if self.tail==None:
            self.head=newnode
            self.tail=newnode
            return

        newnode.prev = self.tail
        self.tail.next = newnode
        self.tail=newnode
    def delete_first(self):
        if self.head.next == None:
            ans=self.head
            self.tail=None
            self.head=None
            return ans
        ans=self.head
        self.head=self.head.next
        self.head.prev=None
        return ans.item

    def delete_last(self):
        if self.tail.prev == None:
            ans=self.tail
            self.tail = None
            self.head = None
            return ans
        ans = self.tail
        self.tail = self.tail.prev
        self.tail.next = None
        return ans.item

    def remove(self, x1, x2):
        L2 = Doubly_Linked_List_Seq()
        L2.head=x1
        L2.tail=x2
        if self.head==x1:
            self.head=x2.next
            x2.next.prev=None
        else:
            x1.prev.next=x2.next #this assumes that x2 is not the tail of the list
        if self.tail==x2:
            self.tail=x1.prev
            x1.next.prev=None
        else:
            x2.next.prev=x1.prev #this assumes that x1 is not the head of the list
        x1.prev=None
        x2.next=None
        return L2

    def splice(self, x, L2):
        if L2.head==None and L2.tail==None: # if L2 is empty
            return
        if x.next==None: # if x is the last node in self
            L2.head.prev=self.tail
            self.tail.next=L2.head
            self.tail=L2.tail
            L2.tail=None
            L2.head=None
            return
        x.next.prev=L2.tail
        L2.tail.next = x.next
        x.next = L2.head
        L2.head.prev = x
        L2.head=None
        L2.tail=None

