from datetime import date, datetime
import pickle
from typing import List, Optional
from fastapi import File, UploadFile
from psycopg2 import Binary
from pydantic import BaseModel, EmailStr
from sqlalchemy import BINARY, LargeBinary


# user section

class UserPersonalInfo(BaseModel):
    middel_name: Optional[str] = None
    birthdate: datetime
    gender: str
    nationality: str
    marital_status:  Optional[str] = None
    military_status: Optional[str] = None
    driving_license: Optional[str] = None
    address: str
    phone: str


class UserPersonalInfoIn(UserPersonalInfo):
    first_name: str
    last_name: str

    class Config():
        arbitrary_types_allowed = True


class UserCareerInterests(BaseModel):
    career_level: str
    years_of_experience: Optional[str] = None
    job_types: list[str]
    job_titles: Optional[list[str]] = None
    job_categories: list[str]
    min_salary: str
    hide_min_salary: bool
    perfered_job_location: Optional[str] = None
    current_job_search_status: Optional[str] = None


class UserCvOut(BaseModel):
    cv_name: str
    # cv_dict: dict
    updated_at: datetime

    class Config():
        arbitrary_types_allowed = True
        from_attributes = True


class UserImgOut(BaseModel):
    img_name: str
    created_at: datetime

    class Config():
        from_attributes = True


class UserWorkExperience(BaseModel):
    id: Optional[int] = None
    experience_type: str
    job_title: str
    job_category: list[str]
    company_name: str
    start_date: datetime
    end_date: Optional[datetime] = None
    work_there: bool


class UserWorkExperienceOut(UserWorkExperience):
    updated_at: datetime

    class Config():
        from_attributes = True


class UserSkills(BaseModel):
    skill: str
    proficiency: Optional[str] = 'Beginner'


class UserSkillsOut(UserSkills):
    id: int

    class Config():
        from_attributes = True


class UserDegree(BaseModel):
    id: Optional[int] = None
    degree: str
    university: str
    field_of_study: list[str]
    degree_year: str
    grade: str
    updated_at: Optional[datetime] = None


class UserHighSchool(BaseModel):
    id: Optional[int] = None
    degree: str
    school_name: str
    certificate_name: str
    language_of_study: str
    graduation_year: str
    highschool_grade: str
    updated_at: Optional[datetime] = None


class UserLanguage(BaseModel):
    id: Optional[int] = None
    language: str
    proficiency: str


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreateIn(User):
    password: str
    pass


class UserCreateOut(User):
    id: int
    created_at: datetime

    class Config():
        from_attributes = True


class UserProfile(User):
    id: int
    created_at: datetime
    img: Optional[UserImgOut]
    cv: Optional[UserCvOut]
    personal_info: Optional[UserPersonalInfo]
    career_interests: Optional[UserCareerInterests]
    work_experience: Optional[List[UserWorkExperienceOut]]
    degrees: Optional[List[UserDegree]]
    highschool: Optional[List[UserHighSchool]]
    skills: Optional[List[UserSkillsOut]]
    languages: Optional[List[UserLanguage]]

    class Config():
        from_attributes = True


class CurrentUserOut(User):
    pass

    class Config():
        from_attributes = True

# auth section


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class LoginOut(Token):
    current_user: CurrentUserOut

    class Config():
        from_attributes = True


# job section
class Job(BaseModel):
    title: str
    company: str
    location: str
    type: str
    skills: str
    link: str


class JobCreate(Job):
    created_at: datetime
    expired_at: datetime


class JobOut(Job):
    created_at: datetime

    class Config():
        from_attributes = True

# keywords section


class keywords(BaseModel):
    keywords: str


class Out_Search_Keyword(BaseModel):
    user_id: int
    id: int
    keywords: str


class Url(BaseModel):
    url: str


class Password(BaseModel):
    password: str


class skill(BaseModel):
    name: str
    frequency: int
