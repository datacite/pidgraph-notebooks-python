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

