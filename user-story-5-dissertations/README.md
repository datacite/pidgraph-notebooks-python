## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 5](https://github.com/datacite/freya/issues/35): As a student using the British Library's EThOS database, I want to be able to find all dissertations on a given topic. 
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fjkar--xj80-fca709.svg)](https://doi.org/10.14454/jkar-xj80)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-5-dissertations%2Fpy-dissertations-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve maximum 100 dissertations via query: "Machine learning"

```
{
dissertations(query: "Machine learning", first: 100) {
    totalCount
    years {
      count
      title
    }
    nodes {
      id
      titles {
        title
      }
      descriptions {
         description
      }
      versionOfCount
      identifiers {
        identifier
      }
      publicationYear
      bibtex
      repository {
        id
      }
      publisher
      creators {
        id
        name
      }
    }
  }
}
```
