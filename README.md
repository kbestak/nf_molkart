# ![nf-core/molkart](docs/images/nf-core-molkart_logo_light.png#gh-light-mode-only) ![nf-core/molkart](docs/images/nf-core-molkart_logo_dark.png#gh-dark-mode-only)

[![GitHub Actions CI Status](https://github.com/nf-core/molkart/workflows/nf-core%20CI/badge.svg)](https://github.com/nf-core/molkart/actions?query=workflow%3A%22nf-core+CI%22)
[![GitHub Actions Linting Status](https://github.com/nf-core/molkart/workflows/nf-core%20linting/badge.svg)](https://github.com/nf-core/molkart/actions?query=workflow%3A%22nf-core+linting%22)[![AWS CI](https://img.shields.io/badge/CI%20tests-full%20size-FF9900?labelColor=000000&logo=Amazon%20AWS)](https://nf-co.re/molkart/results)[![Cite with Zenodo](http://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-1073c8?labelColor=000000)](https://doi.org/10.5281/zenodo.XXXXXXX)

[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A523.04.0-23aa62.svg)](https://www.nextflow.io/)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![run with singularity](https://img.shields.io/badge/run%20with-singularity-1d355c.svg?labelColor=000000)](https://sylabs.io/docs/)
[![Launch on Nextflow Tower](https://img.shields.io/badge/Launch%20%F0%9F%9A%80-Nextflow%20Tower-%234256e7)](https://tower.nf/launch?pipeline=https://github.com/nf-core/molkart)

[![Get help on Slack](http://img.shields.io/badge/slack-nf--core%20%23molkart-4A154B?labelColor=000000&logo=slack)](https://nfcore.slack.com/channels/molkart)[![Follow on Twitter](http://img.shields.io/badge/twitter-%40nf__core-1DA1F2?labelColor=000000&logo=twitter)](https://twitter.com/nf_core)[![Follow on Mastodon](https://img.shields.io/badge/mastodon-nf__core-6364ff?labelColor=FFFFFF&logo=mastodon)](https://mstdn.science/@nf_core)[![Watch on YouTube](http://img.shields.io/badge/youtube-nf--core-FF0000?labelColor=000000&logo=youtube)](https://www.youtube.com/c/nf-core)

## Introduction

**nf-core/molkart** is a pipeline for processing Molecular Cartography data from Resolve Bioscience (combinatorial FISH). It takes as input a table of FISH spot positions (x,y,z,gene), a corresponding DAPI image and optionally a membrane staining image in the `tiff` format. nf-core/molkart performs end-to-end processing of the data including image pre-processing, QC filtering of spots, cell segmentation, spot-to-cell assignment and reports quality metrics such as the spot assignment rate, average spots per cell and segmentation mask size ranges.

<p align="center">
    <img title="molkart workflow" src="docs/images/nfcore_molkart_metromap.png" width=30%>
</p>

1. Correct grid lines with [Mindagap](https://github.com/ViriatoII/MindaGap) on any provided image.
2. Apply contrast-limited adaptive histogram equalization ([CLAHE](https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.equalize_adapthist)) on any provided image (can be toggled off).
3. Perform segmentation to create cell masks with [Mesmer's](https://doi.org/10.1038/s41587-021-01094-0) whole-cell model ([Cellpose](https://www.cellpose.org/), and [ilastik](https://www.ilastik.org/) also available).
4. Run QC filtering on spots to filter out duplicates with [Mindagap](https://github.com/ViriatoII/MindaGap).
5. Project spots to multichannel image.
6. Quantify spots per cell with [MCQuant](https://github.com/labsyspharm/quantification).
7. Gather QC metrics specific to the pipeline.
8. Produce QC report with [`MultiQC`](http://multiqc.info/).

## Usage

:::note
If you are new to Nextflow and nf-core, please refer to [this page](https://nf-co.re/docs/usage/installation) on how
to set-up Nextflow. Make sure to [test your setup](https://nf-co.re/docs/usage/introduction#how-to-run-a-pipeline)
with `-profile test` before running the workflow on actual data.
:::

First, prepare a samplesheet with your input data that looks as follows:

`samplesheet.csv`:

```csv
sample,nuclear_image,spot_locations,membrane_image
sample1,sample1_DAPI.tif,sample1_spots.txt, sample1_WGA.tif
```

Each row represents a sample or FOV. It is denoted by the sample identifier, the path the nuclear image that corresponds to that FOV, the path to the spots table that corresponds to that FOV, and an optional second channel that could help guide segmentation (such as a membrane stain).

Now, you can run the pipeline with default values using:

```bash
nextflow run nf-core/molkart \
   -profile <docker/singularity/.../institute> \
   --input samplesheet.csv \
   --outdir <OUTDIR>
```

:::warning
Please provide pipeline parameters via the CLI or Nextflow `-params-file` option. Custom config files including those
provided by the `-c` Nextflow option can be used to provide any configuration _**except for parameters**_;
see [docs](https://nf-co.re/usage/configuration#custom-configuration-files).
:::

For more details and further functionality, please refer to the [usage documentation](https://nf-co.re/molkart/usage) and the [parameter documentation](https://nf-co.re/molkart/parameters).

## Pipeline output

To see the results of an example test run with a full size dataset refer to the [results](https://nf-co.re/molkart/results) tab on the nf-core website pipeline page.
For more details about the output files and reports, please refer to the
[output documentation](https://nf-co.re/molkart/output).

## Credits

nf-core/molkart was originally written by [Florian Wünnemann](https://github.com/FloWuenne) and adapted to nf-core by [Krešimir Beštak](https://github.com/kbestak) in the [Spatial omics group](https://www.schapirolab.com/) at the [Institute for Computational Biomedicine](https://www.medizinische-fakultaet-hd.uni-heidelberg.de/einrichtungen/institute/institute-for-computational-biomedicine) funded by the [HiGHmed initiative](https://www.highmed.org/en/home).

We thank [Maxime U Garcia](https://github.com/maxulysse) for his valuable assistance in the development of this pipeline.

## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).

For further information or help, don't hesitate to get in touch on the [Slack `#molkart` channel](https://nfcore.slack.com/channels/molkart) (you can join with [this invite](https://nf-co.re/join/slack)).

## Citations

<!-- TODO nf-core: Add citation for pipeline after first release. Uncomment lines below and update Zenodo doi and badge at the top of this file. -->
<!-- If you use  nf-core/molkart for your analysis, please cite it using the following doi: [10.5281/zenodo.XXXXXX](https://doi.org/10.5281/zenodo.XXXXXX) -->

An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.

You can cite the `nf-core` publication as follows:

> **The nf-core framework for community-curated bioinformatics pipelines.**
>
> Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.
>
> _Nat Biotechnol._ 2020 Feb 13. doi: [10.1038/s41587-020-0439-x](https://dx.doi.org/10.1038/s41587-020-0439-x).
