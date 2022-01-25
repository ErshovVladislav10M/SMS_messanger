import json
from unittest import TestCase
from unittest.mock import patch

import Main_project.handlers


class TestFunc(TestCase):
    @patch(
        "Main_project.handlers.get_headers_authorization",
        return_value="Basic eWVyc2g6",
    )
    def test_authentication_positive(self, get_headers_authorization):
        assert not Main_project.handlers.authentication()

    @patch(
        "Main_project.handlers.get_headers_authorization",
        return_value="Basic eWVyc2g6",
    )
    def test_get_username_from_http(self, get_headers_authorization):
        assert Main_project.handlers.get_username_from_http() == "yersh"

    @patch(
        "Main_project.handlers.get_headers_authorization",
        return_value="Basic eWVyc2g6",
    )
    def test_message_status(self, get_headers_authorization):
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

    @patch(
        "Main_project.handlers.get_headers_authorization",
        return_value="Basic eWVyc2g6",
    )
    def test_create_message_by_user(self, get_headers_authorization):
        with patch("Main_project.handlers.add_message_to_db") as fun:
            fun.return_value = json.dumps(
                "23274bba-8078-486e-911a-0a6dfc3e7624"
            )
            assert (
                json.loads(
                    Main_project.handlers.create_message_by_user(
                        "qwerty", "+79212224466", "FileProvider"
                    )
                )
                == "23274bba-8078-486e-911a-0a6dfc3e7624"
            )
