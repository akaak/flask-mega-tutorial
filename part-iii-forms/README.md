
## Querying the Models

```
$ python
>>

>> from app import db
>> db # shows sqlite
>> import models

>> dir(models)
['Business', 'SQLAlchemy', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'datetime', 'db']


>> from models import Business
>>> dir(Business)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__mapper__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__', '__tablename__', '__weakref__', '_decl_class_registry', '_sa_class_manager', 'added_date', 'biz_id', 'description', 'metadata', 'name', 'query', 'query_class']

>> from datetime import date
>> today = date.today()
>> b = models.Business('biz name', 'biz desc', today)

>> db.session.add(b)
>> db.session.commit()

```
