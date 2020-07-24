## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 4](https://github.com/datacite/pidgraph-notebooks-python/issues/8): As a funder I want to see how many of the research outputs funded by me have an open license enabling reuse, so that I am sure I properly support Open Science.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fqaym--kt26-fca709.svg)](https://doi.org/10.14454/qaym-kt26)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-4-open-access%2Fpy-open-access-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Find all outputs and their associated licenses (where available) for three different funders, identified by query1, query2 and query3 respectively: [DFG (Deutsche Forschungsgemeinschaft, Germany)](https://doi.org/10.13039/501100001659), [ANR (Agence Nationale de la Recherche, France)](https://doi.org/10.13039/501100001665) and  [SNF (Schweizerischer Nationalfonds zur Förderung der Wissenschaftlichen Forschung, Switzerland)](https://doi.org/10.13039/501100001711)), up to 300 works per funder.
```
query_params = {
    "query1" : "https://doi.org/10.13039/501100001659",
    "query2" : "https://doi.org/10.13039/501100001665",
    "query3" : "https://doi.org/10.13039/501100001711",
    "maxWorks" : 300
}

query getGrantOutputsForFundersById(
    $query1: ID!,
    $query2: ID!,
    $query3: ID!,
    $maxWorks: Int!
    )
{
query1: funder(id: $query1) {
  name
  id
  works(first: $maxWorks) {
      totalCount
      licenses {
        id
        title
        count
      }        
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
      }
    }
  },
query2: funder(id: $query2) {
  name
  id
  works(first: $maxWorks) {
      totalCount
      licenses {
        id
        title
        count
      }       
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
      }
    }
  },  
query3: funder(id: $query3) {
  name
  id
  works(first: $maxWorks) {
      totalCount
      licenses {
        id
        title
        count
      }       
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
      }
    }
  }  
}
```
