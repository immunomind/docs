# Units: chain -> barcode -> receptor

Basic units of data operations are:

- **Chain** is a single V(D)J sequence record (read/contig/molecule), e.g., TRA, TRB, IGH, or IGL. This is a minimally possible data unit, a building block of everything. It is the smallest sequence-level unit and remains immutable after ingest so you can always drill down to its exact nucleotide/amino-acid sequence and annotations.

- **Barcode** is a physical container that can hold 0, 1, or multiple chains.
    - Single-cell: a droplet/cell barcode.
    - Spatial: a spot barcode (may capture transcripts from multiple cells).
    - Bulk: the term “barcode” is not used; instead, sequences are grouped into "clonotypes" within a sample.
It is a biological unit that "stores" relevant biological data and is used for aggregation of same chains and computing counts of same receptors coming from different barcodes. Inherits any per‑cell / per‑sample metadata you add.

- **Receptor** is a logical grouping of chains that represents one biological receptor instance used for downstream analysis and reporting. All immune repertoire statistics or receptor tracking is computed on receptors. It is defined by a user-specified receptor schema consisting of:
    - Receptor features: typically CDR3 amino-acid (AA) sequence, optionally combined with V gene (and, if desired, J gene or length).
    - Receptor chains: e.g., single chain, α+β (TCR), heavy+light (BCR), or other well-defined groupings. In multi-chain cases (e.g., dual-α), specify your pairing/merging rules.

To summarise: chains are how `immundata` stores the information, barcodes bundle chains together, and receptors are the minimal units on which repertoire statistics are computed.

| Term               | In plain English                                                                                         | How **immundata** represents it                                                                                                             | **Role**                                                              |
| ------------------ | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Chain**          | A single V(D)J transcript (e.g. *TRA* or *IGH*) coming from one read or contig.                          | One row in the physical table `idata$annotations`; retains `locus`, `cdr3`, `umis`/`reads` and other crucial rearrangement characteristics. | **Raw data unit** – atomic building block.                            |
| **Barcode / Cell** | The droplet (10x), spot (Visium) or well a chain was captured in.                                        | Column `imd_barcode`.                                                                                                                       | **Physical bundle** – groups chains that share a capture compartment. |
| **Receptor**       | The biological receptor you analyse: a single chain **or** a paired set (αβ, Heavy-Light) from one cell. | Virtual table `idata$receptors`; unique ID `imd_receptor_id`.                                                                               | **Logical unit** – minimal object for AIRR statistics.                |
| **Repertoire**     | A set of receptors grouped by sample, donor, cluster, etc.                                               | Physical table `idata$repertoires`; unique ID `imd_repertoire_id`; grouping columns you choose.                                             | **Aggregate unit** – higher-level grouping for comparative analysis.  |