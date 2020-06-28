from enum import Enum


class DriverCommand(Enum):
    START = "start",
    GET = "get",
    CLICK = "click",
    GET_ELEMENT_TEXT = "get_element_text",
    SEND_KEYS = "send_keys",
    TYPE = "type",
    GET_ATTR = "get_attr"
    GET_PAGE_SOURCE = "get_page_source"
