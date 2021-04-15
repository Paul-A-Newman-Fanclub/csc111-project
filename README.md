# csc111-project
CSC111 Final Project: Reconstructing the Ethereum Network Using Graph Data Structures in Python 

## Progress

### Report
_Note: a lot of this stuff can be taken from the proposal, it just needs to be polished. ([Link to proposal/report](https://www.overleaf.com/6829945714dwmwckxbbctz))_
- [X] outline
- [ ] introduction
- [ ] computational overview
  - [ ] data fetching
  - [ ] building the graph
  - [ ] answering the questions (graph traversal algos)
  - [ ] visualization
- [ ] instructions for TA
- [ ] changes to original plan
- [ ] discussion
  - [ ] interpreting results
  - [ ] limitations/obstacles
  - [ ] further exploration/conculsion

### Code
- [X] BigQuery/data fetching
<!--
  - [X] basic functionality
  - [X] writing to CSV
  - [X] allowing user to specify params
    - [X] filter out transactions with value = 0 (Y/N)
    - [X] limit number of transactions (default = 1000)
    - [ ] ~~choose to have no sorting (this might result in a mess)~~
    - [X] change sorting order (default = dates DESC)
    - [X] unrelated: consider removing unnecessary columns from transactions.csv
-->
- [X] building the graph (we're done this, right?)
- [ ] graph traversal algos ~~(this probably won't involve much coding, networkx provides methods that help)~~
  - [ ] are there any paths with length > 1? if so, what is the longest path?
  - [X] any cycles?
- [ ] regression analysis?
- [ ] visualization
  - [X] basic functionality
  - [X] size of nodes depends on Ether balance
  - [X] colour of nodes depends on number of connections
  - [X] display balance/acct. number when hovering over node
  - [X] display transaction value when hovering over edge
  - [ ] experiment with other layouts? (maybe let the user specify)
- [ ] Dash app (this has the lowest priority, we do this if we have time)
  - [ ] basic functionality
  - [ ] extra features (_e.g._ user can choose how nodes are clustered using a dropdown?)
  - [ ] prettifying
