## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 1](https://github.com/datacite/freya/issues/30): As a data center, I want to see the citations of publications that use my repository for the underlying data, so that I can demonstrate the impact of our repository. 

### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fr0ed--fh20-fca709.svg)](https://doi.org/10.14454/r0ed-fh20)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-1-datacenter-publication-citations%2Fpy-datacenter-publication-citations-with-output.ipynb)

### Examples of GraphQL Queries Used:

* Get works matching the query "Lake Malawi" from [the Global Biodiversity Information Facility](https://www.gbif.org/) 

```
{
pangaea: repository(id: "gbif.gbif") {
    id
    name
    citationCount
    works(query:"Lake Malawi") {
      totalCount
      years {
        title
        count
      }
      nodes {
        id
        type
        publicationYear
        bibtex
        titles {
          title
        }
        citationCount
        viewCount
        downloadCount
      }
    }
  }
}
```

* Get citations of work [IUCN Red List assessment occurrence data for freshwater species native to the Lake Malawi/Nyasa/Niassa Catchment](https://doi.org/10.15468/1z5fn8) 

```
{
  work(id: "https://doi.org/10.15468/1z5fn8") {
    id
    titles {
      title
    }
    type
    publicationYear
    citations(first: 75) {
      totalCount
      nodes {
        id
        type
        publicationYear
        repository {
          id
          name
        }
        titles {
          title
        }
        bibtex
        citationCount
        viewCount
        downloadCount
      }
    }
  }
}
```
