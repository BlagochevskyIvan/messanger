class Foo:
    def __str__(self) -> str:
        return 'привет'
foo = Foo()
print(foo)

import uuid
print(uuid.uuid4())