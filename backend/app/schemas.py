from pydantic import BaseModel, HttpUrl, model_validator

class Image(BaseModel):
    link: HttpUrl
    type: str
    width: int
    height: int
    
class ImageURLRequest(BaseModel):
    imgur_url: HttpUrl
    agreedToTerms: bool
    
    @model_validator(mode='after')
    def check_terms(self) -> 'ImageURLRequest':
        if not self.agreedToTerms:
            raise ValueError("You must agree to the terms.")
        return self

class ImageURLResponse(BaseModel):
    image: Image
    score: float
    


