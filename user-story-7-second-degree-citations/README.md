## [FREYA](https://www.project-freya.eu/en) WP2 [User Story 7]( https://www.pidforum.org/t/pid-graph-graphql-example-second-degree-citations/939): As a data center, I want to see the citations of publications that use my repository for the underlying data, so that I can demonstrate the impact of our repository. 
                   
### Jupyter Notebook:
[![Identifier](https://img.shields.io/badge/doi-10.14454%2Fxw22--0w50-fca709.svg)](https://doi.org/10.14454/xw22-0w50)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datacite/pidgraph-notebooks-python/master?filepath=user-story-7-second-degree-citations%2Fpy-second-degree-citations-with-output.ipynb)

### Examples of GraphQL Queries Used:
* Retrieve citations of the dataset https://doi.org/10.5061/dryad.234 

```
{
  dataset(id: "https://doi.org/10.5061/dryad.234") {
    id
    titles {
      title
    }
    citationCount
    citations {
      nodes {
        id
        publisher
        titles {
          title
        }
        citationCount
      }
    }
  }
}
```