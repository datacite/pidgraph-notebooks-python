import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import datetime
import altair as alt
import vega
alt.renderers.enable('default')


_transport = RequestsHTTPTransport(
    url='https://api.datacite.org/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)



def get_events_by_doi_and_relation_type(doi, relation_type):
    events = requests.get('https://api.datacite.org/events',  
    params={'doi':  doi , 'relation-type': relation_type, 'rows': 1000})
    
    return events.json()

def get_metadata_display(doi):
    query_params = {
        "instrumentId" : doi
    }

    query = gql("""query getInstrument($instrumentId: ID!)
      {
        work(id: $instrumentId) {
          id
          citationCount
          formattedCitation
          repository {
            uid
						name
          }
        }
      }
    """)

    ## ToDo: check the uid of the repo in akita


    data = client.execute(query, variable_values=json.dumps(query_params))

    return data

def format_citations(events, include_authors=False):

    ids = extract_dois(events)

    query_params = {
        "instrumentIds" : ids
    }

    query = gql("""query getInstruments($instrumentIds: [String!])
    {
    works(ids: $instrumentIds) {
        # authors{
        #     title
        #     id
        # }
        nodes{
            formattedCitation
        }
    }
    } 
    """)

    ## ToDo: condition the use of authors

    formatted_citations = client.execute(query, variable_values=json.dumps(query_params))

    return formatted_citations

def extract_ids(events, doi):
    """Return the property sub_id of array of events."""
    ids = []

    for event in events:
        if event['obj']['doi'] != doi:
            ids.append(event['sub_id'])
        if event['subj']['doi'] != doi:
            ids.append(event['sub_id'])

    return ids
