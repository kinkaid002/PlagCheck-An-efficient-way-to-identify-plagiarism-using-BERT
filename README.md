# PlagCheck-An-efficient-way-to-identify-plagiarism-using-BERT
PlagCheck is a plagiarism detection website which is capable of detecting context based plagiarism between document. i.e., it can detect plagiarism among paraphrased documents as well using BERT!

##Side notes
1] views.py and auth.py require the user's AWS S3 bucket access key as well as the secret access key, which can be obtained once the S3 bucket is created
2] Pinecone database provides the database api key, which will be required in views.py file to access the database vectors.

