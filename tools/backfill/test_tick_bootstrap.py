from intelligence.data.tick.modes.bootstrap import BootstrapMode
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter
from intelligence.data.tick.sources import MT5Source

source = MT5Source()
writer = TickSQLiteWriter()
bootstrap = BootstrapMode(source, writer)
bootstrap.run("EURUSD", days_back=1, hours_batch=1)
