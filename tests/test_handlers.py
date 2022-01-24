import json
from unittest import TestCase
from unittest.mock import patch

import Main_project.handlers


class TestFunc(TestCase):
    @patch(
        "Main_project.handlers.get_username_from_http",
        return_value="yersh",
    )
    def test_message_status(self, get_username_from_http):
        assert json.loads(
            Main_project.handlers.message_status(
                "23274bba-8078-486e-911a-0a6dfc3e7624"
            )
        ) == {
            "uuid": "23274bba-8078-486e-911a-0a6dfc3e7624",
            "created_by": "yersh",
            "created_at": "2022-01-21 21:55:09.493313",
            "text_message": "check_queue22",
            "number": "+7892199922034",
            "provider": "FileProvider",
            "sent_at": "2022-01-21 21:55:09.520754",
            "delivered_at": "2022-01-21 21:55:19.520754",
            "status": "Delivered",
        }
