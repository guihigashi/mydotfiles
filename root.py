import click

from features import *


@click.command
def main():
    root_features: list[Feature] = [
        FileWithContent(
            "/etc/yum.repos.d/vscode.repo",
            """
            [code]
            name=Visual Studio Code
            baseurl=https://packages.microsoft.com/yumrepos/vscode
            enabled=1
            gpgcheck=1
            gpgkey=https://packages.microsoft.com/keys/microsoft.asc
            """,
        ),
        ShellCommands(
            [
                "grubby --update-kernel=ALL --args=systemd.unified_cgroup_hierarchy=1",
                "rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                "dnf -y remove fedora-chromium-config",
                "dnf install"
                " https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"
                " https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm",
                "dnf -y update",
                "dnf -y groupupdate core",
                'dnf -y groupupdate multimedia --setop="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin',
                "dnf -y groupupdate sound-and-video",
                "timedatectl set-local-rtc 0",
            ]
        ),
    ]

    for feature in root_features:
        if not feature.is_installed():
            if click.confirm(f"Should install '{feature}':", default=True):
                feature.install()
        else:
            print(f"'{feature}' already installed")


if __name__ == "__main__":
    main()
