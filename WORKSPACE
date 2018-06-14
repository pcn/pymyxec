# From https://github.com/google/subpar

# Use the skylark git_repository resource
# https://docs.bazel.build/versions/master/skylark/backward-compatibility.html#remove-native-git-repository
load("@bazel_tools//tools/build_defs/repo:git.bzl",
     "git_repository", "new_git_repository")

git_repository(
    name = "subpar",
#    remote = "https://github.com/google/subpar",
#    tag = "1.1.0",
     remote = "https://github.com/pcn/subpar",
     commit = "763f32c",
)

# From https://github.com/bazelbuild/rules_python/blob/master/README.md
git_repository(
    name = "io_bazel_rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "8b5d068",
#     remote = "https://github.com/jac-stripe/rules_python.git",  # Contains a fix for loading shared libs from zip files
#     commit = "5893be97181e338447c4da5cdf7c9f4d5e414c02"
)

# Only needed for PIP support:
load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

# This rule translates the specified requirements.txt into
# @my_deps//:requirements.bzl, which itself exposes a pip_install method.
pip_import(
   name = "my_deps",
   requirements = "//:requirements.txt",
)

# Load the pip_install symbol for my_deps, and create the dependencies'
# repositories.
load("@my_deps//:requirements.bzl", "pip_install")
pip_install()


