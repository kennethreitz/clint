# -*- coding: utf-8 -*-

import sys
from clint.packages.ordereddict import OrderedDict
from clint.misc import is_collection


class Args(object):
    """CLI Argument management."""

    def __init__(self, args=None):
        if not args:
            self._args = sys.argv[1:]
        else:
            self._args = args


    def __len__(self):
        return len(self._args)


    def __repr__(self):
        return '<args %s>' % (repr(self._args))

    
    def get(self, x):
        try:
            return self._args[x]
        except IndexError:
            return False


    def get_after(self, x):
        try:
            return self._args[x:]
        except (IndexError, TypeError):
            return False


    def find(self, x):
        """Returns index of first location of x"""
#       ValueError
        pass
        
    def remove(self, x):
        """Removes given arg (or list thereof) from Args object."""
        if is_collection(x):
            for item in x:
                try:
                    self._args.remove(item)
                except ValueError:
                    pass
        else:
            try:
                self._args.remove(x)
            except ValueError:
                pass

    def any_contain(self, x):
        """Tests if given object is contained in any stored argument."""
        if is_collection(x):
            for arg in self.all:
                for _arg in x:
                    if _arg in arg:
                        return True
            return False
        else:
            for arg in self.all:
                if x in arg:
                    return True
            return True

    def contains(self, x):
        """Tests if given object is in arguments list. 
           Accepts strings and lists of strings."""
        
        if is_collection(x):
            for arg in self.all:
                if arg in x:
                    return True
            return False
        else:
            return (x in self.all)



    def find(self, x):
        """Returns first found index of given value (or list of values)"""
        
        def _find( x):
            try:
                return self.all.index(str(x))
            except ValueError:
                return None

        if is_collection(x):
            for item in x:
                found = _find(item)
                if found:
                    return found
            return None
        else:
            return _find(x)

    def find_with(self, x):
        """Returns first found index containing value (or list of values)"""

        def _find(x):
            try:
                for arg in self.all:
                    if x in arg:
                        return self.all.index(arg)
            except ValueError:
                return None

        if is_collection(x):
            for item in x:
                found = _find(item)
                if found:
                    return found
            return None
        else:
            return _find(x)
    
    def contains_at(self, x, index):
        """Tests if given [list of] string is at given index."""

        try:
            if is_collection(x):
                for _x in x:
                    if (_x in self._args[index]) or (_x == self._args[index]):
                        return True
                    else:
                        return False
            else:
                return (x in self._args[index])
        
        except IndexError:
            return False


    def has(self, x):
        """Returns true if argument exists at given index.
           Accepts: integer.
        """
        
        try:
            self._args[x]
            return True
        except IndexError:
            return False


    def value_after(self, x):
        """Returns value of argument after given found argument (or list thereof)."""
        
        try:
            try:
                i = self._args.index(x)
            except ValueError:
                return None
                
            return self._args[i + 1]
            
        except IndexError:
            return None

    @property
    def grouped(self):
        """Extracts --flag groups from argument list.
           Returns {format: [paths], ...}
        """

        collection = OrderedDict(_=list())

        _current_group = None

        for arg in self.all:
            if arg.startswith('--'):
                group = arg.replace('--', '')
                _current_group = group
                collection[group] = []
            elif not arg.startswith('-'):
                if _current_group:
                    collection[_current_group].append(arg)
                else:
                    collection['_'].append(arg)

        return collection

    @property
    def last(self):
        """Returns last argument."""
        
        try:
            return self._args[-1]
        except IndexError:
            return None

    
    @property
    def all(self):
        """Returns all arguments."""
        
        return self._args
    
    @property    
    def no_flags(self):
        """Returns Arg object excluding flagged arguments."""

        fake_args = Args()
        fake_args.__dict__.update(self.__dict__)

        arg_list = []

        for arg in fake_args._args:
            if not arg.startswith('-'):
                arg_list.append(arg)
        fake_args._args = arg_list

        return fake_args

    @property
    def only_flags(self):
        """Returns Arg object excluding non - flagged arguments."""

        fake_args = Args()
        fake_args.__dict__.update(self.__dict__)

        arg_list = []

        for arg in fake_args._args:
            if arg.startswith('-'):
                arg_list.append(arg)
        fake_args._args = arg_list

        return fake_args
        
# TODO: glob expansion
# TODO: support bash expansion


# args.path_expand(list)
# args.

