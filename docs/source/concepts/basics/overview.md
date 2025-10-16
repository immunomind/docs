# Overview

By design, `immundata` splits the analysis workflow into two clear phases:

1. **Ingestion** – convert your AIRR files into a special format saved on disk, and then read them to a tidy `ImmunData` object.

2. **Transformation**  – explore, annotate, filter and compute on that object.

Before we go into more details for each of the phase, there are three straightforward yet essential concepts to keep in mind:

1. Data units.

2. Aggregation of receptors and repertoires.

3. Pipeline-based execution.

These concepts set it apart from data-frame-based AIRR libraries. By extension, the concepts affect how you would work with and even *think* about the data analysis in other packages such as `immunarch` which use `immundata` as a backbone for computations.