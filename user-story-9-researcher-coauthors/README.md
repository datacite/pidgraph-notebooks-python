## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 9](https://github.com/datacite/freya/issues/26): As a bibliometrician, I want to know all the co-authors of a particular researcher, so that I can do a network analysis of the researcher's collaborations. 
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2F62t3--0822-fca709.svg)](https://doi.org/10.14454/62t3-0822)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-9-researcher-coauthors%2Fpy-researcher-coauthors-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Get publications including co-authors for [Dr Sarah Teichmann](https://orcid.org/0000-0002-6294-6366):

```
{
  person(id: "https://orcid.org/0000-0002-6294-6366") {
    id
    name
    publications(first:300) {
      totalCount
      years {
        title
        count
      }
      nodes {
        id
        type
        versionOfCount
        titles {
          title
        }
        creators {
          id
          name
        }
      }
    }
  }
}
```
