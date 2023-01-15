import os

import click

from features import *


@click.command
def main():
    zsh = [
        GitRepo(
            "git@github.com:ohmyzsh/ohmyzsh.git",
            os.path.expanduser("~/.oh-my-zsh"),
        ),
        GitRepo(
            "git@github.com:romkatv/powerlevel10k.git",
            os.path.expanduser("~/.oh-my-zsh/custom/themes/powerlevel10k"),
            clone_options=["--depth=1"],
        ),
        GitRepo(
            "git@github.com:zsh-users/zsh-autosuggestions.git",
            os.path.expanduser("~/.oh-my-zsh/custom/plugins/zsh-autosuggestions"),
            post_exec="chsh -s $(which zsh)",
        ),
    ]

    shell_theme = [
        GitRepo(
            "git@github.com:chriskempson/base16-shell.git",
            os.path.expanduser("~/.config/base16-shell"),
        ),
        GitRepo(
            "git@github.com:aarowill/base16-gnome-terminal.git",
            os.path.expanduser("~/.config/base16-gnome-terminal"),
            post_exec=os.path.expanduser(
                "~/.config/base16-gnome-terminal/color-scripts/base16-default-dark-256.sh"
            ),
        ),
    ]

    gsettings = ShellCommands(
        [
            "gsettings set org.gnome.desktop.peripherals.mouse speed 0.8",
            "gsettings set org.gnome.desktop.peripherals.mouse accel-profile flat",
            "gsettings set org.gnome.desktop.peripherals.touchpad speed 0.8",
            "gsettings set org.gnome.desktop.sound event-sounds false",
        ]
    )

    rust = ShellCommands(
        [
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path"
        ]
    )

    for feature in [*zsh, *shell_theme, gsettings, rust]:
        if not feature.is_installed():
            if click.confirm(f"Should install '{feature}':", default=True):
                feature.install()
        else:
            print(f"'{feature}' already installed")


if __name__ == "__main__":
    main()
