import os

class BaseConfig:
    CMR_BASE_URL = os.getenv("CMR_BASE_URL", "https://cmr.earthdata.nasa.gov/") 
    GRANULES_URL = os.getenv("GRANULES_URL", "search/granules.json?collection_concept_id={}&page_num={}&page_size={}&created_at[]={}&bounding_box={}")
    OUTPUT_FILE_NAME = os.getenv("OUTPUT_CSV_FILE_NAME", "cmrmetadata")
    OUTPUT_FILE_EXTENSION = os.getenv("OUTPUT_FILE_EXTENSION", ".csv")
    PAGE_NUM = os.getenv("PAGE_NUM", 1)
    PAGE_SIZE = os.getenv("PAGE_SIZE", 10)
    CONCEPT_ID = os.getenv("CONCEPT_ID", "C2021957657-LPCLOUD")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "s3://lp-prod-protected/")
    START_DATE = "2021-01-01T10:00:00Z"
    END_DATE = "2022-03-10T12:00:00Z"
    BOUNDING_BOX="-10,-5,10,5"