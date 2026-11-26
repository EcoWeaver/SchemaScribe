# SchemaScribe

SchemaScribe is a tool for extracting structured annotations from scientific papers with large language models (LLMs). Given a paper and a LinkML schema, it has an LLM fill the schema with the information the paper contains and it is designed to link each annotation to its source passage and to ontology identifiers, validate the results and let a person review them before they are accepted.

## An example

The following example shows what this looks like in practice. It comes from a paper which reports that, one year after a salt marsh restoration project, the abundance of mosquito larvae had dropped by 98.7 percent. Being just free text this is only a string, but as an annotation it becomes a small graph containing the following:

- a cause: the restoration of full tidal action
- an effect: the decreased abundance of the mosquito *Aedes dorsalis*
- a claim linking both: how strongly the text asserts causation, how large the reported effect is, as well as the original sentence kept word for word

If the species is also mapped to an identifier in a taxonomy or knowledge base, it then can be recognised in every other paper, independent of how it is called there. Claims from different studies can then be connected into one collection that can easily be searched, compared and traced back to their sources.

## Core principles

**Schema-agnostic.**  
SchemaScribe is built to work with any schema written in LinkML, so it can be applied to whatever data model a project needs. The Causal Mosaic Schema (CAMO) for causal claims in ecology is the first one in use, but the tool is not built around it, which means that other projects and research fields can use their own.

**Modular by design.**  
Ingestion, prompts, LLM backend, validation, review and export are meant to be separate parts that can be exchanged independently. The LLM backend, for example, can be either a hosted API or a locally running model, with both accessed through the same interface.

**Grounded and reproducible.**  
Annotations should be linked to ontologies where possible and each annotation is meant to record the model, the prompt version, the schema version and the source passage that produced it.

**Measured, not assumed.**  
Our goal is to compare models and prompts against an annotated gold standard, using precision, recall and F1 for each field, so that different setups can be judged for suitability.

## How it works

A paper goes through these stages:

- **Ingest.** The paper is loaded as a PDF or as plain text. PDFs are converted to text first, and long papers are split by section if needed.
- **Extraction.** The LLM annotates the text by filling the schema. The schema is converted into a format that LLM APIs understand and is sent along with the request, so that the server can restrict its answers to the schema.
- **Grounding.** Every annotation is tied to a quote from the paper and terms such as species or habitats are mapped to corresponding ontology identifiers.
- **Validation.** The result is checked against the schema and additional checks, for example whether a quote really appears in the paper and errors can be sent back to the model for revision.
- **Review.** A person accepts, edits or rejects each annotation next to the passage it came from.
- **Export.** Accepted annotations can be exported in different formats such as YAML, JSON, RDF or CSV.

Note: Constraining the output to the schema fixes its structure, but a value can still sit in the right field and be wrong, which is what the grounding, validation and review stages are there to catch. Still, SchemaScribe does not decide whether a claim is true but rather records what a paper claims and makes each annotation easy to verify against its source.

## Documentation

The documentation is hosted on Read the Docs and will be continuously updated: https://schemascribe.readthedocs.io
