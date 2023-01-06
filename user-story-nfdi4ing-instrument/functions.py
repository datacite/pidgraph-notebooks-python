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

def view_metadata_display(data):
    html_formatted_citation = f"<p>{data['work']['formattedCitation']}</p>"
    html_citation_count = f"<p>Citation count: {data['work']['citationCount']}</p>"
    html_repository_link = f'<a href="https://commons.datacite.org/repositories/{data["work"]["repository"]["uid"]}">{data["work"]["repository"]["name"]}</a>'

    html = '<div>' + html_formatted_citation + html_citation_count + html_repository_link + '</div>'

    return html

def get_html_table(formatted_citations_array):
    html_table = '<table>'
    for item in formatted_citations_array['works']['nodes']:
        html_table += '<tr><td>' + item['formattedCitation'] + '</td></tr>'

    html_table += '</table>'

    # ToDo: add table header

    return html_table

def get_authors_html_table(authors):
    html_table = '<table>'
    for item in authors['works']['authors']:
        html_table += '<tr><td>' + item['title'] + '</td></tr>'

    html_table += '</table>'

    # ToDo: add table header

    return html_table

def generate_histogram_spec(data):
    """Return a vega-lite specification for a bar chart with the citation counts."""
    ## data['meta']['occurred']
    
    chartWidth = 500
    thisYear = datetime.datetime.now().year + 1
    lowerBoundYear = ((thisYear - 10) / 5) * 5

    spec = {
    "$schema": 'https://vega.github.io/schema/vega-lite/v4.json',
    "data": {
        "values": data
    },
    "padding": { "left": 5, "top": 5, "right": 5, "bottom": 5 },
    "transform": [
        {
        "calculate": 'toNumber(datum.title)',
        "as": 'period'
        },
        {
        "calculate": 'toNumber(datum.title)+1',
        "as": 'bin_end'
        },
        {
        "filter": f"toNumber(datum.title) >= {lowerBoundYear}"
        }
    ],
    "width": chartWidth,
    "mark": {
        "type": 'bar',
        "cursor": 'pointer',
        "tooltip": True
    },
    "selection": {
        "highlight": {
        "type": 'single',
        "empty": 'none',
        "on": 'mouseover'
        }
    },
    "encoding": {
        "x": {
        "field": 'period',
        "bin": {
            "binned": True,
            "step": 1,
            "maxbins": thisYear - lowerBoundYear
        },
        "type": 'quantitative',
        "axis": {
            "format": '1',
            "labelExpr": 'datum.title % 5 === 0 ? datum.title : ""'
        },
        "scale": {
            "domain": [lowerBoundYear, thisYear]
        }
        },
        "x2": {
        "field": 'bin_end'
        },
        "y": {
        "field": 'count',
        "type": 'quantitative',
        "axis": {
            "format": ',f',
            "tickMinStep": 1
        }
        },
        "color": {
        "field": 'count',
        "scale": { "range": ["#1abc9c"] },
        "type": 'nominal',
        "legend": None,
        "condition": [{ "selection": 'highlight', "value": '#34495e' }]
        }
    },
    "config": {
        "view": {
        "stroke": None
        },
        'axis': {
        "grid": False,
        "title": None,
        "labelFlush": False
        }
    }
    }
    return spec


def render_histogram(spec):
    return(alt.Chart.from_dict(spec))


def main(doi)


# print(get_events_by_doi_and_relation_type('10.5255/ukda-sn-3592-1', 'cites'))

# render_histogram(generate_histogram_spec((get_events_by_doi_and_relation_type('10.5255/ukda-sn-3592-1', 'cites')['meta']['occurred'])))



# print(get_events_by_doi_and_relation_type('10.5255/ukda-sn-3592-1', 'cites'))
# print(get_metadata_display('10.5255/ukda-sn-3592-1'))

# print(format_citations(['10.5255/ukda-sn-3592-1','https://doi.org/10.5255/ukda-sn-1930-1']))

# print(get_html_table(format_citations(['10.5255/ukda-sn-3592-1','https://doi.org/10.5255/ukda-sn-1930-1'])))


# print(view_metadata_display(get_metadata_display('10.5255/ukda-sn-3592-1')))

# print(get_metadata_display('10.5255/ukda-sn-3592-1'))