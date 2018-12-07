# invars

This package brings *invariable variables* or **single assignment variables** to Python (like in [Erlang](http://erlang.org/doc/reference_manual/expressions.html#variables) and other functional programming languages).

**Examples**

```python
one = 1
two = 2
...
two += one  # invalid!
```

```python
total = 0
for i in range(4):
    total += i  # invalid!
```

## Installation

```console
$ pip install invars
```

## Usage

```
$ invars my_script.py
```


## Why?

>  In functional programming, assignment is discouraged in favor of single assignment. [...] Imperative assignment can introduce side effects while destroying and making the old value unavailable while substituting it with a new one


[Wikipedia](https://en.wikipedia.org/wiki/Assignment_%28computer_science%29#Single_assignment)

> Single assignment variables simplifies a lot of things because it takes out the "time" variable from your programs.

[Stack Overflow](https://stackoverflow.com/questions/11255632/the-purpose-of-single-assignment)


## TODO

 - [ ] Integrate with `flakes8`
