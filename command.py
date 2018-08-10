import subprocess

filename = "contrat-de-travail-CDI.jpg"
output_file = "outputbase"
language = "fra"
comm=["tesseract",filename,output_file,"-l",language]
subprocess.run(comm, shell=True)