from graphene import Int, String, ObjectType, InputObjectType, Boolean, Enum, Field

# Default page size in case of negative or too large page sizes
DEFAULT_PAGE_SIZE = 10

class SortingDirection(Enum):
    """Enum to determine sorting direction."""
    DESC = 0
    ASC = 1


class PagingParameters(InputObjectType):
    """Contains paging input parameters from a query."""
    page_num = Int(required=True)
    page_size = Int(required=True)
    sorting_field = String(required=False)
    sorting_dir = Field(SortingDirection, required=False)


class PagingInfo(ObjectType):
    """Contains paging information for this model to be returned."""
    page_num = Int(description='The current page number.')
    page_size = Int(description='The size of a requested page.')
    total_num_pages = Int(description='The total number of available pages.')
    has_next_page = Boolean(description='True if the next page exists.')
    has_prev_page = Boolean(description='True if the previous page exists.')