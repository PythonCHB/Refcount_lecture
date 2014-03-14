
.. Weak References slides file, created by
   hieroglyph-quickstart on Mon Mar 10 21:33:01 2014.


=============================================
Python Memory Management and Weak References
=============================================

Contents:

.. toctree::
   :maxdepth: 2


Memory Management
==================

 * You don't want python objects that are no longer in use taking up memory.
 * You don't want to keep track of all that yourself.
 * Most "scripting languages" or "virtual machines" have some sort of automated memory management

Many ways to do "Garbage collection"

Reference Counting
====================

How memory is managed is not part of the Python Language spec:
 * Jython uses the JVM
 * Iron Python uses the CLR
   - Both are garbage collected
 * PyPy uses: ????

The CPython interpreter uses a reference counting scheme:
 * every time there is a new reference to a Python object, its reference count is increased
 * every time a reference is deleted -- the count is decreased
 * when the reference count goes to zero: the object is deleted (memory freed)

What makes a reference?
========================

* binding to a name::

   x = an_object

* putting it in a container::

   l.append(an_object)

* passing it to a function::

   func(an_object)

Most of the time, you don't need to think about this at all.

How do I see what's going on?
===============================

::

  import sys
  sys.getrefcount(object)

NOTE: This will always return one more than you'd expect, as passing the object to the function increases its refcount by one::

  In [5]: a = []

  In [6]: sys.getrefcount(a)
  Out[6]: 2

[The Heisenberg Uncertainty Principle: you can't observer it without altering it]

Playing with References
========================

::

    In [5]: a = []

	In [6]: sys.getrefcount(a)
	Out[6]: 2

	In [7]: a = []

	In [8]: sys.getrefcount(a)
	Out[8]: 2

	In [9]: b = a

	In [10]: sys.getrefcount(a)
	Out[10]: 3

	In [11]: l = [1,2,3,a]

	In [12]: sys.getrefcount(a)
	Out[12]: 4

Playing with References
========================

::

	In [13]: del b

	In [14]: sys.getrefcount(a)
	Out[14]: 3


	In [15]: del l

	In [16]: sys.getrefcount(a)
	Out[16]: 2

	In [17]: def test(x):
	   ....:     print "x has a refcount of:", sys.getrefcount(x)
	   ....: 

	In [18]: sys.getrefcount(a)
	Out[18]: 2

	In [19]: test(a)
	x has a refcount of: 4

	In [20]: sys.getrefcount(a)
	Out[20]: 2


Playing with References
========================

::

	In [21]: x = 3

	In [22]: sys.getrefcount(x)
	Out[22]: 428

WHOA!!

(hint: interning....)


The Power of Reference Counting
=================================

* You don't need to think about it most of the time.
* Code that creates objects doesn't need to delete them
* Objects get deleted right away
   . They get "cleaned up" (files, for instance)


The Limits of Reference Counting
==================================

Circular references


The Garbage Collector
==================================

::

    import gc


Example
==========

::

import sys
import weakref
import gc

deleted_object_messages = []

class MyChild(object):
    def __init__(self, parent):
        self.parent = weakref.proxy(parent)
        #self.parent = weakref.ref(parent)
        #self.parent = parent
    def __del__(self):
        deleted_object_messages.append( ('MyChild deleted', id(self)) )

class MyParent(object):
    def __init__(self):
        self.my_children = []
    def addChild(self):
        child = MyChild(self)
        self.my_children.append(child)
        return child
    def __del__(self):
        deleted_object_messages.append( ('MyParent deleted', id(self)) )

p = MyParent()

print "refcount for p:", sys.getrefcount(p)
assert sys.getrefcount(p) == 2

a = p.addChild()
a2 = p.addChild()
print "refcount for p after adding an two children:", sys.getrefcount(p)
assert sys.getrefcount(p) == 2

print "p's children:", p.my_children
assert len(p.my_children) == 2

print " a is:", a
print "a's parent:", a.parent
print "a's parent's children:", a.parent.my_children

assert a  is a.parent.my_children[0]
assert a2 is a.parent.my_children[1]


print "a's refcount:", sys.getrefcount(a)
assert sys.getrefcount(a) == 3

print "a2's refcount:", sys.getrefcount(a2)
assert sys.getrefcount(a2) == 3

del p
print "after deleting p:"

print "a's refcount:", sys.getrefcount(a)
assert sys.getrefcount(a) == 2

print "a2's refcount:", sys.getrefcount(a2)
assert sys.getrefcount(a2) == 2

print "deleting a:"
id_a = id(a)
del a
print deleted_object_messages
assert deleted_object_messages[-1][0] == 'MyChild deleted'
assert deleted_object_messages[-1][1] == id_a



print "deleting a2:"
id_a2 = id(a2)
del a2
print deleted_object_messages
assert deleted_object_messages[-1][0] == 'MyChild deleted'
assert deleted_object_messages[-1][1] == id_a2



