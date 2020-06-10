## [FREYA](https://www.project-freya.eu/en) WP2 [User Story3](https://www.pidforum.org/t/pid-graph-graphql-example-research-organization/929): As an administrator for the University of Oxford I am interested in the reuse of research outputs from our university, so that I can help identify the most interesting research outputs.
                   
### Jupyter Notebook:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-3-impacts-of-organization%2Fpy-impacts-of-organization-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve the first 300 outputs of [University of Oxford](https://ror.org/052gg0110), with at least 50 views each.

```
{
  organization(id: "https://ror.org/052gg0110") {
    id
    name
    alternateName
    citationCount
    viewCount
    downloadCount
    works(hasViews: 300, first: 50) {
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
