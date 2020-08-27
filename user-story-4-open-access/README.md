## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 4](https://github.com/datacite/pidgraph-notebooks-python/issues/8): As a funder I want to see how many of the research outputs funded by me have an open license enabling reuse, so that I am sure I properly support Open Science.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fq7jn-xw50--fca709.svg)](https://doi.org/10.14454/q7jn-xw50)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-4-open-access%2Fpy-open-access-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Find all outputs and their associated licenses (where available) for three different funders, identified by query1, query2 and query3 respectively: [DFG (Deutsche Forschungsgemeinschaft, Germany)](https://doi.org/10.13039/501100001659), [ANR (Agence Nationale de la Recherche, France)](https://doi.org/10.13039/501100001665) and  [SNF (Schweizerischer Nationalfonds zur Förderung der Wissenschaftlichen Forschung, Switzerland)](https://doi.org/10.13039/501100001711)), up to 300 works per funder.
```
# Generate the GraphQL query: find all outputs and their associated licenses (where available) 
# for three different funders, identified by funder1, funder2 and funder3.
query_params = {
    "funder1" : "https://doi.org/10.13039/501100001659",
    "funder2" : "https://doi.org/10.13039/501100001665",
    "funder3" : "https://doi.org/10.13039/501100001711",
    "maxWorks" : 200
}

query getGrantOutputsForFundersById(
    $funder1: ID!,
    $funder2: ID!,
    $funder3: ID!
    )
{
funder1: funder(id: $funder1) {
  name
  id
  works {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder2: funder(id: $funder2) {
  name
  id
  works {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder3: funder(id: $funder3) {
  name
  id
  works {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder1Dataset: funder(id: $funder1) {
  name
  id
  works(resourceTypeId: "Dataset") {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder1Text: funder(id: $funder1) {
  name
  id
  works(resourceTypeId: "Text") {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder2Dataset: funder(id: $funder2) {
  name
  id
  works(resourceTypeId: "Dataset") {
      totalCount
      licenses {
        id
        title
        count
      }       
    }
  },
funder2Text: funder(id: $funder2) {
  name
  id
  works(resourceTypeId: "Text") {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  },
funder3Dataset: funder(id: $funder3) {
  name
  id
  works(resourceTypeId: "Dataset") {
      totalCount
      licenses {
        id
        title
        count
      }       
    }
  },
funder3Text: funder(id: $funder3) {
  name
  id
  works(resourceTypeId: "Text") {
      totalCount
      licenses {
        id
        title
        count
      }        
    }
  } 
}
```
