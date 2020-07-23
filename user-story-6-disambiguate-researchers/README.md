## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 6](https://www.pidforum.org/t/pid-graph-graphql-example-disambiguate-researchers/931): As a researcher, I am looking for more information about another researcher with a common name, but don’t know his/her ORCID ID.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2F03vp--ry06-fca709.svg)](https://doi.org/10.14454/03vp-ry06)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-6-disambiguate-researchers%2Fpy-disambiguate-researchers-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve first 50 researcher records with any field matching both terms: "John" and "Smith":

```
{
  people(query: "John AND Smith", first: 50) {
    totalCount
    nodes {
      id
      givenName
      familyName
      name
      affiliation {
        name
      }
      works(first: 3) {
        nodes {
          id
          publicationYear
          titles {
            title
          }
          creators {
            id
            name
            affiliation {
              id
              name
            }
          }
          subjects {
            subject
          }
        }
      }
    }
  }
}
```
