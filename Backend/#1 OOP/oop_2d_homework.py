class MyClass:

        @classmethod
        def method(cls, arg):
            print('%s classmethod. %d' % (cls.__name__, arg))

        @classmethod
        def call_original_method(cls):
            cls.method(5)

        def call_class_method(self):
            self.method(10)

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, x):
            self._x = x
        

class MySubclass(MyClass):

    @classmethod
    def call_original_method(cls):
        cls.method(6)


# Вызываем методы класса через класс.
MyClass.method(0)  # MyClass classmethod. 0
MyClass.call_original_method()  # MyClass classmethod. 5
  
MySubclass.method(0)  # MySubclass classmethod. 0
MySubclass.call_original_method()  # MySubclass classmethod. 6

# Вызываем методы класса через объект.
my_obj = MyClass()
my_obj.method(1)  # MyClass classmethod. 1
my_obj.call_class_method()  # MyClass classmethod. 10
my_obj.call_original_method()

MyClass.x = 32
print(MyClass.x)

