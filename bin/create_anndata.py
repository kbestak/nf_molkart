#!/usr/bin/env python
## Written by Kresimir Bestak and Florian Wuennemann and released under the MIT license.
import pandas as pd
import numpy as np
from anndata import AnnData
import argparse
from argparse import ArgumentParser as AP
from os.path import abspath
import time
from scipy.sparse import csr_matrix


def get_args():
    # Script description
    description = """Anndata object creation"""

    # Add parser
    parser = AP(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Sections
    inputs = parser.add_argument_group(
        title="Required Input", description="Path to required input file"
    )
    inputs.add_argument(
        "-i", "--input", type=str, help="Path to the spot2cell csv file."
    )
    inputs.add_argument(
        "-s", "--spatial_cols", nargs="+", help="Column names for location data."
    )
    inputs.add_argument(
        "-o",
        "--output",
        dest="output",
        action="store",
        required=True,
        help="Path to output anndata object.",
    )
    inputs.add_argument("--version", action="version", version="0.2.0")
    arg = parser.parse_args()
    arg.input = abspath(arg.input)
    arg.output = abspath(arg.output)
    return arg


def create_spatial_anndata(input, spatial_cols):
    # Extracts information from filename to name obs
    filename = input.split("/")[-1].split(".")[0]
    seg_method = filename.split("_")[-1]
    sample_id = "_".join(filename.split("_")[:-1])

    df = pd.read_csv(input, index_col="CellID")
    spatial_coords = np.array(df[spatial_cols].values.tolist())
    # Assumption - spatial columns start off the metadata columns
    first_spatial_col = min(spatial_cols, key=lambda col: df.columns.get_loc(col))
    boundary_index = df.columns.get_loc(first_spatial_col)
    metadata_cols = df.columns[boundary_index:]
    metadata = df[metadata_cols]
    gene_cols = df.columns[:boundary_index]

    count_table = csr_matrix(df[gene_cols].values.tolist())
    adata = AnnData(
        count_table, obsm={"spatial": spatial_coords}, var=pd.DataFrame(index=gene_cols)
    )
    for col in metadata.columns:
        adata.obs[col] = metadata[col].values

    adata.obs_names = [f"{sample_id}-{seg_method}-cell_{i}" for i in range(adata.n_obs)]
    return adata


def main(args):
    adata = create_spatial_anndata(args.input, args.spatial_cols)
    adata.write(args.output)


if __name__ == "__main__":
    args = get_args()
    st = time.time()
    main(args)
    rt = time.time() - st
    print(f"Script finished in {rt // 60:.0f}m {rt % 60:.0f}s")
