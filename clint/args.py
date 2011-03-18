class Args(object):
    """CLI Argument managment."""
    
    def __init__(self):
        self._args = sys.argv[1:]


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


    def contains(self, x):
        """Tests if given object is in arguments list. 
           Accepts strings and lists of strings."""
        
        if is_collection(x):
            for arg in self._args:
                if arg in x:
                    return True
                else:
                    return False
        else:
            if x in self._args:
                return True
            else:
                return False


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


    def everything_after(self, x):
        """Returns all arguments after given index."""
        try:
            return self._args[x + 1:]
        except IndexError:
            return None


    def last(self):
        """Returns last argument."""
        
        try:
            return self._args[-1]
        except IndexError:
            return None


    def all(self):
        """Returns all arguments."""
        
        return self._args
        
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