from pydantic import BaseModel, HttpUrl, model_validator

class Image(BaseModel):
    link: HttpUrl
    type: str
    width: int
    height: int
    
class ImageURLRequest(BaseModel):
    imgur_url: HttpUrl
    agreed_to_terms: bool
    
    @model_validator(mode='after')
    def check_terms(self) -> 'ImageURLRequest':
        if not self.agreed_to_terms:
            raise ValueError("You must agree to the terms.")
        return self

class ImageURLResponse(BaseModel):
    image: Image
    score: float
    


