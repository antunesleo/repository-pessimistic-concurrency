# parallel-aggregates
Studying the persistence implementation of aggregates in parallel in repository and active record patterns

### Pre-requisites
* sqlite
* python 3.8

# Setup

    $ mkvirtualenv -p python3.8 paralleo-aggregates
    $ workon python3.8
    $ pip install -r requirements.txt

### Setup aggregate_classic_repository
    $ sqlite3 aggregate-classic-repository.db
    $ cd aggreagete_classic_repository
    $ alembic init ./migrations
    $ alembic upgrade head
    $ sqlite3 aggreaget-classic-repository.db < migrations/data.sql

### Run

    $ python run.py
