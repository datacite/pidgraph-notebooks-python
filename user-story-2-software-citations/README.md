## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 2](https://github.com/datacite/freya/issues/63): As a software author, I want to be able to see the citations of my software aggregated across all versions. so that I see a complete picture of reuse.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2F27b7--9g84-fca709.svg)](https://doi.org/10.14454/27b7-9g84)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-2-software-citations%2Fpy-software-citations-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve metadata for software: [Calculation Package: Inverting topography for landscape evolution model process representation](hhttps://doi.org/10.5281/zenodo.2799488), including all its versions.

```
{
  software(id: "https://doi.org/10.5281/zenodo.2799488") {
    id
    titles {
      title
    }
    publicationYear
    citations {
      nodes {
        id
        titles {
          title
        }        
      }
    }
    version
    versionCount
    versionOfCount
    citationCount
    downloadCount
    viewCount    
    versions {
      nodes {
        id
        version
        publicationYear
        titles {
          title
        }
        citations {
          nodes {
            id
            titles {
              title
            }
          }
        }
        version
        versionCount
        versionOfCount
        citationCount
        downloadCount
        viewCount        
      }
    }
  }
}

```
