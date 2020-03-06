# The Prodigal Sum

The goals of this exercise are to:

* Understand how bundling class variables and functions (encapsulation) in
  Python offers conceptual and performance benefits in software development.
* Understand how and why the `range` object in Python provides performance
  benefits over lists, despite having similar functionality.
* Practice implementing a Python class with no starter code.

## Introduction: Gauss and Python's range()

An old tale about the mathematician
[Carl Gauss](https://en.wikipedia.org/wiki/Carl_Gauss) says that when he was a
young boy in school, his teacher asked the students to add up all of the
integers from 1 to 100. Gauss quickly worked out that the pairs (1, 100), (2,
99), and so on all summed to 101, and there were 50 of these pairs, the last one
being (50, 51). So 50 * 101 = 5050.

There is some discussion about how accurate this story is, and you can read
about one effort to investigate the truth of the story
[here](https://www.americanscientist.org/article/gausss-day-of-reckoning).

In Python, you can compute and print the sum of the integers from 1 to 100 with
the following code:

```python
gauss_sum = 0

for i in range(1, 101):
    gauss_sum += i

print(f"The sum of the first 100 positive integers is {gauss_sum}")
```

(If you're wondering about the last line, I'm using
[f-strings](https://www.python.org/dev/peps/pep-0498/), which is a more readable
way of including variable values in strings.)

The `range()` function is often taught relatively early and used frequently in
Python courses. It's almost entirely used in the context of iteration - it's
rare that I see `range()` outside of a statement like `for i in range(10)`.

Iteration is also often done over a list. For example, if you have a list of
integers `step_counts` representing the number of steps you walked each day, you
could do something like this:

```python
max_steps = 0

for steps in step_counts:
    if steps > max_steps:
        max_steps = steps

print(f"The most steps I walked in a day was {max_steps}")
```

And although it may seem a bit strange, I could have written the Gauss sum code
like this:

```python
gauss_sum = 0

for i in list(range(1, 101)):
    gauss_sum += i

print(f"The sum of the first 100 positive integers is {gauss_sum}")
```

In the days of Python 2, these code snippets would have done pretty much exactly
the same thing under the hood, so this way of writing things would just be a bit
redundant. But in Python 3, there are technical reasons why you wouldn't want to
use the second way.

In this exercise, we'll dig deeper into what those reasons are and why the
change was made between Python 2 and 3. This is also a great opportunity to
practice designing and implementing classes in Python, so we'll explore this
topic by writing and testing two classes that offer range-like features.

## Overview of Tasks

In a nutshell, this exercise consists of creating two new classes that can
roughly be used like a `range`, one called `ListRange` that simulates the
version of `range` from Python 2, and one called `IndexRange` that simulates the
version from Python 3. These classes do not offer all of the functionality of
`range`, only enough to help you see how they behave differently in practice.

There are three main tasks to this exercise:

* Design and implement `ListRange` using a list as a class variable.
* Design and implement `IndexRange` using start, stop, and step indices as class
  variables.
* Test your implementations against one another and against a reference class
  `BuiltinRange` for correctness and performance.
  
### Starter Code

While you will write almost all of the code for `ListRange` and `IndexRange`,
the repository contains some starter files that form the scaffolding for your
implementation. There are four code files for you to read and/or edit:

* `gauss_sum.py` is the script that you will use to test your implementations.
* `builtin_range.py` contains the code for the reference class `BuiltinRange`.
  This class is a *wrapper* for `range`: it only uses built-in functions and a
  feature of `range` to provide the functions used in `gauss_sum.py`.
* `list_range.py` contains the code for `ListRange`. It is nearly empty, so you
  will have to fill in most of it.
* `index_range.py` contains the code for `IndexRange`. It is nearly empty, so
  you will have to fill in most of it.
  
Lines 66-68 of `gauss_sum.py` are particularly important for you to understand:

```python
while not range_object.done():
    gauss_sum += range_object.value()
    range_object.next()
```

Here, `range_object` is an instance of one of the range implementation. As you
can see, we do not use a `for` loop here because of the way the classes are
set up - instead, we have to "approximate" a `for` loop. We do this by creating
a `while` loop that goes until the object is "done", and moving onto the next
value in the range at the end of each iteration of the loop.

When `range_object` is created, it is given an initial value. At any point, you
can get the current value of the object with `range_object.value()`. You can get
the object to move to its next value with `range_object.next()`. The function
`range_object.done()` tells you whether you have finished iterating through the
range. Thus at the absolute minimum, your classes will need to implement these
three methods.

### Running Tests

As you go through this exercise, you should use the `gauss_sum.py` script to
test your code. In Terminal, you can run a test like this:

```shell script
$ time python3 gauss_sum.py 101
```

This will time how long it takes to sum all of the integers from 0 to 100. If
you leave off `time` at the beginning of the command, the script will run but
you won't see how long it took to run.

In Atom, if you have the Script plugin, you can run `gauss_sum.py` by opening
the file and selecting `Packages -> Script -> Configure Script` and filling in
everything you would write after `gauss_sum.py` in the "Program Arguments"
field. Unfortunately, with this method, you cannot time how long the script
takes.

The script includes several more options. You can see all of these options by
running

```shell script
$ python3 gauss_sum.py -h
```

This will print all of the possible options with an explanation of each one.

As shown in the first example of this script, you need to provide at least one
integer to the program. If you provide one integer and it is positive, the
script will sum all of the integers from 1 to one below that integer. (If the
integer is not positive, the script should just print the sum as 0.)

If you provide multiple integers, they will be assumed to represent the start,
end, and optionally the step (1 by default). If you run

```shell script
$ time python3 gauss_sum.py 1 13 2
```

the script will sum all integers from 1 up to (but not including) 13, stepping
by 2 each time (so the sum will be 1 + 3 + 5 + 7 + 9 + 11 = 36). This can
sometimes cause some confusion - using `1 12 2` will yield the same results
since 12 is still 1 larger than 11. Also note that any or all of the integers
can be negative, so `1 -3 -1` would compute the sum 1 + 0 + -1 + -2 = -2.

You can also do nonsensical things like `1 10 -1` - in this case, the script
will yield 0 as the sum.

You can also add a range type option before the integers:

```shell script
$ time python3 gauss_sum.py --range-type builtin 0 101 1
```

The `--range-type builtin` bit lets you select from the different range
implementations. Including `--range-type builtin` causes the sum to be computed
with `BuiltinRange` (which is the default), include `--range-type list` will
instead use `ListRange`, and `--range-type index` will use `IndexRange`. The
latter two classes have not yet been implemented, so you will get an error if
you try to run the script without changing any files in this repository.

You should use the default (`--range-type builtin` or simply leave it out) to
check that your own implementations are correct. If you did not get the same
results with `--range-type list` or `--range-type index` as with
`--range-type builtin` then you probably have a bug in your code.

## The ListRange Class

Your implementation of `ListRange` must create a list from the start, stop, and
step values passed to the script, representing all integers in the range. You
can do this very easily using the `range` function, but you will need to use a
trick or two to get the `__init__` function to work with one, two, or three
integers as arguments.

Your implementation should not store the start, stop, and step values once they
have been used to generate the list. It is up to you how you implement the rest
of the methods (`done`, `value`, and `next`).

## The IndexRange Class

Your implementation of `IndexRange` must store the start, stop, and step values.
These (and other variables you store within the class) should be used to 
implement all of the class methods (`__init__` and the three mentioned above).
Do not use lists or `range` objects to store any variables.

## Testing

Use the script to test the same set of integers across all three
implementations. If all goes well, you should have `IndexRange` taking close to
the same time as `BuiltinRange`, but `ListRange` taking a different amount of
time for some sets of integers. What sets of integers are necessary to see a
noteworthy difference in running time? (For some sets, the script may not even
successfully complete at all - you should record this as well.)

## Extension: Error Handling

One way you can extend your code is to raise an exception if the range would be
invalid. We can consider a range as being invalid if it would not cause any
values to be added to the overall sum at all. For example, `1 10 -1` can be
considered invalid because starting at one with a step size of -1 would take us
away from 10 rather than towards it.

If you make this change, you will also need to add a try-except statement in
`gauss_sum.py` to handle this exception.

## Licenses

All code for this exercise is licensed under the MIT License, whose full text
can be found in [`MIT-LICENSE.txt`](MIT-LICENSE.txt).

This README is licensed under a Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License, whose full text
is available in [`CC-LICENSE.txt`](CC-LICENSE.txt), or at
<http://creativecommons.org/licenses/by-nc-sa/4.0/>.

## Notes

This exercise was created for the Software Design course at the Olin College of
Engineering in Spring 2020.
