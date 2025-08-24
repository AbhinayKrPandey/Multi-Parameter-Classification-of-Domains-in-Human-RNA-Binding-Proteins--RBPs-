# Multi-Parameter-Classification-of-Domains-in-Human-RNA-Binding-Proteins--RBPs-
This project, a Bachelor's Thesis submitted to the Indian Institute of Technology Kharagpur, investigates the relationship between evolutionary conservation and the physicochemical properties of domains in human RNA-binding proteins (RBPs). The study's primary goal is to develop a novel multi-parameter classification system for these domains by correlating conservation patterns with key amino acid properties.
This repository contains the scripts and analysis performed for the thesis, which provides a comprehensive framework for understanding domain evolution and could inform prediction algorithms for domain boundaries and functions.
## Core Objectives
### Data Curation: 
To create a robust dataset of standard reported RNA-binding domains (RBDs) from a large dataset of structurally solved human RBPs.
-- Conservation Analysis: To quantify the degree of amino acid conservation within these domains and assess its relationship with various physicochemical parameters.
-- Domain Classification: To develop a multi-parameter classification system for domains based on their unique conservation patterns and correlations.
-- Functional Correlation: To correlate these classification patterns with the known catalytic activities of the domains, revealing how functional constraints influence evolutionary pressures.
## Methodology
The research followed a detailed and reproducible methodology, leveraging key bioinformatics tools and Python libraries:
### Datasets
- A curated dataset of 658 human RBPs with experimentally resolved structures, sourced from the UniProt Database and Protein Data Bank (PDB).
- Protein sequences and domain annotations were retrieved from UniProt in FASTA and XML formats.
### Tools and Software
- Python 3.8: Used as the primary programming language for all automation, data processing, and analysis.
- Pandas: Utilized for efficient data manipulation, filtering, and organization of tabular data.
- NumPy and SciPy: Enabled numerical computations and statistical analysis, including Pearson correlation analysis and linear regression.
- Matplotlib: Used for generating all visualizations, such as histograms and plots.
### ClustalW2 (v. 2.1): A powerful tool for performing Multiple Sequence Alignments (MSA) of domain sequences.
### IUPred3: Employed for predicting intrinsically disordered regions by estimating residue-specific energy changes. This tool provided both long and short disorder scores.
### Key Analytical Steps
- Domain Identification: A custom Python script was used to identify and extract domain boundaries from UniProt XML files.
- Disorder Prediction: IUPred3 was run on all domains to characterize their structural properties and predict intrinsically disordered regions.
## Conservation Quantification:
### Shannon Entropy (Hi): Calculated for each aligned position to measure variability. A value of zero indicates perfect conservation.
### Amino Acid Conservation Factor: 
- A custom metric developed to quantify the prevalence of each amino acid across aligned positions.
- Local Environment Analysis: A window-based approach analyzed the local physicochemical environment of amino acids within domains, categorizing them by properties such as polarity, charge, and aromaticity.
- Correlation and Classification: Pearson correlation analysis was performed to examine the relationships between the conservation factors and various physicochemical properties. This allowed for the classification of domains based on their dominant evolutionary constraints
### Key Findings
- Conservation Patterns: The analysis revealed that domain regions exhibit a higher degree of sequence conservation compared to surrounding non-domain regions.
- Functional Constraints: A key finding was that domains with similar catalytic activities often shared similar correlation patterns. This suggests that the functional requirements of a domain are a primary driver of its evolutionary constraints.
- Property-Specific Correlations: Different domain types showed distinct correlations. For example, some domains were strongly correlated with molecular weight, indicating size-related evolutionary pressure, while others correlated more with charge properties.
- Multi-parameter Framework: The developed classification system provides a new framework for understanding the complex interplay between amino acid properties and functional constraints in RBPs.
### Future Scope
- The project concludes with several potential avenues for further research:
- Comparative Proteomics: A comparative analysis of conservation patterns between human and non-human proteomes.
- Domain vs. Non-Domain Analysis: Expanding the analysis to non-domain regions of RBPs to uncover new correlation patterns.
- Broader Application: Applying the same methodology to other protein types, such as DNA-binding proteins, to identify unique correlation patterns specific to RBPs.
- Target-Specific Classification: A sub-classification of RBPs based on the specific type of RNA they bind (e.g., mRNA, tRNA) to analyze relative conservation stress.
