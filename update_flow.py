from prefect import flow
from constants import PROJECT_NAME
from tasks import meltano_dbt, meltano_elt


@flow(name=f"{PROJECT_NAME} elt")
def elt(log_level=False, dbt_args="", full_refresh=False):
    meltano_elt(
        environment="prod",
        extractor="tap-mongodb",
        loader="target-postgres",
        log_level=log_level,
    )
    meltano_elt(
        environment="prod",
        extractor="tap-postgres",
        loader="target-postgres",
        log_level=log_level,
    )
    meltano_dbt(
        environment="prod",
        dbt_args=dbt_args,
    )
