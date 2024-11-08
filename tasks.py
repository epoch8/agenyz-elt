import asyncio
from typing import Any, Dict, List

from prefect import task
from prefect_shell.commands import ShellProcess, ShellOperation
from prefect.utilities.asyncutils import sync_compatible
from prefect.utilities.processutils import open_process


class ShellProcessStdErr(ShellProcess):
    @sync_compatible
    async def wait_for_completion(self) -> None:
        self.logger.debug(f"Waiting for PID {self.pid} to complete.")

        await asyncio.gather(
            self._capture_output(self._process.stdout),
            self._capture_output(self._process.stderr),
        )
        await self._process.wait()

        if self.return_code != 0:
            raise RuntimeError(
                f"PID {self.pid} failed with return code {self.return_code}. \n {self._output}"
            )
        self.logger.info(
            f"PID {self.pid} completed with return code {self.return_code}."
        )

class ShellOperationStdErr(ShellOperation):
    @sync_compatible
    async def run(self, **open_kwargs: Dict[str, Any]) -> List[str]:
        input_open_kwargs = self._compile_kwargs(**open_kwargs)
        async with open_process(**input_open_kwargs) as process:
            shell_process = ShellProcessStdErr(shell_operation=self, process=process)
            num_commands = len(self.commands)
            self.logger.info(
                f"PID {process.pid} triggered with {num_commands} commands running "
                f"inside the {(self.working_dir or '.')!r} directory."
            )
            await shell_process.wait_for_completion()
            result = await shell_process.fetch_result()

        return result



@task(name="meltano_elt", task_run_name="{project_name}-{environment}-{extractor}-{loader}")
def meltano_elt(environment: str, extractor: str, loader: str, full_refresh=False, log_level=False):
    elt_command = f"meltano {'--log-level debug' if log_level else ''} --environment {environment} run {extractor} {loader}"
    if full_refresh:
        elt_command += " --full-refresh"
    try:
        res = ShellOperationStdErr(
            commands=[elt_command],
        ).run()
    except RuntimeError as e:
        if "pipeline is already running" in (str(e)):
            res = ""
        else:
            raise e
    return res 




@task(name="meltano_dbt", task_run_name="{project_name}-{environment}-dbt-{dbt_args}")
def meltano_dbt(environment: str, dbt_args: str = ""):
    command = f"meltano --environment {environment} invoke dbt-postgres run {dbt_args} "
    res = ShellOperation(
        commands=[command],
    ).run()
    return res 