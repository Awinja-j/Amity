#!venv/bin/python
"""

Usage:
front.py createroom -t <roomtype> -n <name>...                          creates room in Amity
front.py editroom      <edit_room>                                      Edits room
front.py edit_room_type <editroom_type>
front.py Delete_room <DeleteRoom>
front.py addperson -n <first_name> <last_name> -r <person_role> -a [--accommodate=N] -p <phone_number>   Adds person to Amity 
front.py Edit_person_name <first_name> <last_name>
front.py Edit_person_info <name>
front.py delete_person <name>
front.py reallocate_person <first_name> <last_name> <new_room_name>     reallocates person in Amity
front.py load_people
front.py print_allocations [--o=file_name]
front.py print_unallocated [--o=file_name]
front.py print_room <room_name>
front.py allocate_livingspace <first_name> <last_name>
front.py save_state [--db=sqlite_database]
front.py load_state <sqlite_database>
front.py quit
front.py reset
front.py clear
front.py restart
front.py (-i | --interactive)
front.py (-h | --help)
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
    text = "Amity"
    cprint(figlet_format(text, font="basic"), "white")
    intro = " Welcome to Amity"
    prompt = 'Amity>> '
    file = None
    amity = Amity()

    @docopt_cmd
    def do_createroom(self, arg):
        """Usage: createroom -t <room_type> -n <room_name>..."""
        # print(self.amity.create_room(arg['<room_type>'], arg['<room_name>']))
        # print(arg)
        self.amity.create_room(arg['<room_type>'], arg['<room_name>'])

    @docopt_cmd
    def do_addperson(self, arg):
        """Usage: addperson -n <first_name> <last_name> -r <person_role> -a [<want_accomodation>] -p <phone_number>"""
        # print(arg)
        person_name = arg['<first_name>'] + arg['<last_name>']
        self.amity.add_person(person_name, arg['<person_role>'], arg['<want_accomodation>'],
                                    arg['<phone_number>'])

    @docopt_cmd
    def do_edit_person_info(self, arg):
        """Usage:editpersoninfo <entry> """
        print(self.amity.edit_person_name(arg['entry']))

    @docopt_cmd
    def do_editroom(self, arg):
        """Usage:"""
        pass
    @docopt_cmd
    def do_editroomtype(self, arg):
        pass
    @docopt_cmd
    def do_Deleteroom(self, arg):
        pass
    @docopt_cmd
    def do_editpersoninfo(self, arg):
        pass
    @docopt_cmd
    def do_Deleteperson(self, arg):
        pass
    @docopt_cmd
    def do_reallocateperson(self, arg):
        pass
    @docopt_cmd
    def do_loadpeople(self, arg):
        pass
    @docopt_cmd
    def do_printallocations(self, arg):
        pass
    @docopt_cmd
    def do_printunallocated(self, arg):
        pass
    @docopt_cmd
    def do_printroom(self, arg):
        pass
    @docopt_cmd
    def do_allocatelivingspace(self, arg):
        pass
    @docopt_cmd
    def do_savestate(self, arg):
        pass
    @docopt_cmd
    def do_loadstate(self, arg):
        pass
    @docopt_cmd
    def do_quit(self, arg):
        pass
    @docopt_cmd
    def do_reset(self, arg):
        pass
    @docopt_cmd
    def do_clear(self, arg):
        pass
    @docopt_cmd
    def do_restart(self, arg):
        pass

    @docopt_cmd
    def do_search(self, args):
        """Usage: Searches <name>"""
        full_name = args['<name>']
        print(c_manager.search(full_name))

    @docopt_cmd
    def do_text(self, args):
        """Usage: text <name> -m <message>..."""
        name = args['<name>']
        message = " ".join(args['<message>'])
        print(c_manager.text(name, message))

    def do_quit(self, arg):
        """quit"""
        print('System closed.')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        print(__doc__)
        FrontAmity().cmdloop()
    except KeyboardInterrupt:
        print("Exiting App")
