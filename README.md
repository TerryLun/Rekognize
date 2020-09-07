# Rekognize
<ul>
<li>Image repository featuring object analysis and identification.</li>
<li>Upload, download or delete image files.</li>
<li>Object labeling using AWS lambda serverless compute</li>
</ul>

## Screenshots
Uploaded image:
![elephantimage](manipulatedelephant-800x534.jpg "inp_image")

Image labels:
![imagelabels](screenshoot.png "screenshot")

## Installation Instructions
In terminal:

`$ pip install flask flask_bootstrap boto3 arrow dominate mimetypes requests`  

Then:

`$ py app.py`

## Tech used
<ul>
<li>Python</li>
<li>Flask</li>
<li>AWS S3</li>
<li>AWS Rekognition</li>
<li>AWS Lambda</li>
<li>AWS API Gateway</li>
</ul>

## To do
<ul>
<li>Cache functionality for calculated image labels to store in DynamoDB to improve performance.</li>
<li>Search filter for images</li>
</ul>