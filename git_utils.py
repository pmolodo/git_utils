"""
Collection of python utilities for using git
"""


import os
import subprocess
from typing import Any, Dict, Iterable, List, Optional


class Git:
    """
    Get a git runner object which will execute commands within a specific
    directory.

    To execute within the current directory, use `git = Git(".")`
    """

    def __init__(
        self,
        work_dir: str,
        git_exec: str = "git",
        args: Iterable[str] = (),
        kwargs: Optional[Dict[str, Any]] = None,
    ):
        self.work_dir = os.path.abspath(work_dir)
        if kwargs is None:
            kwargs = {}
        kwargs.setdefault("cwd", self.work_dir)
        self.args = [git_exec] + list(args)
        self.kwargs = kwargs

    def __call__(self, args: Iterable[str], **kwargs) -> subprocess.CompletedProcess:
        final_kwargs = dict(self.kwargs)
        final_kwargs.setdefault("check", True)
        final_kwargs.setdefault("encoding", "utf8")
        final_kwargs.update(kwargs)
        final_args = list(self.args) + list(args)
        return subprocess.run(final_args, **final_kwargs)

    def output(self, args: Iterable[str], **kwargs) -> str:
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.STDOUT)
        return self(args, **kwargs).stdout

    def lines(
        self, args: Iterable[str], strip: bool = True, non_empty: bool = True, **kwargs
    ) -> List[str]:
        lines = self.output(args, **kwargs).splitlines()
        if strip:
            lines = [x.strip() for x in lines]
        if non_empty:
            lines = [x for x in lines if x]
        return lines

    def list_branches(self):
        branches_dir = "refs/heads"
        branches = self.lines(["for-each-ref", "--format=%(refname)", branches_dir])
        # strip out a leading "refs/heads/"
        prefix = branches_dir + "/"
        return [x[len(prefix) :] if x.startswith(prefix) else x for x in branches]
