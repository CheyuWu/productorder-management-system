from typing import Dict, Union
from fastapi import status

response_base: Dict[Union[int, str], Dict[str, str]] = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "You missed some parameters or paramters was not corrected"
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "You are not allow to do this operation"
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Unknown error"},
}


create_user_response = {**response_base}
delete_user_response = {**response_base}
