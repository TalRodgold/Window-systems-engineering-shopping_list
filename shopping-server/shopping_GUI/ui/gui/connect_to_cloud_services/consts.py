import enum
import os

# api for recepies
RECEIPES_API = "https://edamam-recipe-search.p.rapidapi.com/api/recipes/v2"

# query string (with empty 'q') for recpies
RECEIPES_QUERYSTRING = {"type":"public","co2EmissionsClass":"A+","field[0]":"uri","q":"","beta":"true","random":"true"}

# recepies headers containing key, host and languages
RECEIPES_HEADERS = {
	"Accept-Language": "en",
	"X-RapidAPI-Key": "e4cb194fedmsh8f5e57ba5fc557cp16248ajsn0d64d197f11a",
	"X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
}

# key for imagga 
IMAGGA_KEY = 'acc_f7fdd2eb8b0f369'

# key (secret) for imagga
IMAGGA_SECRET = 'fa10d16de4c930c643cfb106f4b3d0f2'

# imagga api 
IMAGGA_API = 'https://api.imagga.com/v2/tags'

# Basic authentication header for imagga
IMAGGA_AUTH_HEADER = {
    'Authorization': 'Basic YWNjX2Y3ZmRkMmViOGIwZjM2OTpmYTEwZDE2ZGU0YzkzMGM2NDNjZmIxMDZmNGIzZDBmMg=='
}

# temporary file path for saving images before uploading to imagga
TMP_FILE_PATH = os.path.join("PyOneDark_Qt_Widgets_Modern_GUI", "gui", "connect_to_cloud_services", "tmp")

# confidence number for imagga resaults
IMAGGA_CONFIDENCE = 80