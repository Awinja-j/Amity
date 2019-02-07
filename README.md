# Amity
This is a room allocation system for one of Andela’s facilities called Amity

**Installation**

```
$ git clone  https://github.com/Awinja-Andela/Amity.git
$ cd Amity
```

Create and activate a virtual environment

```
$ mkvirtualenv env
$ workon env
```

Install dependencies

```
$ pip install -r requirements.txt
```

Run the application

```
$ python application/front.py --interactive
```

**Commands**
```
create_room <room_type> <room_name>...
add_person <first_name> <last_name> <FELLOW|STAFF> [--p=<phone_number>] [--a=want_accomodation]
find_userid <first_name> <last_name
reallocate_person <person_ID> <new_room_name>
load_people <filename>
print_allocations [--o=file_name]
print_unallocated [--o=file_name]
print_room <room_name>
save_state [--db=sqlite_database]
load_state [--db=sqlite_database]
quit
reset
```
