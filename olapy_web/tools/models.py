import attr


@attr.s
class Facts(object):
    """Facts class used to encapsulate config file attributes."""

    table_name = attr.ib()
    keys = attr.ib()
    measures = attr.ib()
    columns = attr.ib()


@attr.s
class Cube(object):
    """Cube class used to encapsulate config file attributes."""

    name = attr.ib()
    source = attr.ib()
    facts = attr.ib()
    tables = attr.ib()


@attr.s
class Table(object):
    """Column class used to encapsulate config file attributes for web client."""

    name = attr.ib()
    new_names = attr.ib()
    columns = attr.ib()


@attr.s
class Dashboard(object):
    """Column class used to encapsulate config file attributes for web client."""

    global_table = attr.ib()
    pie_charts = attr.ib()
    bar_charts = attr.ib()
    line_charts = attr.ib()
