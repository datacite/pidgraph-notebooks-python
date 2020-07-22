## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 4](https://github.com/datacite/pidgraph-notebooks-python/issues/8): As a funder I want to see how many of the research outputs funded by me have an open license enabling reuse, so that I am sure I properly support Open Science.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fqaym--kt26-fca709.svg)](https://doi.org/10.14454/qaym-kt26)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-4-open-access%2Fpy-open-access-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Get outputs of [FREYA grant award](https://cordis.europa.eu/project/id/777523) from [European Commission](https://doi.org/10.13039/501100000780), including license types

```
{
funder(id: "https://doi.org/10.13039/501100000780") {
  name
  works(query: "fundingReferences.awardNumber:777523", first: 200) {
      totalCount
      nodes {
        id
        titles {
          title
        }     
        types {
          resourceType
        }
        dates {
          date
          dateType
        }
        versionOfCount
				rights {
          rights
          rightsIdentifier
          rightsUri
        }
        fundingReferences {
          funderIdentifier
          funderName
          awardNumber
          awardTitle
        }
        citationCount
        viewCount
        downloadCount
      }
    }
  }
}
```
