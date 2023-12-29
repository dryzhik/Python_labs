from abc import ABC
import time


class BaseDecorator(ABC):
    def __init__(self, function):
        self.function = function
        self.history = list()
        self.__name__ = self.function.__name__
        self.execution_time = 0

    def __call__(self, *args):
        self.decorate(*args)
        self.keep_history(time.localtime(), *args)

    @abstractmethod
    def decorate(self, *args):
        pass

    def keep_history(self, call_time, *args):
        format_call_time = time.strftime("%H:%M:%S", call_time)
        function_name = self.function.__name__
        arguments = ', '.join([str(arg) for arg in args])
        self.history.append(f"<{format_call_time}>: function <{function_name}> called with arguments <{arguments}>")


class ExecutionTime(BaseDecorator):
    def decorate(self, *args):
        start_time = time.perf_counter()
        func = self.function(*args)
        end_time = time.perf_counter()
        self.execution_time = end_time - start_time

        print("Время выполнения:", self.execution_time)

        return func


class HtmlExecutionTime(BaseDecorator):
     def decorate(self, *args):
        func = self.function(*args)
        execution_time = self.function.execution_time

        print(f"<html><body>{execution_time}</body></html>")
        print("------------------------------------")

        return func


@HtmlExecutionTime
@ExecutionTime
def square_for(my_list):
    print("Функция с циклом for ")
    square_list = []
    for i in my_list:
        square_list.append(i ** 2)
    print(square_list)


@HtmlExecutionTime
@ExecutionTime
def square_list_comprehension(my_list):
    print("Функция с list comprehension ")
    square_list = [i ** 2 for i in my_list]
    print(square_list)


@HtmlExecutionTime
@ExecutionTime
def square_map(my_list):
    # time.sleep(1)
    print("Функция с map ")
    square_list = list(map(lambda f: f ** 2, my_list))
    print(square_list)


if __name__ == "__main__":
    test_list = [i for i in range(9)]
    square_for(test_list)
    square_list_comprehension(test_list)
    square_map(test_list)
