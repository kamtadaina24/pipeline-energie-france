import boto3
from botocore.exceptions import ClientError

# 1. On crée un "client" : c'est l'objet qui parle au serveur S3
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",   # notre S3 local (sur AWS, on retirerait cette ligne)
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)

# 2. On crée le bucket "raw"
try:
    s3.create_bucket(Bucket="raw")
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code not in ["BucketAlreadyOwnedByYou", "BucketAlreadyExists"]:
        #print("Le bucket 'raw' existe déjà, on continue...")
        raise
    
    
# 3. On envoie un petit fichier de test dedans
s3.put_object(Bucket="raw", Key="test/bonjour.txt", Body=b"Bonjour S3 local !")

# 4. On liste le contenu du bucket pour vérifier
reponse = s3.list_objects_v2(Bucket="raw")
for objet in reponse.get("Contents", []):
    print(objet["Key"], objet["Size"], "octets")