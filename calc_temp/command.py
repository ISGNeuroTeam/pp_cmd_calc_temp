import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


def calc_temp(speed):
    """
    Calulates temp from speed
    :param speed:
    :return:
    """
    if speed == 0:
        return "0:00"
    int_part = 60 // speed
    float_part = 60 / speed - int_part
    return f"{int(int_part)}:{round(float_part * 60)}"


class CalcTempCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("column", required=True, otl_type=OTLType.TEXT),
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start calc_temp command')
        # that is how you get arguments
        column = self.get_arg("column").value
        temp_column = self.get_arg("column").named_as

        # Make your logic here
        df[temp_column] = df[column].apply(lambda x: calc_temp(x))

        # Add description of what going on for log progress
        self.log_progress('First part is complete.', stage=1, total_stages=1)
        #
        return df
