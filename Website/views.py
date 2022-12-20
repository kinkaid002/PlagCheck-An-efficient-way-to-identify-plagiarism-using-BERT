from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import boto3
from werkzeug.utils import secure_filename
import pinecone
import pinecone.info
import pandas as pd
from sentence_transformers import SentenceTransformer, util


views = Blueprint('views', __name__)

access_key = '' #Enter your AWS s3 bucket access key here
secret_access_key = '' #Enter your AWS s3 bucket secret access key here

# s3 = boto3.client('s3',
#                     aws_access_key_id = access_key,
#                     aws_secret_access_key = secret_access_key)

s3 = boto3.resource(
    service_name = 's3',
    region_name = 'ap-south-1',
    aws_access_key_id = '', #Enter your AWS s3 bucket access key here or just use the variable defined earlier "access_key"
    aws_secret_access_key = '' #Enter your AWS s3 bucket secret access key here or just use the variable defined earlier "secret_access_key"
)


@views.route('/')
# @login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/upload', methods = ['POST'])
@login_required
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.Bucket('varunkalbhore-s3').upload_file(
                # Bucket = 'Your S3 bucket name',
                Filename = filename,
                Key = 'Folder name/' + str(current_user.email) + '/' + str(filename)
            )

            # s3_object = s3.get_object(Bucket = 'Your S3 bucket name', Key = 'Folder name/' + str(current_user.email) + '/' + str(filename))
            #print(s3_object)
            
            obj = s3.Bucket('#Your S3 Bucket name#').Object('Folder name/' + str(current_user.email) + '/' + str(filename)).get()
            text = obj['Body'].read().decode()
            print(text)
            

            api_key = "" #Enter your pinecone database api-key
            pinecone.init(api_key=api_key, environment='us-west1-gcp')
            model = SentenceTransformer('all-mpnet-base-v2')
            index = pinecone.Index('sampleindex')
            encoding = model.encode(text).tolist()
            # print(encoding)
            top_k = 1
            result = index.query(queries=[encoding], top_k = top_k )
            print(result)
            abc=[x['score']for x in result['results'][0]['matches']]
            plag = int(abc[0]*100)
            

            if plag>30:
                msg = str(plag) +"% Plagiarism found"
            else:
                msg = "No Plagiarism Detected"    
            # msg = obj
        else:
            msg = "No files selected"

    return render_template("home.html", msg = msg, user=current_user)

