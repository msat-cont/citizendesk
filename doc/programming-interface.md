### Twitter search

Twitter searches can be triggered as specified [in the examples](https://github.com/sourcefabric-innovation/citizendesk-core/blob/master/opt/citizendesk/etc/utils/examples.txt#L24).

The results of a twitter search will be added to the reports
collection. Those reports will have the following `channel` value:

    { type: 'search', request: 'any request id' }

The request id must be provided in the HTTP request, the core does not
check its unicity, it is responsability of the caller.

