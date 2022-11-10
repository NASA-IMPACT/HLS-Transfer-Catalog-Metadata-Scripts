import csv
from datetime import datetime
from datetime import timezone
from pip._vendor import requests
import uuid
from config import BaseConfig

base_url = BaseConfig.CMR_BASE_URL
query_url = base_url + BaseConfig.GRANULES_URL

filename = BaseConfig.OUTPUT_FILE_NAME
extension = BaseConfig.OUTPUT_FILE_EXTENSION

outfile = "cmrmetadata.csv"

concept_id = BaseConfig.CONCEPT_ID

page_num = BaseConfig.PAGE_NUM
page_size = BaseConfig.PAGE_SIZE

s3_bucket_name = BaseConfig.S3_BUCKET_NAME

start_date = BaseConfig.START_DATE
end_date = BaseConfig.END_DATE

date_range = start_date + ',' + end_date

bounding_box = BaseConfig.BOUNDING_BOX

page_num_limit = BaseConfig.PAGE_NUM_LIMIT

with open(outfile, "w", newline= "") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(["Id", "Name", "ContentLength", "IngestionDate", "ContentDate:Start", "ContentDate:End", "Checksum:Algorithm", "Checksum:Value", "IsSealed", "SourceStorageId", "DestStorageId"])
    count = 0
    while (page_num <= page_num_limit):
        formated_url = query_url.format(concept_id, page_num, page_size, date_range, bounding_box)
        print(formated_url)
        resp = requests.get(query_url.format(concept_id,page_num,page_size, date_range, bounding_box)).json()
        entries = resp["feed"]["entry"]
        for i,granule in enumerate  (entries):
            for link in granule["links"]:
                if (link["href"].startswith(s3_bucket_name)):
                    Id = uuid.uuid1()
                    Name = link["href"].split(s3_bucket_name)[1]
                    IngestionDate = datetime.fromisoformat(granule["time_start"][:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    ContentDateStart = datetime.fromisoformat(granule["time_start"][:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    ContentDateEnd = datetime.fromisoformat(granule["time_end"][:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    ContentLength = 100
                    ChecksumAlgorithm = 'SHA-256'
                    ChecksumValue = '2c044996bfd029c30c22f62b51e19556'
                    IsSealed = "false"
                    SourceStorageId = "abcdef"
                    DestStorageId = "defabc"
                    writer.writerow([Id, Name, ContentLength, IngestionDate, ContentDateStart, ContentDateEnd, ChecksumAlgorithm,
                                    ChecksumValue, IsSealed, SourceStorageId, DestStorageId])
                    count = count + 1
        page_num = page_num + 1
    print("Total Number of records in CSV file is {}".format(count))
