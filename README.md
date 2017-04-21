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

Set up database

```
$ mkdir Amity/database
$ python Amity/models/models.py
```

Run the application

```
$ python amity.py -i
```

**Commands**
```
create_room <room_name>...
add_person <first_name> <last_name> <type> [--accommodate=N]
reallocate_person <first_name> <last_name> <new_room_name>
load_people
print_allocations [--o=file_name]
print_unallocated [--o=file_name]
print_room <room_name>
allocate_office <first_name> <last_name>
allocate_livingspace <first_name> <last_name>
save_state [--db=sqlite_database]
load_state <sqlite_database>
quit
reset
clear
restart
```
