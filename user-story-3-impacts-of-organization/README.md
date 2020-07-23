## [FREYA](https://www.project-freya.eu/en) WP2 [User Story3](https://www.pidforum.org/t/pid-graph-graphql-example-research-organization/929): As an administrator for the University of Oxford I am interested in the reuse of research outputs from our university, so that I can help identify the most interesting research outputs.
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fe23v--x328-fca709.svg)](https://doi.org/10.14454/e23v-x328)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-3-impacts-of-organization%2Fpy-impacts-of-organization-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve the first 100 outputs of [University of Oxford](https://ror.org/052gg0110), with at least 100 views each.

```
{
  organization(id: "https://ror.org/052gg0110") {
    id
    name
    alternateName
    citationCount
    viewCount
    downloadCount
    works(hasViews: 100, first: 100) {
      totalCount
      published {
        title
        count
      }
      resourceTypes {
        title
        count
      }
      nodes {
        id
        type
        publisher
        publicationYear
        titles {
          title
        }
        citations {
            nodes {
              id
        	}
        }        
        creators {
          id
          name
          affiliation {
            id
            name
          }
        }
        citationCount
        viewCount
        downloadCount
      }
    }
  }
}

```
