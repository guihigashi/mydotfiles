import abc
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from textwrap import dedent


class Feature(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def install(self):
        pass

    @abc.abstractmethod
    def is_installed(self) -> bool:
        pass

    @abc.abstractmethod
    def uninstall(self):
        pass


@dataclass
class Features(Feature):
    features: list[Feature]

    def install(self):
        for f in self.features:
            if not f.is_installed():
                f.install()
            else:
                print("already installed")

    def is_installed(self):
        return all(f.is_installed() for f in self.features)

    def uninstall(self):
        for f in self.features:
            if f.is_installed():
                f.uninstall()


@dataclass
class DnfInstall(Feature):
    packages: list[str] = field(default_factory=list)

    def install(self):
        subprocess.run(["dnf", "-y", "install", *self.packages])

    def is_installed(self):
        dnf_installed = (
            subprocess.run(["dnf", "list", "--installed"], capture_output=True)
            .stdout.decode("utf-8")
            .splitlines()
        )
        pat = re.compile(r"^(.+?)\.(?:noarch|x86_64|i686).*$")
        matches = filter(None, (pat.match(line) for line in dnf_installed))
        installed_packages = (m.group(1) for m in matches)

        return all(any(p in i for i in installed_packages) for p in self.packages)

    def uninstall(self):
        subprocess.run(["dnf", "-y", "uninstall", *self.packages])


@dataclass
class ShellCommands(Feature):
    commands: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        header = "ShellCommands:\n"
        body = "\n".join(self.commands)

        return f"{header}{body}"

    def install(self):
        for cmd in self.commands:
            subprocess.run(cmd, shell=True)

    def is_installed(self) -> bool:
        return False

    def uninstall(self):
        pass


@dataclass
class FileWithContent(Feature):
    path: str
    content: str

    def __str__(self) -> str:
        return f"File: {self.path}"

    def install(self):
        with open(self.path, "x") as f:
            f.write(dedent(self.content.strip("\n")))

    def is_installed(self) -> bool:
        if not os.path.exists(self.path):
            return False

        with open(self.path) as f:
            lines = f.readlines()
            return "".join(lines) == dedent(self.content.strip("\n"))

    def uninstall(self):
        os.remove(self.path)


class GitRepo(Feature):
    repo: str
    dir: str
    post_exec: str | None
    clone_options: list[str]

    def __init__(
        self,
        repo,
        directory,
        *,
        post_exec: str | None = None,
        clone_options: list[str] | None = None,
    ) -> None:
        self.repo = repo
        self.dir = directory
        self.post_exec = post_exec
        self.clone_options = [] if clone_options is None else clone_options

    def __str__(self) -> str:
        return f"Git: {self.repo}"

    def install(self):
        subprocess.run(["git", "clone", *self.clone_options, self.repo, self.dir])
        if self.post_exec is not None:
            subprocess.run(self.post_exec, shell=True)

    def is_installed(self) -> bool:
        return os.path.exists(self.dir)

    def uninstall(self):
        return os.remove(self.dir)


Contents = list[str | dict[str, "Contents"]]
Folder = dict[str, Contents]


class FolderContentSync(Feature):
    config: Folder
    source: str
    dest: str

    def __init__(self, config_path: str, source: str, dest: str) -> None:
        self.source = source
        self.dest = dest

        with open(config_path) as f:
            self.config = json.load(f)

    def install(self):
        for folder, file in traverse_config(self.config):
            src_folder = f"{self.source}/{'/'.join(folder)}"
            dest_folder = f"{self.dest}/{'/'.join(folder)}"

            Path(dest_folder).mkdir(parents=True, exist_ok=True)

            src = Path(f"{src_folder}/{file}")
            dst = Path(f"{dest_folder}/{file}")

            shutil.copy(src, dst)

    def is_installed(self) -> bool:
        return all(
            Path(f"{self.dest}/{'/'.join(k)}/{v}").exists()
            for k, v in traverse_config(self.config)
        )

    def uninstall(self):
        for k, v in traverse_config(self.config):
            Path(f"{self.dest}/{'/'.join(k)}/{v}").unlink()


def traverse_config(config: Folder, base_folder=[]):
    for folder, contents in config.items():
        if folder == "$schema":
            continue

        acc_folder = [
            *base_folder,
            *([] if folder == "home" else [folder]),
        ]

        for content in contents:
            match content:
                case str():
                    yield acc_folder, content
                case dict():
                    yield from traverse_config(content, acc_folder)
