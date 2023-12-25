from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: int
    email: str = None
    phone_number: str = None
    default_lang: str
    default_role: str
    name: str = None
    image_url: str = None

class UpdateProfileRequest(BaseModel):
    default_lang: str = None
    default_role: str = None
    name: str = None
    image_id: str = None


