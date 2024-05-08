from io import BytesIO

from werkzeug.exceptions import InternalServerError

from src.common.exception.BusinessException import (BusinessException,
                                                    BusinessExceptionEnum)
from src.user.repository.configuration_repository import \
    ConfigurationRepository
from src.user.utils.excel_parser import parse_excel_stream_to_configurations


class ConfigurationService:
    def __init__(self, repository: ConfigurationRepository):
        self.repository = repository

    def process_excel_file(self, file_stream: BytesIO) -> list[dict[str, str]]:
        # Step 1: parse excel
        try:
            configurations = parse_excel_stream_to_configurations(file_stream)
        except BusinessException as e:
            raise e

        responses = []
        # Step 2: clean db
        try:
            self.repository.clean_configurations()
        except Exception as e:
            raise InternalServerError from e

        # Step 3: Save each configuration from the parsed data
        for config in configurations:
            user_case_key = f"{config.user_email}-{config.case_id}"
            result = {"user_case_key": user_case_key}
            try:
                if config.user_email == "":
                    raise BusinessException(BusinessExceptionEnum.InvalidUserEmail)
                if config.case_id == -999:
                    raise BusinessException(BusinessExceptionEnum.InvalidUserEmail)
                self.repository.save_configuration(config)
                result["status"] = "added"
            except Exception:
                result["status"] = "failed"
            responses.append(result)

        return responses
