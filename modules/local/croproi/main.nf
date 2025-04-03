process CROPROI {
    tag "$meta.id"
    label 'process_single'

    container 'ghcr.io/schapirolabor/molkart-local:v0.0.4'

    input:
    tuple val(meta), path(image)

    output:
    tuple val(meta), path("*.txt") , emit: crop_summary
    tuple val(meta), path("*.png") , emit: crop_overview
    path "versions.yml"           , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    export MPLCONFIGDIR=./tmp
    export NUMBA_CACHE_DIR=./tmp

    tmp_crop_roi.py \\
        --input ${image} \\
        --output . \\
        --name ${prefix} \\
        $args

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        molkart_croproi: \$(crop_roi.py --version)
    END_VERSIONS
    """

    stub:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    touch ${prefix}_CropOverview.png
    touch ${prefix}_CropSummary.txt

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        molkart_croproi: \$(crop_roi.py --version)
    END_VERSIONS
    """
}
