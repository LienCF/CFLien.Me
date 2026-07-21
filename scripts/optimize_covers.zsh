#!/bin/zsh

set -euo pipefail

script_dir=${0:A:h}
repo_root=${script_dir:h}
cover_dir="${repo_root}/static/images/covers"
webp_quality=${WEBP_QUALITY:-82}
avif_crf=${AVIF_CRF:-32}
avif_preset=${AVIF_PRESET:-6}

for required_command in cwebp ffmpeg; do
    if ! command -v "${required_command}" >/dev/null 2>&1; then
        print -u2 "Required command is unavailable: ${required_command}"
        exit 1
    fi
done

cover_sources=("${cover_dir}"/*.png(N))
if (( ${#cover_sources} == 0 )); then
    print -u2 "No PNG cover images were found in ${cover_dir}"
    exit 1
fi

for source_png in "${cover_sources[@]}"; do
    output_base=${source_png:r}
    cwebp -quiet -q "${webp_quality}" "${source_png}" -o "${output_base}.webp"
    ffmpeg \
        -hide_banner \
        -loglevel error \
        -y \
        -i "${source_png}" \
        -c:v libsvtav1 \
        -crf "${avif_crf}" \
        -preset "${avif_preset}" \
        -pix_fmt yuv420p10le \
        -svtav1-params tune=0:still-picture=1 \
        "${output_base}.avif"
done

print "Optimized ${#cover_sources} cover images."
