# AURA — AI Research & Decision Report
## Research Question
I want to build a solar flare prediction
system using machine learning.

Find relevant papers, datasets and code,
compare existing approaches, identify
limitations, and propose an implementation
roadmap.
## Research Plan
**Goal:** Build a solar flare prediction system using machine learning, including literature review, data and code discovery, methodology comparison, limitation analysis, and an implementation roadmap.
**Domain:** Space Weather / Machine Learning / Astrophysics
### Tasks
- **paper_search** — Identify state-of-the-art research papers and methodologies for solar flare prediction using machine learning.
- **dataset_search** — Find standard datasets used in solar flare prediction research, such as NASA's SDO/HMI data or Space-weather HMI Active Region Patch (SHARP) data.
- **code_search** — Discover existing open-source code repositories and implementations for solar flare forecasting.
- **method_comparison** — Compare different architectural approaches (e.g., SVMs, Random Forests, CNNs, LSTMs) applied to flare prediction.
- **limitation_analysis** — Analyze current limitations in flare prediction models, such as class imbalance, false alarm rates, and feature engineering bottlenecks.
- **implementation_planning** — Formulate a step-by-step implementation roadmap for building, training, and deploying a solar flare prediction system.

## Sources Discovered
- Papers: 2
- Datasets: 2
- Code repositories: 0
- Unified evidence items: 4

## Verified Claims
### Machine learning can be applied to space weather forecasting, specifically for predicting solar flare occurrence.
- Confidence: high
- Reason: Evidence 2 explicitly identifies solar flare occurrence forecasting as a key area of machine learning activity in space weather.
- Supporting evidence IDs: [2]
### SDO/HMI active region magnetograms with flaring activity labels are available as benchmark datasets for training machine learning models for solar flare prediction.
- Confidence: high
- Reason: Both Evidence 3 and Evidence 4 describe SDO HMI magnetograms of solar active regions paired with flare labels useful for supervised and unsupervised machine learning.
- Supporting evidence IDs: [3, 4]
### Current space weather forecasting paradigms should shift toward probabilistic approaches with reliable uncertainty assessment and combine physics-based models with machine learning.
- Confidence: high
- Reason: Evidence 2 highlights the need for probabilistic forecasting and gray box modeling.
- Supporting evidence IDs: [2]
### Extreme Learning Machine (ELM) is a fast-converging training algorithm for single hidden layer feedforward neural networks applied to classification, clustering, and regression.
- Confidence: high
- Reason: Evidence 1 details the definition, theoretical analysis, improvements, and applications of ELM.
- Supporting evidence IDs: [1]

## Key Findings
- Machine learning can be successfully applied to space weather forecasting, specifically targeting the prediction of solar flare occurrences.
- Benchmark datasets comprising NASA Solar Dynamics Observatory (SDO) Helioseismic and Magnetic Imager (HMI) magnetograms with corresponding flaring activity labels are available at both full and reduced resolutions for training supervised/unsupervised machine learning models.
- Extreme Learning Machines (ELM) offer a fast-converging training algorithm for single hidden layer feedforward neural networks (SLFN) suitable for classification, clustering, and regression tasks.

## Method Comparison
### Probabilistic and Gray-Box Space Weather Forecasting
**Strengths**
- Focuses on reliable assessment of uncertainties.
- Combines physics-based approaches with machine learning ('gray box' models).
**Limitations**
- Current forecasting paradigms require a shift toward probabilistic uncertainty assessment.
- Open challenges remain in adopting machine learning across the space weather community.
### Extreme Learning Machine (ELM) for Neural Networks
**Strengths**
- Converges much faster than traditional methods for training single hidden layer feedforward neural networks.
- Yields promising performance for real-time classification, clustering, and regression tasks.
**Limitations**
- Controversies exist regarding ELM, and specific performance metrics or limitations related to solar flare prediction are not detailed in the abstract.
### Machine Learning on SDO/HMI Active Region Magnetograms
**Strengths**
- Uses minimally processed, user-configurable benchmark datasets featuring consistently sized active region images with flare labels.
- Supports supervised and unsupervised methods, binary/multi-class classification, and regression.
**Limitations**
- Specific metadata details like exact time ranges, number of samples, class distribution, and full usage notes are limited or missing from the repository metadata.

## Research Gaps
- Lack of direct evaluation data or code repositories pairing specific machine learning algorithms (like ELM) directly with the SDO/HMI Dryad datasets for flare prediction within the supplied evidence.
- Detailed documentation on class distributions, time ranges, and usage notes for the benchmark datasets is absent from the provided metadata.

## Recommendation
Build a supervised machine learning system for solar flare prediction using benchmark SDO/HMI active region magnetogram datasets paired with flaring activity labels, designed within a probabilistic forecasting framework that accounts for uncertainty assessment.

### Why
- Evidence indicates that machine learning is actively applied to space weather forecasting, specifically for solar flare occurrence.
- NASA SDO/HMI active region magnetograms with flaring activity labels are available as benchmark datasets at both full and reduced resolutions for training.
- Current space weather forecasting recommendations emphasize shifting toward probabilistic approaches with reliable uncertainty assessments.

### Risks
- Specific metadata details such as exact time ranges, sample sizes, and class distributions for the SDO/HMI datasets are limited in the provided evidence.
- Specific code repositories or direct implementations pairing algorithms like ELM directly with the SDO/HMI datasets are not present in the verified evidence.

### Confidence
medium

## Implementation Roadmap
### Phase 1 — Data Acquisition and Exploratory Analysis
**Objective:** Acquire and inspect the benchmark SDO/HMI active region magnetogram datasets and associated flaring labels to understand data structure, missing values, and class distributions.

**Tasks**
- Download full and reduced resolution NASA SDO/HMI active region magnetogram benchmark datasets from Dryad (identifiers 10.5061/dryad.dv41ns23n, 10.5061/dryad.jq2bvq898).
- Inspect data formats, metadata, image dimensions, and associated flaring activity labels.
- Perform exploratory data analysis to evaluate class distributions, time ranges, and sample sizes.

**Deliverables**
- Data profiling report detailing class distributions, sample counts, and data formats.
- Data ingestion and preprocessing scripts.

**Evaluation**
- Successful parsing of all downloaded SDO/HMI records and clear documentation of identified data constraints.
### Phase 2 — Model Architecture and Baseline Design
**Objective:** Design a supervised machine learning architecture incorporating probabilistic forecasting principles and explore fast-converging alternatives such as Extreme Learning Machines (ELM).

**Tasks**
- Define the baseline supervised classification/regression pipeline for binary or multi-class solar flare prediction.
- Incorporate probabilistic output structures to support uncertainty quantification as highlighted in space weather forecasting paradigms.
- Implement a candidate Extreme Learning Machine (ELM) or standard neural network architecture for comparative baseline training.

**Deliverables**
- Model architecture specification document.
- Initial training and validation code framework.

**Evaluation**
- Feasibility check of training execution speed and capability of the architecture to output probabilistic uncertainty estimates.
### Phase 3 — Model Training, Validation, and Uncertainty Quantification
**Objective:** Train the machine learning models using the SDO/HMI benchmark datasets, validate performance, and assess prediction uncertainties.

**Tasks**
- Split the SDO/HMI dataset into training, validation, and test sets, addressing potential class imbalances.
- Train baseline models and candidate ELM architectures using the magnetogram images and flare labels.
- Implement evaluation metrics focusing on reliable uncertainty assessment and probabilistic forecast validation.

**Deliverables**
- Trained model checkpoints.
- Validation performance report including uncertainty metrics.

**Evaluation**
- Model performance benchmarks against validation data, ensuring robust handling of class distributions and reliable uncertainty bounds.

## Major Risks
- Specific metadata details such as exact time ranges, sample sizes, and class distributions for the SDO/HMI datasets are limited in the provided evidence.
- Specific code repositories or direct implementations pairing algorithms like ELM directly with the SDO/HMI datasets are not present in the verified evidence.
- Lower-resolution SDO/HMI datasets offer processing convenience at the potential trade-off of fine-grained spatial feature fidelity.

## Success Criteria
- Successful ingestion and preprocessing of SDO/HMI active region magnetograms and labels.
- Deployment of a functional machine learning training pipeline incorporating probabilistic uncertainty assessment.
- Completion of model evaluation demonstrating predictive capability for solar flare occurrences.

## Evidence Sources
1. [paper] A review on extreme learning machine — https://doi.org/10.1007/s11042-021-11007-7
2. [paper] The Challenge of Machine Learning in Space Weather: Nowcasting and Forecasting — https://doi.org/10.1029/2018sw002061
3. [dataset] Active region magnetograms for solar flare prediction: Full resolution dataset — https://datadryad.org/dataset/doi:10.5061/dryad.dv41ns23n
4. [dataset] Active region magnetograms for solar flare prediction: Reduced resolution dataset — https://datadryad.org/dataset/doi:10.5061/dryad.jq2bvq898
