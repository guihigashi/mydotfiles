#!/usr/bin/env bash

get_uuid() {
    lsblk --output NAME,UUID | awk -v name="$1" '$1 ~ name { print $2 }'
}

cat <<EOF
UUID=$(get_uuid sdb1) /mnt/HDD    ntfs3 rw,iocharset=utf8,uid=1000,gid=1000,dmask=027,fmask=137 0 0
UUID=$(get_uuid sdb2) /mnt/data1  btrfs defaults,subvol=data,compress=zstd:1 0 0
EOF

exit 0
