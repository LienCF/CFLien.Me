#!/bin/zsh
# Generate AVIF and WebP variants for every PNG cover, plus a 10:3 center-cropped
# preview pair used by the home page summary cards.
# Existing outputs are kept; pass --force to re-encode everything.

set -euo pipefail

script_dir=${0:A:h}
repo_root=${script_dir:h}
cover_dir="${repo_root}/static/images/covers"
webp_quality=${WEBP_QUALITY:-82}
avif_crf=${AVIF_CRF:-32}
avif_preset=${AVIF_PRESET:-6}
preview_width=${PREVIEW_WIDTH:-1300}
preview_height=${PREVIEW_HEIGHT:-390}
force_encode=0
if [[ ${1:-} == "--force" ]]; then
    force_encode=1
fi

for required_command in cwebp ffmpeg sips; do
    if ! command -v "${required_command}" >/dev/null 2>&1; then
        print -u2 "Required command is unavailable: ${required_command}"
        exit 1
    fi
done

needs_encode() {
    local target_file=$2
    (( force_encode )) && return 0
    [[ ! -f ${target_file} ]]
}

encode_webp() {
    local source_file=$1 target_file=$2
    shift 2
    cwebp -quiet -q "${webp_quality}" "$@" "${source_file}" -o "${target_file}"
}

encode_avif() {
    local source_file=$1 target_file=$2 video_filter=${3:-}
    local -a filter_args=()
    if [[ -n ${video_filter} ]]; then
        filter_args=(-vf "${video_filter}")
    fi
    ffmpeg \
        -hide_banner \
        -loglevel error \
        -y \
        -i "${source_file}" \
        "${filter_args[@]}" \
        -c:v libsvtav1 \
        -crf "${avif_crf}" \
        -preset "${avif_preset}" \
        -pix_fmt yuv420p10le \
        -svtav1-params tune=0:still-picture=1 \
        "${target_file}"
}

cover_sources=("${cover_dir}"/*.png(N))
if (( ${#cover_sources} == 0 )); then
    print -u2 "No PNG cover images were found in ${cover_dir}"
    exit 1
fi

encoded_count=0
for source_png in "${cover_sources[@]}"; do
    output_base=${source_png:r}

    if needs_encode "${source_png}" "${output_base}.webp"; then
        encode_webp "${source_png}" "${output_base}.webp"
        (( encoded_count += 1 ))
    fi
    if needs_encode "${source_png}" "${output_base}.avif"; then
        encode_avif "${source_png}" "${output_base}.avif"
        (( encoded_count += 1 ))
    fi

    # Center crop to the 10:3 box the home page uses, then downscale.
    source_width=$(sips -g pixelWidth "${source_png}" | awk '/pixelWidth/ {print $2}')
    source_height=$(sips -g pixelHeight "${source_png}" | awk '/pixelHeight/ {print $2}')
    crop_height=$(( source_width * preview_height / preview_width ))
    if (( crop_height > source_height )); then
        crop_height=${source_height}
    fi
    crop_top=$(( (source_height - crop_height) / 2 ))

    if needs_encode "${source_png}" "${output_base}-preview.webp"; then
        encode_webp "${source_png}" "${output_base}-preview.webp" \
            -crop 0 "${crop_top}" "${source_width}" "${crop_height}" \
            -resize "${preview_width}" "${preview_height}"
        (( encoded_count += 1 ))
    fi
    if needs_encode "${source_png}" "${output_base}-preview.avif"; then
        encode_avif "${source_png}" "${output_base}-preview.avif" \
            "crop=${source_width}:${crop_height}:0:${crop_top},scale=${preview_width}:${preview_height}"
        (( encoded_count += 1 ))
    fi
done

print "Encoded ${encoded_count} cover variants for ${#cover_sources} PNG covers."
