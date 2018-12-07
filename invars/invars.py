import ast
import click
import os
import sys
from collections import namedtuple
from typing import Iterator


EXCLUDE_VARNAMES = "_"
EXCLUDE_DIRS = (
    ".svn",
    "CVS",
    ".bzr",
    ".hg",
    ".git",
    ".tox",
    ".eggs",
    "*.egg",
    "env",
    "venv",
    "__pycache__",
)


Violation = namedtuple("Violation", ("variable_name", "cur_position", "prev_position"))
Position = namedtuple("Position", ("lineno", "col_offset"))

AST_DEF_STMT = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
AST_LOOP_STMT = (ast.For, ast.AsyncFor, ast.While)
AST_STMTS = (ast.If, ast.With, ast.AsyncWith)


@click.command()
@click.argument("src", nargs=-1)
def main(src=None):
    err = 0
    for file_path in get_files_to_analyze(src):
        for v in analyze_file(file_path):
            err += 1
            sys.stderr.write(
                "{0}:{1}:{2}: variable '{3}' already assigned in line {4}\n".format(
                    file_path,
                    v.cur_position.lineno,
                    v.cur_position.col_offset,
                    v.variable_name,
                    v.prev_position.lineno,
                )
            )

    sys.exit(1 if err > 0 else 0)


def get_files_to_analyze(src=["."]):
    for fn in src:
        if os.path.isdir(fn):
            for fname in get_py_files_in_dir(fn):
                yield fname
        else:
            yield fn


def get_py_files_in_dir(dir):
    for dir_name, _, file_list in os.walk(dir):
        for path in dir_name.split("/"):
            if path in EXCLUDE_DIRS:
                break
        else:
            for fname in file_list:
                if fname.endswith(".py"):
                    yield os.path.join(dir_name, fname)


def analyze_file(filename):
    with open(filename, "rb") as f:
        return analyze_code(f.read())


def analyze_code(code):
    tree = ast.parse(code)
    return list(get_violations(tree, {}))


def get_violations(tree, track_vars, parent=None):
    for node in tree.body:
        for varname in get_assigns_in_node(node):
            if isinstance(parent, AST_LOOP_STMT) and not isinstance(
                node, AST_LOOP_STMT + AST_STMTS
            ):
                # TODO: find a better way to manage this case
                # By definition, all the assignments inside a loop are invalid,
                # except the index variable in a nested loop
                yield Violation(
                    variable_name=varname,
                    cur_position=Position(node.lineno, node.col_offset),
                    prev_position=Position(node.lineno, node.col_offset),
                )

            else:
                if varname not in track_vars:
                    if varname in EXCLUDE_VARNAMES:
                        continue

                    track_vars[varname] = Position(node.lineno, node.col_offset)
                else:
                    position_first_assign = track_vars[varname]
                    yield Violation(
                        variable_name=varname,
                        cur_position=Position(node.lineno, node.col_offset),
                        prev_position=position_first_assign,
                    )

        if isinstance(node, AST_DEF_STMT):
            yield from get_violations(node, {})
        elif isinstance(node, AST_STMTS + AST_LOOP_STMT):
            yield from get_violations(node, track_vars, parent=node)


def get_assigns_in_node(node) -> Iterator[str]:
    if isinstance(node, ast.Attribute):
        # self.name = 1
        yield node.value.id + "." + node.attr  # type: ignore
    elif isinstance(node, ast.Subscript):
        # a['key'] = 'value'
        pass
    elif isinstance(node, ast.Tuple):
        # a, b = 1, 2
        for target in node.elts:
            yield target.id  # type: ignore
    elif isinstance(node, ast.Name):
        # a = 1
        yield node.id
    elif isinstance(node, (ast.For, ast.AsyncFor)):
        if isinstance(node.target, ast.Tuple):
            # for a, b in d.items()
            yield from get_assigns_in_node(node.target)
        else:
            # for i in range(10)
            yield node.target.id  # type: ignore
    elif isinstance(node, (ast.With, ast.AsyncWith)):
        # with open('file.txt') as (a, b)
        for item in node.items:
            yield from get_assigns_in_node(item.optional_vars)
    elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
        # a += 1
        # a -= 1
        yield from get_assigns_in_node(node.target)
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            yield from get_assigns_in_node(target)


if __name__ == "__main__":
    main()
