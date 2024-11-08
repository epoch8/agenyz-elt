from prefect import flow
from constants import PROJECT_NAME
from tasks import meltano_dbt, meltano_elt


@flow(name=f"{PROJECT_NAME} elt")
def elt(log_level=False, dbt_args="", full_refresh=False):
    meltano_elt(
        PROJECT_NAME,
        "prod",
        "tap-mongodb",
        "target-postgres",
    )
    meltano_elt(
        PROJECT_NAME,
        "prod",
        "tap-postgres",
        "target-postgres",
    )
    meltano_dbt(
        PROJECT_NAME,
        "prod",
        dbt_args=dbt_args,
        full_refresh=full_refresh,
    )
