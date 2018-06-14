package(default_visibility = ["//visibility:public"])

load("@subpar//:subpar.bzl", "par_binary")

load(
  "@io_bazel_rules_python//python:python.bzl",
  "py_binary", "py_library", "py_test"
)

# Load the pip_install symbol for my_deps, and create the dependencies'
# repositories.

load("@my_deps//:requirements.bzl", "requirement")

DEPLOY_DEPS = [
    requirement("requests"),
    requirement("docopt"),
    requirement("mysql-python"),  
]

par_binary(
    name = 'mysql_repl',
    srcs = glob(["bin/mysql_repl.py"], exclude=["test*", "setup.py", "test/**", "bazel-*/**", ]),
    deps = DEPLOY_DEPS,
    data = ["libmysqlclient.so"],
    main = 'bin/mysql_repl.py'
)