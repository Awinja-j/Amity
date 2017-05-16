#!venv/bin/python
"""
Usage:
Amity>> create_room <roomtype> <name>...                                                           
Amity>> add_person <first_name> <last_name> <person_role> [--accommodate=N]   
Amity>> find_userid <first_name> <last_name>                                                       
Amity>> reallocate_person <person_ID> <room_name>                                               
Amity>> load_people <filename>
Amity>> print_allocations [--o=file_name]
Amity>> print_unallocated [--o=file_name]
Amity>> print_room <room_name>
Amity>> save_state [--db=<sqlite_database>]
Amity>> load_state [--db=<sqlite_database>]
Amity>> quit
Amity>> (-i | --interactive)
Amity>> (-h | --help)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from colorama import init
init(strip=not sys.stdout.isatty())
from docopt import docopt, DocoptExit
from Amity import Amity
from db_conn import DbManager
from termcolor import cprint
from pyfiglet import figlet_format


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class FrontAmity(cmd.Cmd):
    header = "  A M I T Y  "
    cprint(figlet_format(header, font="starwars"), "green")
    intro = """
      THE SPACE ALLOCATOR OF YOUR DREAMS   """
    cprint(figlet_format(intro, font='digital'), "white")

    prompt = 'Amity>> '
    file = None
    amity = Amity()


    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""
        print(self.amity.create_room(arg['<room_type>'], arg['<room_name>']))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_role> [--a=<want_accomodation>]"""
        person_name = arg['<first_name>'] + ' ' + arg['<last_name>']
        if arg['--a'] == None:
            want_accomodation = 'n'
        else:
            want_accomodation = str(arg['--a'])
        person_role = arg['<person_role>']
        print(self.amity.add_person(person_name, person_role,want_accomodation))

    @docopt_cmd
    def do_find_userid(self, arg):
        """Usage: find_userid <first_name> <last_name>"""
        person_name = arg['<first_name>'] + ' ' + arg['<last_name>']
        print(self.amity.find_userid(person_name))
    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_ID> <room_name>"""
        print(self.amity.reallocate_person(int(arg['<person_ID>']), arg['<room_name>']))
    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <filename>"""
        self.amity.load_people(arg['<filename>'])
    @docopt_cmd
    def do_print_allocations(self, args):
        '''Usage: print_allocations [--o=filename]'''
        print(self.amity.print_allocations(args))
    @docopt_cmd
    def do_print_unallocated(self,args):
        """Usage: print_unallocated [--o=filename]"""
        print(self.amity.print_unallocated(args))
    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        print(self.amity.print_room(arg['<room_name>']))
    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=<sqlite_database>]"""
        print(args)
        self.amity.save_state(args)
    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [--db=<sqlite_database>]"""
        self.amity.load_state(args)

    def do_quit(self, arg):
        """Usage: quit"""
        print('System closed.')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        FrontAmity().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")
