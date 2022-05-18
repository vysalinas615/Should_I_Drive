### In this folder you will have access to an Eye Tracking Trained LSTM model and a Body Tracking Trained LSTM model  <br />
We trained both models on 300 epochs each. <br />
##### Steps for running LSTMEyeandBody.ipynb with the pre trained model: <br />

Everytime you load a model, you must first define the dataset, initialize the LSTM, and define the structure of the model, therefore run the cells under these headers:
```
- Load necessary imports 
- Bidirectional Recurrent Neural Network
- Eye Dataset
- Body Dataset
- Load Eye Dataset
- Load Body Dataset
- Divide Dataset for Training and Testing
- Make Eye NN Loders
- Make Body NN Loders
- LSTM Init parameters
- Eye Tracking LSTM
- Body Tracking LSTM
```

If you would like to test out these pre trained models, connecting to a GPU:
```
After connecting to a GPU and runnig the cells above, run the following cells:
-Load Trained Eye Model
-Test Eye LSTM
-Load Trained Body Model
-Test Body LSTM
```
If you would like to test out these pre trained models, without connecting to a GPU:
``` 
Since the model was trained using a GPU, when you load the model, you have to convert it to CPU usage: 
Modify the -Load Trained Eye Model cell to the following:

eye_model_path = 'ShouldIDrive_eye_tracking_colab.pkl'
eye_model.load_state_dict(torch.load(eye_model_path, map_location=torch.device('cpu')))
eye_model.eval()

Now you can run - Test Eye LSTM cell.

Do the same for the Body cells. 
```
