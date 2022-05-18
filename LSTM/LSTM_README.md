## LSTM README
### In this folder you will have access 'LSTMEyeandBody.ipynb', the main code to run the LSTM, this README with instructions on how to run it, and a subfolder called TrainedModels in which you will have access to a trained Eye Model and trained Body Model and instructions on how to use 'LSTMEyeandBody.ipynb' with a pretrained model. <br />

Before going into the LSTM, make sure you have downloaded the CSV files needed for the LSTM. You can access them here: https://github.com/vysalinas615/Should_I_Drive/tree/main/LSTM/LSTMReadyCSV <br />

For better performance of the LSTM, we recommend connecting to GPU's so that you can train with more epochs and more neural network hidden layers which together give less loss and more accuracy. <br />

If you don't want to connect to a GPU, wanting to train on less epochs or just use the pre trained models we provide here: https://github.com/vysalinas615/Should_I_Drive/tree/main/LSTM/TrainedModels <br />
```
You can simply open the jupyter notebook 'LSTMEyeandBody.ipynb' on your local computer JupyterLab or JupyterNotebook. <br />
Once you open it, skip the first two cells and then continue to run all of the cells. 
```
If you want to connect to a GPU using Google Colab, follow the following steps:
```
Upload 'LSTMEyeandBody.ipynb' to your drive. In your drive install Google Colab and then open the file with that app. 
Follow this video for more details: https://www.youtube.com/watch?v=ovpW1Ikd7pY 
To be able to run the LSTM, also upload the CSV files onto your drive. 

Once you open it, you can run all the cells in the notebook. When we trained connected to the NVIDIA-SMI CUDA provided by Google Colab, each model (Eye and Body) took just short of an hour to complete. 
```
