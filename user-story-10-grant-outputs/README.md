## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 10](https://github.com/datacite/freya/issues/45): As a funder, we want to be able to find all the outputs related to our awarded grants, including block grants such as doctoral training grants, for management info and looking at impact. 
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fqaym--kt26-fca709.svg)](https://doi.org/10.14454/qaym-kt26)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-10-grant-outputs%2Fpy-grant-outputs-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Get outputs of [FREYA grant award](https://cordis.europa.eu/project/id/777523) from [European Commission](https://doi.org/10.13039/501100000780)

```
{
funder(id: "https://doi.org/10.13039/501100000780") {
  name
  works(query: "fundingReferences.awardNumber:777523", first: 75) {
      totalCount
      nodes {
        id
        formattedCitation(style: "vancouver")
        titles {
          title
        }
        descriptions {
          description
        }        
        types {
          resourceType
        }
        dates {
          date
          dateType
        }
        versionOfCount
        creators {
          id
          name
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
